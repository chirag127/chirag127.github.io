"""
Trend Aggregator - Combines and ranks trends from all sources.

Handles parallel fetching, deduplication, and scoring.
All API sources are OPTIONAL - graceful degradation if keys not provided.
"""

import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass

from .base import TrendItem, TrendSource

# Unified Sources Import
from .sources import (
    ArxivSource, PapersWithCodeSource, SemanticScholarSource,
    DevToSource, GitHubTrendingSource, HackerNewsSource,
    HashnodeSource, LobstersSource, RedditSource, StackOverflowSource,
    HuggingFaceSource, KaggleSource, NewsAPISource,
    ProductHuntSource, TechCrunchRSSSource
)

logger = logging.getLogger("TrendDiscovery.Aggregator")


@dataclass
class AggregatorConfig:
    """Configuration for trend aggregation.

    Updated for comprehensive discovery (Dec 2025):
    - 20 trends per source = 300+ raw topics
    - 150 total after deduplication = 100+ unique ideas
    """
    max_trends_per_source: int = 20  # Increased from 10
    total_limit: int = 150  # Increased from 50 for 100+ topics
    parallel_fetch: bool = True
    timeout: int = 45  # Increased for stability


class TrendAggregator:
    """
    Aggregates trends from multiple sources with intelligent ranking.

    Features:
    - Parallel fetching from all sources
    - Cross-source deduplication
    - Weighted scoring based on source reliability and novelty
    - Category-based grouping
    - Graceful degradation for optional sources
    """

    # Source weights for scoring (higher = more trusted/novel)
    SOURCE_WEIGHTS = {
        # Research Papers (Highest - Future Trends)
        "semantic_scholar": 2.0,
        "arxiv": 2.0,
        "paperswithcode": 1.8,
        # AI/ML Platforms (High)
        "huggingface": 1.7,
        "kaggle": 1.5,
        # Pre-Trend Signals (Medium-High)
        "producthunt": 1.5,
        "newsapi": 1.4,
        "techcrunch": 1.3,
        # Tech Community (Medium)
        "github": 1.5,
        "hackernews": 1.3,
        "lobsters": 1.2,
        "devto": 1.1,
        "hashnode": 1.0,
        # General (Lower)
        "reddit": 1.0,
        "stackoverflow": 0.8,
    }

    def __init__(self, config: AggregatorConfig | None = None):
        self.config = config or AggregatorConfig()
        self.sources = self._initialize_sources()

        enabled_count = sum(1 for s in self.sources if getattr(s, 'enabled', True))
        logger.info(f"   🔌 TrendAggregator: {enabled_count}/{len(self.sources)} sources enabled")

    def _initialize_sources(self) -> list[TrendSource]:
        """Initialize all sources with graceful optional handling."""
        timeout = self.config.timeout

        sources = [
            # === Research Paper Sources (No Keys Required) ===
            SemanticScholarSource(timeout=timeout),
            ArxivSource(timeout=timeout),
            PapersWithCodeSource(timeout=timeout),

            # === AI/ML Platform Sources (Optional Keys) ===
            HuggingFaceSource(timeout=timeout),
            KaggleSource(timeout=timeout),

            # === Pre-Trend Signal Sources (Optional Keys) ===
            ProductHuntSource(timeout=timeout),

            # === News Sources (Mixed) ===
            NewsAPISource(timeout=timeout),
            TechCrunchRSSSource(timeout=timeout),

            # === Tech Community Sources (No Keys Required) ===
            GitHubTrendingSource(timeout=timeout),
            HackerNewsSource(timeout=timeout),
            LobstersSource(timeout=timeout),
            RedditSource(timeout=timeout),
            DevToSource(timeout=timeout),
            HashnodeSource(timeout=timeout),
            StackOverflowSource(timeout=timeout),
        ]

        return sources

    def fetch_all_trends(self) -> list[TrendItem]:
        """
        Fetch trends from all sources and aggregate.

        Returns:
            Deduplicated, ranked list of TrendItems
        """
        logger.info("🔍 Fetching trends from all sources...")

        all_trends: list[TrendItem] = []

        if self.config.parallel_fetch:
            all_trends = self._fetch_parallel()
        else:
            all_trends = self._fetch_sequential()

        logger.info(f"📊 Collected {len(all_trends)} raw trends")

        # Deduplicate
        unique_trends = self._deduplicate(all_trends)
        logger.info(f"🧹 After deduplication: {len(unique_trends)} trends")

        # Apply source weights and sort
        weighted_trends = self._apply_weights(unique_trends)
        weighted_trends.sort(key=lambda x: x.popularity_score, reverse=True)

        return weighted_trends[:self.config.total_limit]

    def _fetch_parallel(self) -> list[TrendItem]:
        """Fetch from all sources in parallel."""
        all_trends: list[TrendItem] = []

        # Filter to only enabled sources
        enabled_sources = [s for s in self.sources if getattr(s, 'enabled', True)]

        with ThreadPoolExecutor(max_workers=min(12, len(enabled_sources))) as executor:
            futures = {
                executor.submit(
                    source.fetch_trends,
                    self.config.max_trends_per_source
                ): source.name
                for source in enabled_sources
            }

            for future in as_completed(futures):
                source_name = futures[future]
                try:
                    trends = future.result()
                    all_trends.extend(trends)
                    if trends:
                        logger.info(f"   ✅ {source_name}: {len(trends)} trends")
                except Exception as e:
                    logger.warning(f"   ❌ {source_name}: {e}")

        return all_trends

    def _fetch_sequential(self) -> list[TrendItem]:
        """Fetch from all sources sequentially."""
        all_trends: list[TrendItem] = []

        for source in self.sources:
            if not getattr(source, 'enabled', True):
                continue

            try:
                trends = source.fetch_trends(self.config.max_trends_per_source)
                all_trends.extend(trends)
                if trends:
                    logger.info(f"   ✅ {source.name}: {len(trends)} trends")
            except Exception as e:
                logger.warning(f"   ❌ {source.name}: {e}")

        return all_trends

    def _deduplicate(self, trends: list[TrendItem]) -> list[TrendItem]:
        """Remove duplicate trends based on title similarity."""
        seen_titles: dict[str, TrendItem] = {}

        for trend in trends:
            normalized = self._normalize_title(trend.title)

            if normalized not in seen_titles:
                seen_titles[normalized] = trend
            else:
                # Keep the one with higher score
                existing = seen_titles[normalized]
                if trend.popularity_score > existing.popularity_score:
                    seen_titles[normalized] = trend

        return list(seen_titles.values())

    def _normalize_title(self, title: str) -> str:
        """Normalize title for deduplication comparison."""
        normalized = title.lower().strip()

        # Remove common suffixes
        suffixes = [
            "-tool", "-cli", "-app", "-web", "-extension",
            "-implementation", "-api", "-sdk", "-lib", "-library",
            "-ai-model", "-llm-implementation", "-dataset-analysis-tool",
        ]
        for suffix in suffixes:
            if normalized.endswith(suffix):
                normalized = normalized[:-len(suffix)]

        # Remove non-alphanumeric for comparison
        normalized = "".join(c for c in normalized if c.isalnum())

        return normalized

    def _apply_weights(self, trends: list[TrendItem]) -> list[TrendItem]:
        """Apply source-specific weights to scores."""
        for trend in trends:
            weight = self.SOURCE_WEIGHTS.get(trend.source, 1.0)
            trend.popularity_score *= weight

        return trends

    def get_top_trends(self, limit: int = 10) -> list[TrendItem]:
        """Get top N trends after aggregation."""
        all_trends = self.fetch_all_trends()
        return all_trends[:limit]

    def get_trends_by_category(self) -> dict[str, list[TrendItem]]:
        """Group trends by category."""
        all_trends = self.fetch_all_trends()

        by_category: dict[str, list[TrendItem]] = {}
        for trend in all_trends:
            category = trend.category.value
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(trend)

        return by_category

    def get_source_status(self) -> dict[str, bool]:
        """Get enabled/disabled status of all sources."""
        return {
            source.name: getattr(source, 'enabled', True)
            for source in self.sources
        }
