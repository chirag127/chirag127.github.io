"""
Deduplication Module - Fuzzy matching trends against existing repositories.

Uses RapidFuzz for fast string similarity matching.
Classifies trends as CREATE (new repo) or UPDATE (existing repo enhancement).
"""

import logging
from dataclasses import dataclass
from enum import Enum

from rapidfuzz import fuzz, process

from .trend_discovery.base import TrendItem

logger = logging.getLogger("Deduplication")


class TaskType(Enum):
    """Classification of trend tasks."""
    CREATE = "create"  # New repository needed
    UPDATE = "update"  # Enhancement to existing repository


@dataclass
class ClassifiedTrend:
    """A trend classified as CREATE or UPDATE task."""
    trend: TrendItem
    task_type: TaskType
    similarity_score: float
    matched_repo: str | None = None
    reason: str = ""


class TrendDeduplicator:
    """
    Deduplicates trends against existing GitHub repositories.

    Uses fuzzy matching to identify:
    - Exact/near matches -> UPDATE task
    - Novel ideas -> CREATE task
    """

    # Similarity threshold for UPDATE classification
    UPDATE_THRESHOLD = 80  # 80% similarity
    PARTIAL_MATCH_THRESHOLD = 60  # Consider but flag

    def __init__(self, similarity_threshold: int = 80):
        self.threshold = similarity_threshold

    def classify_trends(
        self,
        trends: list[TrendItem],
        existing_repos: list[dict]
    ) -> list[ClassifiedTrend]:
        """
        Classify each trend as CREATE or UPDATE.

        Args:
            trends: List of discovered trends
            existing_repos: List of existing repository dicts with 'name' and 'description'

        Returns:
            List of ClassifiedTrend objects
        """
        if not existing_repos:
            # No existing repos = all are CREATE
            return [
                ClassifiedTrend(
                    trend=t,
                    task_type=TaskType.CREATE,
                    similarity_score=0,
                    reason="No existing repositories to match"
                )
                for t in trends
            ]

        # Build search corpus from existing repos
        repo_names = [r.get("name", "") for r in existing_repos]
        repo_descriptions = [r.get("description", "") or "" for r in existing_repos]

        # Build combined lookup for matching
        repo_lookup = {
            self._normalize(r.get("name", "")): r.get("name", "")
            for r in existing_repos
        }

        classified: list[ClassifiedTrend] = []

        for trend in trends:
            classification = self._classify_single(
                trend,
                repo_names,
                repo_descriptions,
                repo_lookup
            )
            classified.append(classification)

        return classified

    def _classify_single(
        self,
        trend: TrendItem,
        repo_names: list[str],
        repo_descriptions: list[str],
        repo_lookup: dict[str, str]
    ) -> ClassifiedTrend:
        """Classify a single trend."""
        trend_title = trend.title
        trend_desc = trend.description

        # Check name similarity
        name_match = self._find_best_match(trend_title, repo_names)
        desc_match = self._find_best_match(trend_title, repo_descriptions)

        # Take best match - handle None cases
        best_score = 0.0
        matched_repo = None

        name_score = name_match[1] if name_match else 0.0
        desc_score = desc_match[1] if desc_match else 0.0

        if name_score >= desc_score and name_match:
            matched_repo = name_match[0]
            best_score = name_score
        elif desc_match:
            # Find repo with this description
            for i, desc in enumerate(repo_descriptions):
                if desc == desc_match[0]:
                    matched_repo = repo_names[i]
                    break
            best_score = desc_score

        # Classify based on score
        if best_score >= self.threshold:
            return ClassifiedTrend(
                trend=trend,
                task_type=TaskType.UPDATE,
                similarity_score=best_score,
                matched_repo=matched_repo,
                reason=f"High similarity ({best_score:.0f}%) to existing repo"
            )
        elif best_score >= self.PARTIAL_MATCH_THRESHOLD:
            # Partial match - could be related, classify as CREATE with note
            return ClassifiedTrend(
                trend=trend,
                task_type=TaskType.CREATE,
                similarity_score=best_score,
                matched_repo=matched_repo,
                reason=f"Partial match ({best_score:.0f}%) - may be related to {matched_repo}"
            )
        else:
            return ClassifiedTrend(
                trend=trend,
                task_type=TaskType.CREATE,
                similarity_score=best_score,
                reason="Novel idea - no similar existing repositories"
            )

    def _find_best_match(
        self,
        query: str,
        candidates: list[str]
    ) -> tuple[str, float] | None:
        """Find best fuzzy match from candidates."""
        if not candidates or not query:
            return None

        # Use RapidFuzz extractOne for efficiency
        result = process.extractOne(
            query,
            candidates,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=self.PARTIAL_MATCH_THRESHOLD
        )

        if result:
            return (result[0], result[1])

        return None

    def _normalize(self, text: str) -> str:
        """Normalize text for comparison."""
        return text.lower().replace("-", " ").replace("_", " ").strip()

    def get_create_tasks(
        self,
        classified: list[ClassifiedTrend]
    ) -> list[ClassifiedTrend]:
        """Filter for CREATE tasks only."""
        return [c for c in classified if c.task_type == TaskType.CREATE]

    def get_update_tasks(
        self,
        classified: list[ClassifiedTrend]
    ) -> list[ClassifiedTrend]:
        """Filter for UPDATE tasks only."""
        return [c for c in classified if c.task_type == TaskType.UPDATE]

    def print_classification_report(self, classified: list[ClassifiedTrend]) -> None:
        """Print a summary of classifications."""
        create_count = sum(1 for c in classified if c.task_type == TaskType.CREATE)
        update_count = sum(1 for c in classified if c.task_type == TaskType.UPDATE)

        logger.info("=" * 60)
        logger.info("📊 TREND CLASSIFICATION REPORT")
        logger.info("=" * 60)
        logger.info(f"   Total Trends: {len(classified)}")
        logger.info(f"   CREATE Tasks: {create_count}")
        logger.info(f"   UPDATE Tasks: {update_count}")
        logger.info("-" * 60)

        for c in classified:
            icon = "🆕" if c.task_type == TaskType.CREATE else "🔄"
            logger.info(f"   {icon} {c.trend.title[:40]:<40} | {c.task_type.value:<6} | {c.similarity_score:.0f}%")
