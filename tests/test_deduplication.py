"""
Tests for deduplication module.
"""

import pytest

from apex_optimizer.deduplication import ClassifiedTrend, TaskType, TrendDeduplicator
from apex_optimizer.trend_discovery.base import TrendItem


class TestTrendDeduplicator:
    """Tests for TrendDeduplicator class."""

    def test_classify_all_create_when_no_repos(self):
        """All trends should be CREATE when no existing repos."""
        deduplicator = TrendDeduplicator()

        trends = [
            TrendItem(title="New Tool", description="", source="github", url=""),
            TrendItem(title="Another Tool", description="", source="hackernews", url=""),
        ]

        classified = deduplicator.classify_trends(trends, existing_repos=[])

        assert len(classified) == 2
        assert all(c.task_type == TaskType.CREATE for c in classified)

    def test_classify_exact_match_as_update(self):
        """Exact match should be classified as UPDATE."""
        deduplicator = TrendDeduplicator()

        trends = [
            TrendItem(title="My-Existing-Tool", description="", source="github", url=""),
        ]

        existing_repos = [
            {"name": "My-Existing-Tool", "description": "An existing tool"},
        ]

        classified = deduplicator.classify_trends(trends, existing_repos)

        assert len(classified) == 1
        assert classified[0].task_type == TaskType.UPDATE
        assert classified[0].similarity_score >= 80

    def test_classify_similar_as_partial_match(self):
        """Similar names should be detected as related."""
        deduplicator = TrendDeduplicator()

        trends = [
            TrendItem(title="My Existing Tool", description="", source="github", url=""),
        ]

        existing_repos = [
            {"name": "My-Existing-Tool", "description": ""},
        ]

        classified = deduplicator.classify_trends(trends, existing_repos)

        # "My Existing Tool" vs "My-Existing-Tool" should have good similarity
        # Depending on exact score, could be UPDATE or CREATE with partial match note
        assert classified[0].similarity_score >= 60  # Should detect as related

    def test_classify_different_as_create(self):
        """Different names should be classified as CREATE."""
        deduplicator = TrendDeduplicator()

        trends = [
            TrendItem(title="Brand New Unique Idea", description="", source="github", url=""),
        ]

        existing_repos = [
            {"name": "Completely-Different-Repo", "description": "Something else"},
        ]

        classified = deduplicator.classify_trends(trends, existing_repos)

        assert classified[0].task_type == TaskType.CREATE

    def test_get_create_tasks(self):
        """Test filtering for CREATE tasks."""
        deduplicator = TrendDeduplicator()

        classified = [
            ClassifiedTrend(
                trend=TrendItem(title="New", description="", source="", url=""),
                task_type=TaskType.CREATE,
                similarity_score=0,
            ),
            ClassifiedTrend(
                trend=TrendItem(title="Update", description="", source="", url=""),
                task_type=TaskType.UPDATE,
                similarity_score=85,
            ),
        ]

        create_tasks = deduplicator.get_create_tasks(classified)

        assert len(create_tasks) == 1
        assert create_tasks[0].trend.title == "New"

    def test_get_update_tasks(self):
        """Test filtering for UPDATE tasks."""
        deduplicator = TrendDeduplicator()

        classified = [
            ClassifiedTrend(
                trend=TrendItem(title="New", description="", source="", url=""),
                task_type=TaskType.CREATE,
                similarity_score=0,
            ),
            ClassifiedTrend(
                trend=TrendItem(title="Update", description="", source="", url=""),
                task_type=TaskType.UPDATE,
                similarity_score=85,
            ),
        ]

        update_tasks = deduplicator.get_update_tasks(classified)

        assert len(update_tasks) == 1
        assert update_tasks[0].trend.title == "Update"


class TestTaskType:
    """Tests for TaskType enum."""

    def test_task_types_exist(self):
        """Test task types exist."""
        assert TaskType.CREATE.value == "create"
        assert TaskType.UPDATE.value == "update"
