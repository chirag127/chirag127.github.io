"""
Product Hunt Source - New product launches & pre-trends.

API Docs: https://api.producthunt.com/v2/docs
Requires: PRODUCT_HUNT_API_KEY (Optional - graceful degradation)
"""

import logging
import os
import requests

from .base import TrendItem, TrendSource, TrendCategory

logger = logging.getLogger("TrendDiscovery.ProductHunt")


class ProductHuntSource(TrendSource):
    """
    Fetches trending products from Product Hunt GraphQL API.

    Features:
    - New product launches
    - Upvote velocity tracking
    - Tech/AI/Dev tool focus

    Optional: Set PRODUCT_HUNT_API_KEY for access.
    If not set, this source is silently disabled.
    """

    BASE_URL = "https://api.producthunt.com/v2/api/graphql"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.api_key = os.getenv("PRODUCT_HUNT_API_KEY")
        self.enabled = bool(self.api_key)

        if not self.enabled:
            logger.debug("   ℹ️ ProductHunt: Disabled (no API key)")

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch trending products from Product Hunt."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }

            query = """
            query {
                posts(first: %d) {
                    edges {
                        node {
                            id
                            name
                            tagline
                            url
                            votesCount
                            topics {
                                edges {
                                    node {
                                        name
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """ % limit

            response = requests.post(
                self.BASE_URL,
                json={"query": query},
                headers=headers,
                timeout=self.timeout,
            )
            response.raise_for_status()

            data = response.json()
            posts = data.get("data", {}).get("posts", {}).get("edges", [])

            max_votes = max((p["node"].get("votesCount", 0) for p in posts), default=1)

            for post in posts:
                node = post.get("node", {})
                name = node.get("name", "")
                tagline = node.get("tagline", "")
                votes = node.get("votesCount", 0)
                url = node.get("url", "")

                if not name:
                    continue

                # Extract topics as keywords
                topics = [
                    t["node"]["name"]
                    for t in node.get("topics", {}).get("edges", [])
                ]

                trend = TrendItem(
                    title=self._format_title(name),
                    description=tagline[:300] if tagline else "Trending product on Product Hunt.",
                    source="producthunt",
                    url=url,
                    popularity_score=self._normalize_score(votes, max_votes),
                    category=self._detect_category(f"{name} {tagline}"),
                    keywords=topics[:10] if topics else self._extract_keywords(f"{name} {tagline}"),
                    raw_data=node,
                )
                trends.append(trend)

            logger.info(f"   🚀 ProductHunt: {len(trends)} products")

        except Exception as e:
            logger.warning(f"   ⚠️ ProductHunt: {e}")

        return trends

    def _format_title(self, title: str) -> str:
        """Convert product name to repo-friendly format."""
        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in title)
        words = clean.split()[:8]
        formatted = "-".join(w.capitalize() for w in words if w)
        # Add type suffix if not present
        if not any(suffix in formatted.lower() for suffix in ["-app", "-tool", "-extension", "-web"]):
            formatted += "-Web-App"
        return formatted
