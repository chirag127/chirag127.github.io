"""
State Manager - Persistent Git-based state storage.

Stores state in `state/` directory which is committed to Git,
ensuring persistence across GitHub Actions runs.
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger("StateManager")


class StateManager:
    """
    Persistent state manager using Git-tracked files.

    State files are stored in `state/` directory and auto-committed
    after each run to ensure persistence across GitHub Actions.
    """

    def __init__(self, state_dir: str = "state") -> None:
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(parents=True, exist_ok=True)

        # State file paths
        self.processed_repos_file = self.state_dir / "processed_repos.json"
        self.pending_connections_file = self.state_dir / "pending_connections.json"
        self.session_history_file = self.state_dir / "session_history.json"

        # Load state from files
        self.processed_repos = self._load_json(self.processed_repos_file, {})
        self.pending_connections = self._load_json(self.pending_connections_file, {})
        self.session_history = self._load_json(self.session_history_file, [])

        logger.info(f"[StateManager] Loaded: {len(self.processed_repos)} processed, {len(self.pending_connections)} pending")

    def _load_json(self, path: Path, default: Any) -> Any:
        """Load JSON file or return default if not exists."""
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"[StateManager] Failed to load {path}: {e}")
        return default

    def _save_json(self, path: Path, data: Any) -> None:
        """Save data to JSON file."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"[StateManager] Failed to save {path}: {e}")

    def save_all(self) -> None:
        """Save all state files."""
        self._save_json(self.processed_repos_file, self.processed_repos)
        self._save_json(self.pending_connections_file, self.pending_connections)
        self._save_json(self.session_history_file, self.session_history)
        logger.info("[StateManager] All state saved to disk")

    # =========================================================================
    # Processed Repos (repos with PRs created/merged)
    # =========================================================================

    def is_processed(self, repo: str) -> bool:
        """Check if repo has been processed (PR created)."""
        return repo in self.processed_repos

    def mark_processed(
        self,
        repo: str,
        pr_url: str = "",
        status: str = "completed",
        session_id: str = ""
    ) -> None:
        """Mark a repo as processed."""
        self.processed_repos[repo] = {
            "pr_url": pr_url,
            "status": status,
            "session_id": session_id,
            "processed_at": datetime.now().isoformat(),
        }
        self._save_json(self.processed_repos_file, self.processed_repos)
        logger.info(f"[StateManager] Marked processed: {repo}")

    def update_pr_status(self, repo: str, status: str) -> None:
        """Update PR status (merged, closed, etc)."""
        if repo in self.processed_repos:
            self.processed_repos[repo]["status"] = status
            self.processed_repos[repo]["updated_at"] = datetime.now().isoformat()
            self._save_json(self.processed_repos_file, self.processed_repos)

    def get_processed_repos(self) -> dict:
        """Get all processed repos."""
        return self.processed_repos

    # =========================================================================
    # Pending Connections (repos waiting to connect to Jules)
    # =========================================================================

    def add_pending(self, repo: str, url: str, description: str = "") -> None:
        """Add a repo to pending connections."""
        self.pending_connections[repo] = {
            "url": url,
            "description": description,
            "created_at": datetime.now().isoformat(),
            "connected_to_jules": False,
        }
        self._save_json(self.pending_connections_file, self.pending_connections)

    def mark_connected(self, repo: str, session_id: str = "") -> None:
        """Mark a pending repo as connected to Jules."""
        if repo in self.pending_connections:
            self.pending_connections[repo]["connected_to_jules"] = True
            self.pending_connections[repo]["session_id"] = session_id
            self.pending_connections[repo]["connected_at"] = datetime.now().isoformat()
            self._save_json(self.pending_connections_file, self.pending_connections)

    def get_unconnected_repos(self) -> dict:
        """Get repos not yet connected to Jules."""
        return {
            k: v for k, v in self.pending_connections.items()
            if not v.get("connected_to_jules", False)
        }

    def is_pending(self, repo: str) -> bool:
        """Check if repo is pending connection."""
        return repo in self.pending_connections

    # =========================================================================
    # Session History
    # =========================================================================

    def record_session(
        self,
        repo: str,
        session_id: str,
        outcome: str,
        pr_url: str = ""
    ) -> None:
        """Record a session outcome for history."""
        self.session_history.append({
            "repo": repo,
            "session_id": session_id,
            "outcome": outcome,
            "pr_url": pr_url,
            "recorded_at": datetime.now().isoformat(),
        })
        # Keep last 1000 sessions
        if len(self.session_history) > 1000:
            self.session_history = self.session_history[-1000:]
        self._save_json(self.session_history_file, self.session_history)

    # =========================================================================
    # Git Commit & Push (for GitHub Actions persistence)
    # =========================================================================

    def commit_and_push(self, message: str = "auto: update state") -> bool:
        """Commit and push state changes to Git."""
        try:
            # Add state directory
            subprocess.run(
                ["git", "add", str(self.state_dir)],
                check=True,
                capture_output=True
            )

            # Check if there are changes to commit
            result = subprocess.run(
                ["git", "status", "--porcelain", str(self.state_dir)],
                capture_output=True,
                text=True
            )

            if not result.stdout.strip():
                logger.info("[StateManager] No state changes to commit")
                return True

            # Commit
            subprocess.run(
                ["git", "commit", "-m", message],
                check=True,
                capture_output=True
            )

            # Push
            subprocess.run(
                ["git", "push"],
                check=True,
                capture_output=True
            )

            logger.info("[StateManager] State committed and pushed to Git")
            return True

        except subprocess.CalledProcessError as e:
            logger.warning(f"[StateManager] Git operation failed: {e}")
            return False
        except Exception as e:
            logger.error(f"[StateManager] Commit failed: {e}")
            return False

    def print_status(self) -> None:
        """Print current state status."""
        print("\n" + "=" * 60)
        print("STATE MANAGER STATUS (Git-Persistent)")
        print("=" * 60)
        print(f"Processed Repos: {len(self.processed_repos)}")
        print(f"Pending Connections: {len(self.pending_connections)}")
        print(f"  - Connected: {sum(1 for v in self.pending_connections.values() if v.get('connected_to_jules'))}")
        print(f"  - Waiting: {len(self.get_unconnected_repos())}")
        print(f"Session History: {len(self.session_history)} records")
        print("=" * 60)
