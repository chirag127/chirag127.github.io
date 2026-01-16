"""
SearXNG Trend Discovery Source.

Uses comprehensive SearXNG client to discover profitable, frontend-only tool ideas.
"""

import logging
from datetime import datetime
from typing import Any

from ..clients.searxng import get_searxng_client
from .base import BaseTrendSource, DiscoveredTrend

logger = logging.getLogger("TrendDiscovery.SearXNG")


class SearXNGTrendSource(BaseTrendSource):
    """
    Trend discovery using SearXNG for comprehensive market research.

    Focuses on:
    - Profitable tools with high traffic
    - Frontend-only projects (no backend needed)
    - Tools with SEO potential
    - Underserved niches with demand
    """

    SOURCE_NAME = "searxng"

    # Categories to search
    TOOL_CATEGORIES = [
        "pdf",
        "image",
        "video",
        "audio",
        "text",
        "converter",
        "generator",
        "compress",
        "editor",
        "downloader",
        "qr code",
        "password",
        "json",
        "markdown",
        "calculator",
    ]

    def __init__(self) -> None:
        super().__init__()
        self.client = get_searxng_client()

    def fetch_trends(self, limit: int = 30) -> list[DiscoveredTrend]:
        """
        Fetch profitable, frontend-only tool ideas.

        Uses multiple search strategies for comprehensive discovery.
        """
        if not self.client.is_available():
            logger.warning(f"⚠️ {self.SOURCE_NAME}: Service unavailable")
            return []

        all_trends: list[DiscoveredTrend] = []

        # Strategy 1: Find profitable tools by category
        for category in self.TOOL_CATEGORIES[:8]:  # Limit to avoid rate limiting
            try:
                results = self.client.find_profitable_tools(category, max_results=5)
                trends = self._convert_to_trends(results, f"profitable_{category}")
                all_trends.extend(trends)
            except Exception as e:
                logger.warning(f"⚠️ Category {category} failed: {e}")

        # Strategy 2: Find frontend-only projects
        try:
            frontend_results = self.client.find_frontend_only_projects(max_results=15)
            trends = self._convert_to_trends(frontend_results, "frontend_only")
            all_trends.extend(trends)
        except Exception as e:
            logger.warning(f"⚠️ Frontend search failed: {e}")

        # Strategy 3: Find underserved niches
        try:
            niche_results = self.client.find_underserved_niches("online tool")
            trends = self._convert_to_trends(niche_results, "underserved")
            all_trends.extend(trends)
        except Exception as e:
            logger.warning(f"⚠️ Niche search failed: {e}")

        # Deduplicate and limit
        seen_urls = set()
        unique_trends = []
        for trend in all_trends:
            if trend.url and trend.url not in seen_urls:
                seen_urls.add(trend.url)
                unique_trends.append(trend)

        logger.info(f"✅ {self.SOURCE_NAME}: Discovered {len(unique_trends)} trends")
        return unique_trends[:limit]

    def _convert_to_trends(
        self, results: list[dict], strategy: str
    ) -> list[DiscoveredTrend]:
        """Convert search results to DiscoveredTrend objects."""
        trends = []

        for result in results:
            title = result.get("title", "").strip()
            content = result.get("content", "").strip()
            url = result.get("url", "")

            if not title or not url:
                continue

            # Extract tool idea from title
            idea = self._extract_tool_idea(title, content)
            if not idea:
                continue

            # Score based on strategy
            score = self._calculate_score(result, strategy)

            # Extract tags
            tags = self._extract_tags(title, content)
            tags.append(strategy)

            trends.append(DiscoveredTrend(
                source=self.SOURCE_NAME,
                title=idea,
                description=content[:400] if content else f"From: {title}",
                url=url,
                score=score,
                tags=tags[:15],
                discovered_at=datetime.now(),
                raw_data=result,
            ))

        return trends

    def _extract_tool_idea(self, title: str, content: str) -> str | None:
        """Extract a viable tool idea from search result."""
        title_lower = title.lower()

        # Skip non-tool results
        skip_patterns = [
            "news", "article", "blog post", "review", "comparison",
            "top 10", "best of", "vs", "versus", "opinion",
        ]
        if any(p in title_lower for p in skip_patterns):
            return None

        # Look for tool indicators
        tool_indicators = [
            "tool", "app", "generator", "converter", "compressor",
            "editor", "maker", "builder", "optimizer", "creator",
            "downloader", "manager", "tracker", "analyzer", "viewer",
            "formatter", "validator", "checker", "tester", "calculator",
            "resizer", "merger", "splitter", "extractor", "encoder",
        ]

        for indicator in tool_indicators:
            if indicator in title_lower or (content and indicator in content.lower()):
                return title

        return None

    def _calculate_score(self, result: dict, strategy: str) -> float:
        """Calculate relevance score for a result."""
        base_score = 0.5

        # Boost by strategy
        strategy_boosts = {
            "profitable_pdf": 0.3,
            "profitable_image": 0.3,
            "profitable_video": 0.25,
            "profitable_converter": 0.25,
            "frontend_only": 0.35,
            "underserved": 0.4,
        }

        for key, boost in strategy_boosts.items():
            if key in strategy:
                base_score += boost
                break

        # Boost if from GitHub
        url = result.get("url", "")
        if "github.com" in url:
            base_score += 0.1

        # Cap at 1.0
        return min(base_score, 1.0)

    def _extract_tags(self, title: str, content: str) -> list[str]:
        """Extract SEO-relevant tags from title and content."""
        combined = f"{title} {content}".lower()

        tag_mapping = {
            "pdf": "pdf",
            "image": "image",
            "photo": "photo",
            "video": "video",
            "audio": "audio",
            "file": "file",
            "compress": "compression",
            "convert": "converter",
            "edit": "editor",
            "download": "downloader",
            "generate": "generator",
            "qr": "qr-code",
            "json": "json",
            "xml": "xml",
            "csv": "csv",
            "markdown": "markdown",
            "html": "html",
            "css": "css",
            "javascript": "javascript",
            "python": "python",
            "ai": "ai",
            "free": "free",
            "online": "online",
            "browser": "browser-based",
            "no signup": "no-signup",
            "client-side": "client-side",
            "frontend": "frontend-only",
            "static": "static-site",
        }

        tags = []
        for keyword, tag in tag_mapping.items():
            if keyword in combined and tag not in tags:
                tags.append(tag)

        return tags
