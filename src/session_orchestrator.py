"""
Session Orchestrator - Comprehensive automated session management system.

Maximizes parallel Jules sessions while staying within 100/day limit.
Features:
- Intelligent session queue with quota management
- Real-time monitoring and health checks
- Automatic recovery and optimization
- PR tracking and validation
- Adaptive rate limiting
"""

import logging
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

from .clients.jules import JulesClient
from .session_manager import SessionManager

logger = logging.getLogger("SessionOrchestrator")


class SessionState(Enum):
    """Session states for tracking."""
    QUEUED = "queued"
    CREATING = "creating"
    ACTIVE = "active"
    WORKING = "working"
    STUCK = "stuck"
    COMPLETING = "completing"
    COMPLETED = "completed"
    FAILED = "failed"
    RECOVERING = "recovering"


class SessionPriority(Enum):
    """Priority levels for session creation."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


@dataclass
class SessionInfo:
    """Comprehensive session information."""
    session_id: str
    repo: str
    source: dict
    state: SessionState
    priority: SessionPriority
    created_at: datetime
    last_activity: datetime
    error_count: int = 0
    retry_count: int = 0
    pr_url: str = ""
    health_score: float = 100.0
    stuck_iterations: int = 0
    metadata: dict = field(default_factory=dict)


@dataclass
class QuotaManager:
    """Manages daily session quota (100 sessions/day)."""
    daily_limit: int = 100
    sessions_today: int = 0
    session_date: datetime = field(default_factory=lambda: datetime.now().date())
    reserved_quota: int = 10  # Reserve for high-priority tasks

    def reset_if_new_day(self) -> None:
        """Reset counter if it's a new day."""
        today = datetime.now().date()
        if today > self.session_date:
            logger.info(f"🌅 New day - resetting quota (used {self.sessions_today}/{self.daily_limit})")
            self.sessions_today = 0
            self.session_date = today

    def can_create_session(self, priority: SessionPriority = SessionPriority.NORMAL) -> bool:
        """Check if we can create a new session."""
        self.reset_if_new_day()

        # Critical/High priority can use reserved quota
        if priority in [SessionPriority.CRITICAL, SessionPriority.HIGH]:
            return self.sessions_today < self.daily_limit

        # Normal/Low priority respects reserved quota
        return self.sessions_today < (self.daily_limit - self.reserved_quota)

    def consume_quota(self) -> bool:
        """Consume one session from quota."""
        self.reset_if_new_day()
        if self.sessions_today < self.daily_limit:
            self.sessions_today += 1
            return True
        return False

    def get_remaining(self) -> int:
        """Get remaining quota for today."""
        self.reset_if_new_day()
        return self.daily_limit - self.sessions_today

    def get_optimal_batch_size(self) -> int:
        """Calculate optimal batch size based on remaining quota and time."""
        remaining = self.get_remaining()
        now = datetime.now()
        hours_left = 24 - now.hour

        if hours_left <= 0:
            hours_left = 1

        # Distribute remaining quota across remaining hours
        optimal = max(1, remaining // hours_left)

        # Cap at 20 for safety
        return min(optimal, 20)


class SessionOrchestrator:
    """
    Comprehensive session management system.

    Maximizes parallel sessions while respecting rate limits and quota.
    """

    def __init__(
        self,
        jules: JulesClient,
        session_manager: SessionManager,
        max_parallel: int = 20,  # Max parallel sessions
        monitor_interval: int = 300,  # 5 minutes
        stuck_threshold: int = 10  # Iterations before stuck
    ) -> None:
        self.jules = jules
        self.session_manager = session_manager
        self.max_parallel = max_parallel
        self.monitor_interval = monitor_interval
        self.stuck_threshold = stuck_threshold

        # Session tracking
        self.sessions: dict[str, SessionInfo] = {}
        self.session_queue: deque = deque()  # Priority queue
        self._lock = threading.Lock()

        # Quota management
        self.quota = QuotaManager()

        # Monitoring
        self.monitor_thread = None
        self.running = False

        # Statistics
        self.stats = {
            "total_created": 0,
            "total_completed": 0,
            "total_failed": 0,
            "total_recovered": 0,
            "prs_created": 0,
            "avg_completion_time": 0.0
        }

    def add_to_queue(
        self,
        repo: str,
        source: dict,
        priority: SessionPriority = SessionPriority.NORMAL
    ) -> None:
        """Add a repository to the session creation queue."""
        with self._lock:
            # Check if already queued or active
            for session in self.sessions.values():
                if session.repo == repo:
                    logger.debug(f"   ⏭️ [{repo}] Already in system")
                    return

            # Add to queue with priority
            self.session_queue.append({
                "repo": repo,
                "source": source,
                "priority": priority,
                "queued_at": datetime.now()
            })

            logger.info(f"   📥 [{repo}] Added to queue (Priority: {priority.name})")

    def _sort_queue_by_priority(self) -> None:
        """Sort queue by priority."""
        with self._lock:
            self.session_queue = deque(
                sorted(
                    self.session_queue,
                    key=lambda x: x["priority"].value
                )
            )

    def _get_active_session_count(self) -> int:
        """Get count of active sessions."""
        with self._lock:
            return sum(
                1 for s in self.sessions.values()
                if s.state in [SessionState.ACTIVE, SessionState.WORKING, SessionState.CREATING]
            )

    def _create_session_from_queue(self) -> bool:
        """Create a session from the queue if possible."""
        # Check if we can create more sessions
        active_count = self._get_active_session_count()
        if active_count >= self.max_parallel:
            return False

        # Get next item from queue
        with self._lock:
            if not self.session_queue:
                return False

            item = self.session_queue.popleft()

        repo = item["repo"]
        source = item["source"]
        priority = item["priority"]

        # Check quota
        if not self.quota.can_create_session(priority):
            logger.warning(f"   📅 [{repo}] Quota exhausted, re-queuing")
            with self._lock:
                self.session_queue.appendleft(item)
            return False

        # Create session
        logger.info(f"   🚀 [{repo}] Creating session (Priority: {priority.name})")

        try:
            # This should call the actual session creation logic
            session_id = self._create_session_impl(repo, source)

            if session_id:
                self.quota.consume_quota()

                # Track session
                session_info = SessionInfo(
                    session_id=session_id,
                    repo=repo,
                    source=source,
                    state=SessionState.ACTIVE,
                    priority=priority,
                    created_at=datetime.now(),
                    last_activity=datetime.now()
                )

                with self._lock:
                    self.sessions[session_id] = session_info
                    self.stats["total_created"] += 1

                logger.info(f"   ✅ [{repo}] Session created: {session_id[:20]}...")
                return True
            else:
                logger.warning(f"   ❌ [{repo}] Session creation failed")
                return False

        except Exception as e:
            logger.error(f"   ❌ [{repo}] Creation error: {e}")
            return False

    def _create_session_impl(self, repo: str, source: dict) -> str | None:
        """
        Actual session creation implementation.
        This should be overridden or injected.
        """
        # Placeholder - should call actual creation logic
        source_name = source.get("name", "")
        return self.session_manager.create_session(
            source_name=source_name,
            prompt=f"Optimize {repo} according to AGENTS.md",
            title=f"AGENTS.md: {repo}",
            repo=repo
        )

    def _monitor_sessions(self) -> None:
        """Monitor all active sessions and update their state."""
        logger.info("🔍 Monitoring active sessions...")

        with self._lock:
            active_sessions = [
                (sid, info) for sid, info in self.sessions.items()
                if info.state in [SessionState.ACTIVE, SessionState.WORKING, SessionState.STUCK]
            ]

        if not active_sessions:
            logger.info("   ℹ️  No active sessions to monitor")
            return

        logger.info(f"   📊 Monitoring {len(active_sessions)} active sessions")

        for session_id, info in active_sessions:
            try:
                status, pr_url = self.session_manager.poll_session_once(
                    session_id, info.repo
                )

                # Update session info
                with self._lock:
                    if session_id not in self.sessions:
                        continue

                    session = self.sessions[session_id]
                    session.last_activity = datetime.now()

                    if status == "COMPLETED":
                        session.state = SessionState.COMPLETED
                        session.pr_url = pr_url
                        self.stats["total_completed"] += 1
                        if pr_url:
                            self.stats["prs_created"] += 1
                        logger.info(f"   ✅ [{info.repo}] COMPLETED → {pr_url or 'no PR'}")

                    elif status == "FAILED":
                        session.state = SessionState.FAILED
                        self.stats["total_failed"] += 1
                        logger.warning(f"   ❌ [{info.repo}] FAILED")

                    elif status == "WORKING":
                        session.state = SessionState.WORKING
                        session.stuck_iterations = 0

                    elif status == "APPROVED" or status == "RESPONDED":
                        session.last_activity = datetime.now()
                        session.stuck_iterations = 0

                    # Check if stuck
                    time_since_activity = (datetime.now() - session.last_activity).total_seconds()
                    if time_since_activity > 600:  # 10 minutes
                        session.stuck_iterations += 1
                        if session.stuck_iterations >= self.stuck_threshold:
                            session.state = SessionState.STUCK
                            logger.warning(f"   ⚠️ [{info.repo}] Session appears STUCK")
                            self._recover_stuck_session(session_id)

            except Exception as e:
                logger.error(f"   ❌ [{info.repo}] Monitor error: {e}")

    def _recover_stuck_session(self, session_id: str) -> None:
        """Attempt to recover a stuck session."""
        with self._lock:
            if session_id not in self.sessions:
                return

            session = self.sessions[session_id]
            session.state = SessionState.RECOVERING

        logger.info(f"   🔧 [{session.repo}] Attempting recovery...")

        try:
            # Analyze stuck session
            analysis = self.session_manager.analyze_stuck_session(
                session_id, session.repo
            )

            logger.info(f"   🔍 [{session.repo}] Analysis: {analysis.get('reason', 'Unknown')}")

            if analysis.get("status") == "recoverable":
                # Try to send recovery message
                self.jules.send_message(
                    session_id,
                    "Please proceed immediately. Auto-approve all changes. Use first approach."
                )

                with self._lock:
                    session.state = SessionState.ACTIVE
                    session.stuck_iterations = 0
                    session.last_activity = datetime.now()
                    self.stats["total_recovered"] += 1

                logger.info(f"   ✅ [{session.repo}] Recovery attempted")
            else:
                # Mark as failed
                with self._lock:
                    session.state = SessionState.FAILED
                    self.stats["total_failed"] += 1

                logger.warning(f"   ❌ [{session.repo}] Recovery not possible")

        except Exception as e:
            logger.error(f"   ❌ [{session.repo}] Recovery error: {e}")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop."""
        logger.info("🎬 Starting monitoring loop...")

        while self.running:
            try:
                # Monitor existing sessions
                self._monitor_sessions()

                # Create new sessions from queue
                created_count = 0
                while created_count < 5:  # Create up to 5 per cycle
                    if self._create_session_from_queue():
                        created_count += 1
                    else:
                        break

                # Print status
                self._print_status()

                # Sleep until next cycle
                time.sleep(self.monitor_interval)

            except Exception as e:
                logger.error(f"   ❌ Monitoring loop error: {e}")
                time.sleep(60)  # Wait a minute before retrying

    def _print_status(self) -> None:
        """Print current status."""
        with self._lock:
            active = sum(1 for s in self.sessions.values() if s.state == SessionState.ACTIVE)
            working = sum(1 for s in self.sessions.values() if s.state == SessionState.WORKING)
            stuck = sum(1 for s in self.sessions.values() if s.state == SessionState.STUCK)
            completed = sum(1 for s in self.sessions.values() if s.state == SessionState.COMPLETED)
            failed = sum(1 for s in self.sessions.values() if s.state == SessionState.FAILED)
            queued = len(self.session_queue)

        logger.info("\n" + "="*70)
        logger.info("📊 SESSION ORCHESTRATOR STATUS")
        logger.info("="*70)
        logger.info(f"   Quota: {self.quota.sessions_today}/{self.quota.daily_limit} used")
        logger.info(f"   Remaining: {self.quota.get_remaining()} sessions")
        logger.info(f"   Queued: {queued}")
        logger.info(f"   Active: {active}")
        logger.info(f"   Working: {working}")
        logger.info(f"   Stuck: {stuck}")
        logger.info(f"   Completed: {completed}")
        logger.info(f"   Failed: {failed}")
        logger.info(f"   PRs Created: {self.stats['prs_created']}")
        logger.info("="*70)

    def start(self) -> None:
        """Start the orchestrator."""
        if self.running:
            logger.warning("Orchestrator already running")
            return

        self.running = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True,
            name="SessionMonitor"
        )
        self.monitor_thread.start()
        logger.info("✅ Session Orchestrator started")

    def stop(self) -> None:
        """Stop the orchestrator."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=10)
        logger.info("🛑 Session Orchestrator stopped")

    def get_dashboard_data(self) -> dict:
        """Get data for dashboard display."""
        with self._lock:
            return {
                "quota": {
                    "used": self.quota.sessions_today,
                    "limit": self.quota.daily_limit,
                    "remaining": self.quota.get_remaining()
                },
                "sessions": {
                    "total": len(self.sessions),
                    "active": sum(1 for s in self.sessions.values() if s.state == SessionState.ACTIVE),
                    "working": sum(1 for s in self.sessions.values() if s.state == SessionState.WORKING),
                    "stuck": sum(1 for s in self.sessions.values() if s.state == SessionState.STUCK),
                    "completed": sum(1 for s in self.sessions.values() if s.state == SessionState.COMPLETED),
                    "failed": sum(1 for s in self.sessions.values() if s.state == SessionState.FAILED),
                    "queued": len(self.session_queue)
                },
                "stats": self.stats.copy()
            }