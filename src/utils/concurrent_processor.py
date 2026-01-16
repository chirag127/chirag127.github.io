"""
Concurrent Processor - Handles parallel session processing with rate limiting.

Manages concurrent session creation and polling with intelligent rate limiting
and error recovery.
"""

import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from src.core.session_manager import SessionManager
from src.core.cache import CacheManager

logger = logging.getLogger("ConcurrentProcessor")


class ConcurrentProcessor:
    """
    Processes multiple repositories concurrently with rate limiting.
    """

    def __init__(
        self,
        session_manager: SessionManager,
        cache: CacheManager,
        max_workers: int = 5  # Changed from 100 to 5 (AGENTS.md limit)
    ) -> None:
        self.session_manager = session_manager
        self.cache = cache
        self.max_workers = max_workers
        self._stats_lock = threading.Lock()
        self.stats = {
            "total": 0,
            "processed": 0,
            "skipped": 0,
            "failed": 0,
            "prs": 0
        }

    def increment_stat(self, key: str, value: int = 1) -> None:
        """Thread-safe stat increment."""
        with self._stats_lock:
            self.stats[key] += value

    def process_batch(
        self,
        batch: list[dict],
        create_session_fn: callable,
        dry_run: bool = False
    ) -> dict[str, dict]:
        """
        Process a batch of repositories concurrently.

        Phase 1: Create all sessions in parallel
        Phase 2: Poll all sessions until completion

        Returns:
            {session_id: {"repo": repo, "source": source}}
        """
        logger.info("\n" + "="*60)
        logger.info("📤 PHASE 1: Creating ALL sessions concurrently...")
        logger.info(f"   Max Workers: {self.max_workers} (AGENTS.md Safe Limit)")
        logger.info("="*60)

        active_sessions = {}

        # Phase 1: Create sessions
        with ThreadPoolExecutor(
            max_workers=self.max_workers,
            thread_name_prefix="Create"
        ) as executor:
            futures = {
                executor.submit(create_session_fn, src): src
                for src in batch
            }

            for future in as_completed(futures):
                src = futures[future]
                repo = src.get("repo", "unknown")

                try:
                    session_id = future.result()
                    if session_id:
                        active_sessions[session_id] = {
                            "repo": repo,
                            "source": src
                        }
                        logger.info(f"   ✅ [{repo}] Session: {session_id[:20]}...")
                    else:
                        logger.warning(f"   ❌ [{repo}] Failed to create session")
                        self.increment_stat("failed")
                except Exception as e:
                    logger.error(f"   ❌ [{repo}] Error: {e}")
                    self.increment_stat("failed")

        logger.info(f"\n📊 Created {len(active_sessions)} sessions")

        if not active_sessions:
            logger.error("❌ No sessions created!")
            return {}

        # Phase 2: Poll sessions
        self._poll_all_sessions(active_sessions)

        return active_sessions

    def _poll_all_sessions(self, active_sessions: dict[str, dict]) -> None:
        """
        Poll all sessions concurrently until completion.
        """
        logger.info("\n" + "="*60)
        logger.info("🔄 PHASE 2: Polling ALL sessions concurrently...")
        logger.info("="*60)

        completed = set()
        failed = set()
        max_iterations = 1000  # Safety limit
        stuck_threshold = 50  # Iterations before analyzing stuck session

        iteration_counts = {sid: 0 for sid in active_sessions}

        for iteration in range(max_iterations):
            remaining = {
                sid: info for sid, info in active_sessions.items()
                if sid not in completed and sid not in failed
            }

            if not remaining:
                logger.info("✅ All sessions finished!")
                break

            logger.info(f"   🔄 Iteration {iteration + 1}: {len(remaining)} active")

            # Poll all remaining sessions in parallel
            with ThreadPoolExecutor(
                max_workers=self.max_workers,
                thread_name_prefix="Poll"
            ) as executor:
                futures = {
                    executor.submit(
                        self.session_manager.poll_session_once,
                        sid,
                        info["repo"]
                    ): sid
                    for sid, info in remaining.items()
                }

                for future in as_completed(futures):
                    session_id = futures[future]
                    info = remaining[session_id]
                    repo = info["repo"]

                    try:
                        status, pr_url = future.result()
                        iteration_counts[session_id] += 1

                        if status == "COMPLETED":
                            completed.add(session_id)
                            self._mark_completed(repo, pr_url)
                            logger.info(f"   ✅ [{repo}] COMPLETED → {pr_url or 'no PR'}")

                        elif status == "FAILED":
                            failed.add(session_id)
                            self._mark_failed(repo)
                            logger.warning(f"   ❌ [{repo}] FAILED")

                        elif status == "APPROVED":
                            logger.info(f"   📋 [{repo}] Plan approved")

                        elif status == "RESPONDED":
                            logger.info(f"   💬 [{repo}] Auto-responded")

                        # Check if stuck
                        elif iteration_counts[session_id] >= stuck_threshold:
                            logger.warning(f"   ⚠️ [{repo}] Appears stuck, analyzing...")
                            self._analyze_and_recover(session_id, repo)
                            iteration_counts[session_id] = 0  # Reset counter

                    except Exception as e:
                        logger.error(f"   ❌ [{repo}] Poll error: {e}")

        # Summary
        logger.info(f"\n🎉 Completed: {len(completed)} | Failed: {len(failed)}")

    def _mark_completed(self, repo: str, pr_url: str) -> None:
        """Mark repository as completed in cache."""
        self.cache.set(f"mega_processed:{repo}", {
            "status": "completed",
            "pr_url": pr_url,
            "time": self._get_timestamp()
        })
        self.increment_stat("processed")
        if pr_url:
            self.increment_stat("prs")

    def _mark_failed(self, repo: str) -> None:
        """Mark repository as failed in cache."""
        self.cache.set(f"mega_processed:{repo}", {
            "status": "failed",
            "time": self._get_timestamp()
        })
        self.increment_stat("failed")

    def _analyze_and_recover(self, session_id: str, repo: str) -> None:
        """Analyze stuck session and attempt recovery."""
        try:
            analysis = self.session_manager.analyze_stuck_session(session_id, repo)
            logger.info(f"   🔍 [{repo}] Analysis: {analysis.get('reason', 'Unknown')}")
            logger.info(f"   💡 [{repo}] Action: {analysis.get('action', 'Continue')}")

            # Take action based on analysis
            if analysis.get("status") == "recoverable":
                # Try to send a recovery message
                self.session_manager.jules.send_message(
                    session_id,
                    "Please proceed with the current approach. Auto-approve all changes."
                )
        except Exception as e:
            logger.error(f"   ❌ [{repo}] Recovery failed: {e}")

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def print_stats(self) -> None:
        """Print final statistics."""
        logger.info("\n" + "="*60)
        logger.info("📊 FINAL STATISTICS")
        logger.info("="*60)
        for k, v in self.stats.items():
            logger.info(f"   {k}: {v}")
        logger.info("="*60)