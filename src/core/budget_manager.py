"""
Budget Manager - Enforces strict 100 session/day limit for Jules API.

Features:
- Hard budget enforcement
- Dynamic allocation (new repos vs optimization)
- Persistence across runs
- Consumption tracking
"""

import json
import logging
from dataclasses import asdict, dataclass, field
from datetime import date, datetime
from pathlib import Path

logger = logging.getLogger("BudgetManager")


@dataclass
class BudgetState:
    """Persistent budget state."""
    date: str  # YYYY-MM-DD
    total_limit: int = 100
    sessions_used: int = 0
    new_repo_sessions: int = 0
    optimization_sessions: int = 0
    session_log: list[dict] = field(default_factory=list)

    @property
    def remaining(self) -> int:
        return max(0, self.total_limit - self.sessions_used)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "BudgetState":
        return cls(**data)


class BudgetManager:
    """
    Manages Jules session budget with strict enforcement.

    Allocation strategy:
    - 10-15 sessions reserved for new trending repos (high priority)
    - Remaining 85-90 sessions for optimization (low priority)
    """

    DAILY_LIMIT = 100
    NEW_REPO_ALLOCATION = 10  # Max sessions for new repos (10%)
    OPTIMIZATION_ALLOCATION = 90  # Max sessions for optimization (90%)

    def __init__(self, state_file: str | Path | None = None):
        self.state_file = Path(state_file) if state_file else Path("budget_state.json")
        self.state = self._load_or_create_state()

    def _load_or_create_state(self) -> BudgetState:
        """Load existing state or create new for today."""
        today = date.today().isoformat()

        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    data = json.load(f)

                state = BudgetState.from_dict(data)

                # Check if it's a new day
                if state.date != today:
                    logger.info(f"🌅 New day detected. Resetting budget from {state.date}")
                    return BudgetState(date=today)

                logger.info(f"📊 Loaded budget state: {state.sessions_used}/{state.total_limit} used")
                return state

            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Failed to load budget state: {e}")

        return BudgetState(date=today)

    def _save_state(self) -> None:
        """Persist budget state to file."""
        try:
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state.to_dict(), f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save budget state: {e}")

    def can_create_session(self, task_type: str = "optimization") -> bool:
        """
        Check if budget allows creating a session.

        Args:
            task_type: "new_repo" or "optimization"
        """
        if self.state.remaining <= 0:
            return False

        if task_type == "new_repo":
            return self.state.new_repo_sessions < self.NEW_REPO_ALLOCATION
        else:
            return self.state.optimization_sessions < self.OPTIMIZATION_ALLOCATION

    def consume_session(
        self,
        task_type: str,
        repo: str,
        session_id: str | None = None
    ) -> bool:
        """
        Consume one session from budget.

        Args:
            task_type: "new_repo" or "optimization"
            repo: Repository name
            session_id: Jules session ID (optional)

        Returns:
            True if consumed, False if budget exhausted
        """
        if not self.can_create_session(task_type):
            logger.warning(f"❌ Budget exhausted for {task_type} tasks")
            return False

        self.state.sessions_used += 1

        if task_type == "new_repo":
            self.state.new_repo_sessions += 1
        else:
            self.state.optimization_sessions += 1

        # Log session
        self.state.session_log.append({
            "type": task_type,
            "repo": repo,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
        })

        self._save_state()

        logger.info(
            f"📉 Session consumed: {self.state.sessions_used}/{self.DAILY_LIMIT} "
            f"(New: {self.state.new_repo_sessions}, Opt: {self.state.optimization_sessions})"
        )

        return True

    def get_allocation(self) -> dict:
        """Get current allocation status."""
        return {
            "date": self.state.date,
            "total_limit": self.DAILY_LIMIT,
            "sessions_used": self.state.sessions_used,
            "remaining": self.state.remaining,
            "new_repo": {
                "used": self.state.new_repo_sessions,
                "allocated": self.NEW_REPO_ALLOCATION,
                "available": self.NEW_REPO_ALLOCATION - self.state.new_repo_sessions,
            },
            "optimization": {
                "used": self.state.optimization_sessions,
                "allocated": self.OPTIMIZATION_ALLOCATION,
                "available": self.OPTIMIZATION_ALLOCATION - self.state.optimization_sessions,
            },
        }

    def get_remaining_for_new_repos(self) -> int:
        """Get remaining sessions for new repo creation."""
        return max(0, self.NEW_REPO_ALLOCATION - self.state.new_repo_sessions)

    def get_remaining_for_optimization(self) -> int:
        """Get remaining sessions for optimization."""
        return max(0, self.OPTIMIZATION_ALLOCATION - self.state.optimization_sessions)

    def print_status(self) -> None:
        """Print current budget status."""
        alloc = self.get_allocation()

        logger.info("=" * 60)
        logger.info("📊 BUDGET STATUS")
        logger.info("=" * 60)
        logger.info(f"   Date: {alloc['date']}")
        logger.info(f"   Total: {alloc['sessions_used']}/{alloc['total_limit']} used")
        logger.info(f"   Remaining: {alloc['remaining']} sessions")
        logger.info("-" * 60)
        logger.info(f"   New Repos: {alloc['new_repo']['used']}/{alloc['new_repo']['allocated']}")
        logger.info(f"   Optimization: {alloc['optimization']['used']}/{alloc['optimization']['allocated']}")
        logger.info("=" * 60)

    def enforce_hard_stop(self) -> bool:
        """Check if hard stop should be enforced."""
        if self.state.remaining <= 0:
            logger.warning("🛑 HARD STOP: Daily session limit reached (100/100)")
            return True
        return False
