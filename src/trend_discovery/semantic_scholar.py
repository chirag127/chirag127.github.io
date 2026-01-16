"""
Semantic Scholar Source - Academic research papers API.

API Docs: https://api.semanticscholar.org/
Free tier: 100 requests/5 min without key, higher with key.
"""

import logging
import os
import requests
from datetime import datetime

from .base import TrendItem, TrendSource, TrendCategory

logger = logging.getLogger("TrendDiscovery.SemanticScholar")


class SemanticScholarSource(TrendSource):
    """
    Fetches trending AI/ML research papers from Semantic Scholar API.

    Features:
    - 200M+ academic papers
    - Citation velocity tracking
    - SPECTER2 embeddings for semantic search

    Optional: Set SEMANTIC_SCHOLAR_API_KEY for higher rate limits.
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        self.headers = {"x-api-key": self.api_key} if self.api_key else {}
        self.enabled = True  # Always enabled (public API)

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch recent high-impact AI/ML papers."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            url = f"{self.BASE_URL}/paper/search"
            params = {
                "query": "machine learning OR artificial intelligence OR LLM OR transformer",
                "fields": "title,abstract,url,citationCount,year,authors",
                "limit": limit,
                "year": f"{datetime.now().year - 1}-{datetime.now().year}",
            }

            response = requests.get(
                url, params=params, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            papers = data.get("data", [])

            max_citations = max((p.get("citationCount", 0) for p in papers), default=1)

            for paper in papers:
                title = paper.get("title", "")
                abstract = paper.get("abstract", "") or ""
                citations = paper.get("citationCount", 0)

                if not title:
                    continue

                trend = TrendItem(
                    title=self._format_title(title),
                    description=abstract[:300] if abstract else f"Research paper with {citations} citations.",
                    source="semantic_scholar",
                    url=paper.get("url", f"https://semanticscholar.org/paper/{paper.get('paperId', '')}"),
                    popularity_score=self._normalize_score(citations, max_citations),
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{title} {abstract}"),
                    raw_data=paper,
                )
                trends.append(trend)

            logger.info(f"   📚 SemanticScholar: {len(trends)} papers")

        except Exception as e:
            logger.warning(f"   ⚠️ SemanticScholar: {e}")

        return trends

    def _format_title(self, title: str) -> str:
        """Convert paper title to repo-friendly format."""
        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in title)
        words = clean.split()[:8]
        return "-".join(w.capitalize() for w in words if w)
