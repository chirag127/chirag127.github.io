"""
arXiv Source - CS/AI/ML preprints API.

API Docs: https://arxiv.org/help/api/
Free: Public API, no key required.
"""

import logging
import requests
import xml.etree.ElementTree as ET

from .base import TrendItem, TrendSource, TrendCategory

logger = logging.getLogger("TrendDiscovery.ArXiv")


class ArxivSource(TrendSource):
    """
    Fetches recent CS/AI preprints from arXiv API.

    Categories covered:
    - cs.AI (Artificial Intelligence)
    - cs.LG (Machine Learning)
    - cs.CL (Computation and Language / NLP)
    - cs.CV (Computer Vision)

    No API key required.
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.enabled = True  # Always enabled (public API)

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch recent AI/ML preprints from arXiv."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            params = {
                "search_query": "cat:cs.AI OR cat:cs.LG OR cat:cs.CL OR cat:cs.CV",
                "sortBy": "submittedDate",
                "sortOrder": "descending",
                "max_results": limit,
            }

            response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}

            entries = root.findall("atom:entry", ns)

            for i, entry in enumerate(entries):
                title_el = entry.find("atom:title", ns)
                summary_el = entry.find("atom:summary", ns)
                link_el = entry.find("atom:id", ns)

                title = title_el.text.strip().replace("\n", " ") if title_el is not None else ""
                summary = summary_el.text.strip().replace("\n", " ")[:300] if summary_el is not None else ""
                url = link_el.text if link_el is not None else ""

                if not title:
                    continue

                trend = TrendItem(
                    title=self._format_title(title),
                    description=summary,
                    source="arxiv",
                    url=url,
                    popularity_score=100.0 - (i * 5),  # Recency-based
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{title} {summary}"),
                    raw_data={"title": title, "url": url},
                )
                trends.append(trend)

            logger.info(f"   📄 arXiv: {len(trends)} preprints")

        except Exception as e:
            logger.warning(f"   ⚠️ arXiv: {e}")

        return trends

    def _format_title(self, title: str) -> str:
        """Convert paper title to repo-friendly format."""
        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in title)
        words = clean.split()[:8]
        return "-".join(w.capitalize() for w in words if w)
