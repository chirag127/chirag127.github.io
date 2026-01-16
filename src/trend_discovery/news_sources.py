"""
News Sources - AI/Tech news aggregation.

Includes:
- NewsAPI.ai
- TechCrunch (via RSS)
- AI-specific news feeds

Optional: NEWSAPI_AI_KEY for NewsAPI.ai
"""

import logging
import os
import requests
import xml.etree.ElementTree as ET

from .base import TrendItem, TrendSource, TrendCategory

logger = logging.getLogger("TrendDiscovery.News")


class NewsAPISource(TrendSource):
    """
    Fetches AI/Tech news from NewsAPI.ai.

    Features:
    - 150K+ global publishers
    - Sentiment analysis
    - Topic identification

    Optional: Set NEWSAPI_AI_KEY for access.
    If not set, this source is silently disabled.
    """

    BASE_URL = "https://newsapi.ai/api/v1/article/getArticles"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.api_key = os.getenv("NEWSAPI_AI_KEY")
        self.enabled = bool(self.api_key)

        if not self.enabled:
            logger.debug("   ℹ️ NewsAPI.ai: Disabled (no API key)")

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch AI/Tech news articles."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            params = {
                "apiKey": self.api_key,
                "keyword": "artificial intelligence OR machine learning OR LLM",
                "lang": "eng",
                "articlesPage": 1,
                "articlesCount": limit,
                "articlesSortBy": "date",
            }

            response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            articles = data.get("articles", {}).get("results", [])

            for i, article in enumerate(articles):
                title = article.get("title", "")
                body = article.get("body", "")
                url = article.get("url", "")
                source_name = article.get("source", {}).get("title", "")

                if not title:
                    continue

                trend = TrendItem(
                    title=self._format_title(title),
                    description=body[:300] if body else f"News from {source_name}.",
                    source="newsapi",
                    url=url,
                    popularity_score=100.0 - (i * 5),  # Recency-based
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{title} {body}"),
                    raw_data=article,
                )
                trends.append(trend)

            logger.info(f"   📰 NewsAPI.ai: {len(trends)} articles")

        except Exception as e:
            logger.warning(f"   ⚠️ NewsAPI.ai: {e}")

        return trends

    def _format_title(self, title: str) -> str:
        """Convert news title to repo-friendly format."""
        # Remove common news prefixes
        prefixes_to_remove = ["breaking:", "update:", "news:", "report:"]
        title_lower = title.lower()
        for prefix in prefixes_to_remove:
            if title_lower.startswith(prefix):
                title = title[len(prefix):].strip()
                break

        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in title)
        words = clean.split()[:8]
        formatted = "-".join(w.capitalize() for w in words if w)
        return f"{formatted}-Implementation"


class TechCrunchRSSSource(TrendSource):
    """
    Fetches tech news from TechCrunch RSS feed.

    No API key required.
    """

    RSS_URL = "https://techcrunch.com/category/artificial-intelligence/feed/"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.enabled = True  # Always enabled (public RSS)

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch AI news from TechCrunch RSS."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            response = requests.get(self.RSS_URL, timeout=self.timeout)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            items = root.findall(".//item")[:limit]

            for i, item in enumerate(items):
                title_el = item.find("title")
                desc_el = item.find("description")
                link_el = item.find("link")

                title = title_el.text if title_el is not None else ""
                description = desc_el.text[:300] if desc_el is not None and desc_el.text else ""
                url = link_el.text if link_el is not None else ""

                if not title:
                    continue

                trend = TrendItem(
                    title=self._format_title(title),
                    description=description,
                    source="techcrunch",
                    url=url,
                    popularity_score=100.0 - (i * 5),
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{title} {description}"),
                    raw_data={"title": title, "url": url},
                )
                trends.append(trend)

            logger.info(f"   📢 TechCrunch: {len(trends)} articles")

        except Exception as e:
            logger.warning(f"   ⚠️ TechCrunch: {e}")

        return trends

    def _format_title(self, title: str) -> str:
        """Convert news title to repo-friendly format."""
        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in title)
        words = clean.split()[:8]
        formatted = "-".join(w.capitalize() for w in words if w)
        return f"{formatted}-Tool"
