"""
Lobsters Source - Curated tech news community.

Similar to Hacker News but with invite-only curation.
No API key required.
"""

import logging
import requests

from .base import TrendItem, TrendSource, TrendCategory

logger = logging.getLogger("TrendDiscovery.Lobsters")


class LobstersSource(TrendSource):
    """
    Fetches trending stories from Lobsters.

    Features:
    - Invite-only community (higher quality)
    - Technical focus
    - Tagging system

    No API key required.
    """

    BASE_URL = "https://lobste.rs"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.enabled = True  # Always enabled (public API)

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch hottest stories from Lobsters."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            url = f"{self.BASE_URL}/hottest.json"
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            stories = response.json()[:limit]
            max_score = max((s.get("score", 0) for s in stories), default=1)

            for story in stories:
                title = story.get("title", "")
                url_link = story.get("url", "") or story.get("comments_url", "")
                score = story.get("score", 0)
                tags = story.get("tags", [])

                if not title:
                    continue

                trend = TrendItem(
                    title=self._format_title(title),
                    description=f"Lobsters story with {score} points. Tags: {', '.join(tags)}",
                    source="lobsters",
                    url=url_link,
                    popularity_score=self._normalize_score(score, max_score),
                    category=self._detect_category(f"{title} {' '.join(tags)}"),
                    keywords=tags[:10] if tags else self._extract_keywords(title),
                    raw_data=story,
                )
                trends.append(trend)

            logger.info(f"   🦞 Lobsters: {len(trends)} stories")

        except Exception as e:
            logger.warning(f"   ⚠️ Lobsters: {e}")

        return trends

    def _format_title(self, title: str) -> str:
        """Convert story title to repo-friendly format."""
        # Remove common patterns
        title = title.replace("Show Lobsters:", "").replace("Ask Lobsters:", "").strip()

        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in title)
        words = clean.split()[:8]
        formatted = "-".join(w.capitalize() for w in words if w)

        # Add suffix if not present
        if not any(suffix in formatted.lower() for suffix in ["-tool", "-app", "-lib", "-cli"]):
            formatted += "-Tool"

        return formatted
