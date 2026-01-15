"""
Dev.to Forem API Client - Fetches trending articles from Dev.to.

Uses official Forem API (free, no key required for public content).
"""

import logging

import requests

from .base import TrendItem, TrendSource

logger = logging.getLogger("TrendDiscovery.DevTo")


class DevToSource(TrendSource):
    """
    Fetches trending articles from Dev.to using the Forem API.

    Focuses on articles with high engagement and dev tool tags.
    """

    BASE_URL = "https://dev.to/api"
    DEV_TAGS = ["opensource", "devtools", "productivity", "tutorial", "showdev", "webdev"]

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "PRFusion-TrendDiscovery/1.0",
        })

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch trending articles from Dev.to."""
        trends: list[TrendItem] = []

        # Fetch from multiple tags
        for tag in self.DEV_TAGS[:4]:  # Limit tags for speed
            try:
                articles = self._fetch_by_tag(tag, limit=5)
                trends.extend(articles)
            except Exception as e:
                logger.warning(f"Failed to fetch Dev.to tag {tag}: {e}")
                continue

        # Also fetch top articles (no tag filter)
        try:
            top_articles = self._fetch_top_articles(limit=10)
            trends.extend(top_articles)
        except Exception as e:
            logger.warning(f"Failed to fetch Dev.to top articles: {e}")

        # Deduplicate and sort
        seen = set()
        unique = []
        for trend in trends:
            if trend.title not in seen:
                seen.add(trend.title)
                unique.append(trend)

        unique.sort(key=lambda x: x.popularity_score, reverse=True)
        return unique[:limit]

    def _fetch_by_tag(self, tag: str, limit: int = 5) -> list[TrendItem]:
        """Fetch articles by tag."""
        url = f"{self.BASE_URL}/articles"
        params = {
            "tag": tag,
            "per_page": limit,
            "top": 1,  # Top articles from today
        }

        response = self.session.get(url, params=params, timeout=self.timeout)

        if response.status_code != 200:
            return []

        articles = response.json()
        return [self._article_to_trend(a) for a in articles if a]

    def _fetch_top_articles(self, limit: int = 10) -> list[TrendItem]:
        """Fetch top articles overall."""
        url = f"{self.BASE_URL}/articles"
        params = {
            "per_page": limit,
            "top": 7,  # Top from last 7 days
        }

        response = self.session.get(url, params=params, timeout=self.timeout)

        if response.status_code != 200:
            return []

        articles = response.json()
        return [self._article_to_trend(a) for a in articles if a]

    def _article_to_trend(self, article: dict) -> TrendItem:
        """Convert Dev.to article to TrendItem."""
        title = article.get("title", "")
        description = article.get("description", "")
        url = article.get("url", "")
        reactions = article.get("positive_reactions_count", 0)
        comments = article.get("comments_count", 0)
        tags = article.get("tag_list", [])

        # Calculate popularity
        popularity = self._normalize_score(reactions + (comments * 3), 200)

        # Extract project idea from title
        project_name = self._extract_project_idea(title)

        return TrendItem(
            title=project_name,
            description=description[:300] if description else title,
            source="devto",
            url=url,
            popularity_score=popularity,
            category=self._detect_category(f"{title} {description}"),
            keywords=self._extract_keywords(f"{title} {' '.join(tags)}"),
            raw_data={
                "original_title": title,
                "reactions": reactions,
                "comments": comments,
                "tags": tags,
                "author": article.get("user", {}).get("username", ""),
            },
        )

    def _extract_project_idea(self, title: str) -> str:
        """Extract a potential project name from article title."""
        # Remove common article patterns
        patterns = [
            "How to build ",
            "Building ",
            "Creating ",
            "I built ",
            "I made ",
            "Introducing ",
            "Announcing ",
            "My ",
        ]

        clean = title
        for pattern in patterns:
            if clean.startswith(pattern):
                clean = clean[len(pattern):].strip()
                break

        # Take first part before common separators
        for sep in [" with ", " using ", " in ", " - ", " | ", ": "]:
            if sep in clean:
                clean = clean.split(sep)[0].strip()
                break

        return clean[:80]
