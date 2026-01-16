"""
PapersWithCode Source - Papers with code implementations.

API Docs: https://paperswithcode.com/api/v1/docs/
Free: Public API, no key required.
"""

import logging
import requests

from .base import TrendItem, TrendSource, TrendCategory

logger = logging.getLogger("TrendDiscovery.PapersWithCode")


class PapersWithCodeSource(TrendSource):
    """
    Fetches papers with code implementations from PapersWithCode API.

    Features:
    - Papers linked to GitHub repos
    - State-of-the-art tracking
    - Benchmark results

    No API key required.
    """

    BASE_URL = "https://paperswithcode.com/api/v1"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.enabled = True  # Always enabled (public API)

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch papers with trending code implementations."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            url = f"{self.BASE_URL}/papers/"
            params = {"items_per_page": limit}

            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            papers = data.get("results", [])

            for i, paper in enumerate(papers):
                title = paper.get("title", "")
                abstract = paper.get("abstract", "") or ""
                paper_url = paper.get("url_abs", "") or paper.get("paper_url", "")

                if not title:
                    continue

                trend = TrendItem(
                    title=self._format_title(title),
                    description=abstract[:300] if abstract else "Paper with code implementation.",
                    source="paperswithcode",
                    url=paper_url or f"https://paperswithcode.com/paper/{paper.get('id', '')}",
                    popularity_score=100.0 - (i * 5),  # Recency-based
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{title} {abstract}"),
                    raw_data=paper,
                )
                trends.append(trend)

            logger.info(f"   💻 PapersWithCode: {len(trends)} papers")

        except Exception as e:
            logger.warning(f"   ⚠️ PapersWithCode: {e}")

        return trends

    def _format_title(self, title: str) -> str:
        """Convert paper title to repo-friendly format."""
        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in title)
        words = clean.split()[:8]
        return "-".join(w.capitalize() for w in words if w)
