"""
AI-Powered Trend Selector - Selects best 10-20 ideas from 100+ trends.

Uses top-tier AI models to evaluate trends based on:
1. Novelty (not similar to existing repos)
2. Feasibility (frontend-only implementation)
3. Market demand (trending, useful)
4. SEO potential (searchable keywords)
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from .base import TrendItem, TrendCategory


logger = logging.getLogger("TrendDiscovery.Selector")


@dataclass
class SelectedTrend:
    """A trend selected by AI for repository creation."""
    original_trend: TrendItem
    apex_name: str
    description: str
    category: str
    tags: list[str] = field(default_factory=list)
    feasibility_score: float = 0.0
    novelty_score: float = 0.0
    seo_score: float = 0.0
    reason: str = ""


class TrendSelector:
    """
    Uses AI to select the best project ideas from discovered trends.

    This is the core intelligence that decides which projects to create.
    Uses the unified AI client with automatic provider fallback.
    """

    def __init__(self, ai_client: Any = None) -> None:
        """
        Initialize the selector.

        Args:
            ai_client: UnifiedAIClient instance (creates one if not provided)
        """
        if ai_client is None:
            from ..ai import UnifiedAIClient
            self.ai = UnifiedAIClient()
        else:
            self.ai = ai_client

    def select_top_ideas(
        self,
        trends: list[TrendItem],
        count: int = 20,
        existing_repos: list[str] | None = None,
    ) -> list[SelectedTrend]:
        """
        Select the best project ideas from discovered trends.

        Args:
            trends: List of discovered TrendItems (100+)
            count: Number of ideas to select (10-20)
            existing_repos: List of existing repo names to avoid duplicates

        Returns:
            List of SelectedTrend objects with AI-generated metadata
        """
        if not trends:
            logger.warning("[Selector] No trends to select from")
            return []

        logger.info(f"[Selector] Analyzing {len(trends)} trends to select top {count}")

        # Convert TrendItems to dicts for AI processing
        trend_dicts = [
            {
                "title": t.title,
                "description": t.description,
                "source": t.source,
                "category": t.category.value,
                "popularity_score": t.popularity_score,
                "keywords": t.keywords,
                "url": t.url,
            }
            for t in trends
        ]

        # Use AI to select best ideas
        selected = self.ai.select_best_ideas(
            trends=trend_dicts,
            count=count,
            existing_repos=existing_repos,
        )

        if not selected:
            logger.warning("[Selector] AI selection returned no results, using fallback")
            return self._fallback_selection(trends, count)

        # Convert AI results to SelectedTrend objects
        results: list[SelectedTrend] = []

        for item in selected:
            original_index = item.get("original_index", 0) - 1

            # Get original trend or create placeholder
            if 0 <= original_index < len(trends):
                original = trends[original_index]
            else:
                # Create from AI data
                original = TrendItem(
                    title=item.get("title", "Unknown"),
                    description=item.get("description", ""),
                    source="ai_selected",
                    category=TrendCategory.WEB_APP,
                    popularity_score=100,
                )

            # Ensure we have 20 tags
            tags = item.get("tags", [])
            if len(tags) < 20:
                tags = self._expand_tags(tags, item.get("title", ""))

            selected_trend = SelectedTrend(
                original_trend=original,
                apex_name=item.get("apex_name", original.title),
                description=item.get("description", original.description)[:250],
                category=item.get("category", "web_app"),
                tags=tags[:20],  # Ensure exactly 20
                feasibility_score=item.get("feasibility_score", 0.8),
                novelty_score=item.get("novelty_score", 0.8),
                seo_score=item.get("seo_score", 0.8) if "seo_score" in item else 0.8,
                reason=item.get("reason", "AI selected"),
            )

            results.append(selected_trend)
            logger.info(f"   ✓ Selected: {selected_trend.apex_name}")

        logger.info(f"[Selector] Selected {len(results)} ideas")
        return results

    def _fallback_selection(
        self,
        trends: list[TrendItem],
        count: int,
    ) -> list[SelectedTrend]:
        """
        Fallback selection when AI is unavailable.

        Simply takes top-scored trends.
        """
        logger.info("[Selector] Using fallback (top-scored) selection")

        # Sort by popularity score
        sorted_trends = sorted(
            trends,
            key=lambda t: t.popularity_score,
            reverse=True
        )

        results: list[SelectedTrend] = []

        for trend in sorted_trends[:count]:
            # Generate basic APEX name
            apex_name = self._generate_apex_name(trend.title)

            # Generate tags
            tags = self._expand_tags(trend.keywords, trend.title)

            selected = SelectedTrend(
                original_trend=trend,
                apex_name=apex_name,
                description=trend.description[:250],
                category=trend.category.value,
                tags=tags,
                feasibility_score=0.7,
                novelty_score=0.7,
                seo_score=0.7,
                reason=f"High popularity score ({trend.popularity_score:.0f})",
            )

            results.append(selected)

        return results

    def _generate_apex_name(self, title: str) -> str:
        """Generate APEX-compliant repository name from title."""
        import re

        # Clean and normalize
        name = title.strip()

        # Replace special chars with hyphens
        name = re.sub(r"[^a-zA-Z0-9\s-]", "", name)
        name = re.sub(r"\s+", "-", name)
        name = re.sub(r"-+", "-", name)

        # Title case each word
        words = name.split("-")
        words = [w.capitalize() for w in words if w]

        # Limit to 3-10 words
        if len(words) < 3:
            words.extend(["App", "Tool", "Web"][:3 - len(words)])
        elif len(words) > 10:
            words = words[:10]

        return "-".join(words)[:100]  # Max 100 chars

    def _expand_tags(self, base_tags: list[str], title: str) -> list[str]:
        """Expand tags to reach 20 unique tags."""
        tags = list(set(tag.lower().replace(" ", "-") for tag in base_tags if tag))

        # Extract keywords from title
        import re
        title_words = re.findall(r"[a-zA-Z]+", title.lower())
        for word in title_words:
            if len(word) > 3 and word not in tags:
                tags.append(word)

        # Add generic tech tags
        generic = [
            "open-source", "software", "tools", "developer-tools",
            "automation", "productivity", "github", "project",
            "application", "frontend", "javascript", "typescript",
            "react", "web-development", "2025", "trending",
            "coding", "programming", "tech", "innovation",
            "github-project", "software-development", "web-app",
            "browser-extension", "library", "framework", "api",
            "developer", "code", "modern"
        ]

        for tag in generic:
            if tag not in tags and len(tags) < 20:
                tags.append(tag)

        return tags[:20]

    def enrich_with_metadata(
        self,
        trends: list[SelectedTrend],
    ) -> list[SelectedTrend]:
        """
        Enrich selected trends with AI-generated metadata.

        Adds detailed descriptions, features, and README content.
        """
        logger.info(f"[Selector] Enriching {len(trends)} trends with AI metadata")

        enriched: list[SelectedTrend] = []

        for trend in trends:
            metadata = self.ai.generate_repo_metadata(
                idea=trend.apex_name,
                description=trend.description,
                category=trend.category,
            )

            if metadata:
                # Update with enriched data
                trend.apex_name = metadata.get("apex_name", trend.apex_name)
                trend.description = metadata.get("description", trend.description)
                trend.tags = metadata.get("tags", trend.tags)[:20]

            enriched.append(trend)

        return enriched
