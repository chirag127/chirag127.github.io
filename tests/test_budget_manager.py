"""
Tests for budget manager module.
"""

import json
import os
import tempfile
from datetime import date
from pathlib import Path

import pytest

from apex_optimizer.budget_manager import BudgetManager, BudgetState


class TestBudgetState:
    """Tests for BudgetState dataclass."""

    def test_create_budget_state(self):
        """Test creating a BudgetState."""
        state = BudgetState(date="2024-01-15")

        assert state.date == "2024-01-15"
        assert state.total_limit == 100
        assert state.sessions_used == 0
        assert state.remaining == 100

    def test_remaining_calculation(self):
        """Test remaining sessions calculation."""
        state = BudgetState(date="2024-01-15", sessions_used=30)

        assert state.remaining == 70

    def test_to_dict(self):
        """Test serialization to dict."""
        state = BudgetState(date="2024-01-15", sessions_used=10)

        data = state.to_dict()

        assert data["date"] == "2024-01-15"
        assert data["sessions_used"] == 10

    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "date": "2024-01-15",
            "total_limit": 100,
            "sessions_used": 25,
            "new_repo_sessions": 10,
            "optimization_sessions": 15,
            "session_log": [],
        }

        state = BudgetState.from_dict(data)

        assert state.sessions_used == 25
        assert state.new_repo_sessions == 10


class TestBudgetManager:
    """Tests for BudgetManager class."""

    @pytest.fixture
    def temp_state_file(self):
        """Create a temporary state file for testing."""
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)  # Close the file descriptor
        yield path
        # Cleanup
        try:
            os.unlink(path)
        except (OSError, PermissionError):
            pass

    def test_create_new_state_for_today(self, temp_state_file):
        """Test creating new state for today."""
        manager = BudgetManager(state_file=temp_state_file)

        assert manager.state.date == date.today().isoformat()
        assert manager.state.sessions_used == 0

    def test_can_create_session_within_budget(self, temp_state_file):
        """Test can create session when budget available."""
        manager = BudgetManager(state_file=temp_state_file)

        assert manager.can_create_session("new_repo") is True
        assert manager.can_create_session("optimization") is True

    def test_cannot_create_when_exhausted(self, temp_state_file):
        """Test cannot create session when budget exhausted."""
        manager = BudgetManager(state_file=temp_state_file)
        manager.state.new_repo_sessions = 15  # Max allocation

        assert manager.can_create_session("new_repo") is False
        assert manager.can_create_session("optimization") is True

    def test_consume_session(self, temp_state_file):
        """Test consuming a session."""
        manager = BudgetManager(state_file=temp_state_file)

        result = manager.consume_session("new_repo", "test-repo", "session-123")

        assert result is True
        assert manager.state.sessions_used == 1
        assert manager.state.new_repo_sessions == 1
        assert len(manager.state.session_log) == 1

    def test_get_allocation(self, temp_state_file):
        """Test getting allocation status."""
        manager = BudgetManager(state_file=temp_state_file)
        manager.consume_session("new_repo", "repo1")
        manager.consume_session("optimization", "repo2")

        alloc = manager.get_allocation()

        assert alloc["sessions_used"] == 2
        assert alloc["new_repo"]["used"] == 1
        assert alloc["optimization"]["used"] == 1

    def test_persistence(self, temp_state_file):
        """Test state persists across manager instances."""
        # First manager
        manager1 = BudgetManager(state_file=temp_state_file)
        manager1.consume_session("new_repo", "repo1")

        # Second manager (loads from file)
        manager2 = BudgetManager(state_file=temp_state_file)

        assert manager2.state.sessions_used == 1

    def test_hard_stop_enforcement(self, temp_state_file):
        """Test hard stop when budget exhausted."""
        manager = BudgetManager(state_file=temp_state_file)
        manager.state.sessions_used = 100

        assert manager.enforce_hard_stop() is True
