"""
Hashnode GraphQL API Client - Fetches trending posts from Hashnode.

Uses official GraphQL API (free for public content).
"""

import logging

import requests

from .base import TrendItem, TrendSource

logger = logging.getLogger("TrendDiscovery.Hashnode")


class HashnodeSource(TrendSource):
    """
    Fetches trending posts from Hashnode using GraphQL API.

    Focuses on programming and development content.
    """

    API_URL = "https://gql.hashnode.com"
    DEV_TAGS = ["programming", "javascript", "python", "webdev", "devops", "ai"]

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch trending posts from Hashnode."""
        trends: list[TrendItem] = []

        for tag in self.DEV_TAGS[:3]:  # Limit for speed
            try:
                posts = self._fetch_by_tag(tag, limit=5)
                trends.extend(posts)
            except Exception as e:
                logger.warning(f"Failed to fetch Hashnode tag {tag}: {e}")
                continue

        # Deduplicate
        seen = set()
        unique = []
        for trend in trends:
            if trend.title not in seen:
                seen.add(trend.title)
                unique.append(trend)

        unique.sort(key=lambda x: x.popularity_score, reverse=True)
        return unique[:limit]

    def _fetch_by_tag(self, tag: str, limit: int = 5) -> list[TrendItem]:
        """Fetch posts by tag using GraphQL."""
        query = """
        query FeedByTag($tag: String!, $first: Int!) {
            tag(slug: $tag) {
                id
                name
                posts(first: $first, sortBy: HOT) {
                    edges {
                        node {
                            id
                            title
                            brief
                            url
                            reactionCount
                            responseCount
                            author {
                                username
                            }
                        }
                    }
                }
            }
        }
        """

        variables = {
            "tag": tag,
            "first": limit,
        }

        try:
            response = self.session.post(
                self.API_URL,
                json={"query": query, "variables": variables},
                timeout=self.timeout
            )

            if response.status_code != 200:
                logger.warning(f"Hashnode returned {response.status_code}")
                return []

            data = response.json()
            tag_data = data.get("data", {}).get("tag")

            if not tag_data:
                return []

            posts = tag_data.get("posts", {}).get("edges", [])
            return [self._post_to_trend(p.get("node", {}), tag) for p in posts if p]

        except Exception as e:
            logger.warning(f"Hashnode GraphQL error: {e}")
            return []

    def _post_to_trend(self, post: dict, tag: str) -> TrendItem:
        """Convert Hashnode post to TrendItem."""
        title = post.get("title", "")
        brief = post.get("brief", "")
        url = post.get("url", "")
        reactions = post.get("reactionCount", 0)
        responses = post.get("responseCount", 0)

        # Calculate popularity
        popularity = self._normalize_score(reactions + (responses * 2), 100)

        # Extract project idea
        project_name = self._extract_project_idea(title)

        return TrendItem(
            title=project_name,
            description=brief[:300] if brief else title,
            source="hashnode",
            url=url,
            popularity_score=popularity,
            category=self._detect_category(f"{title} {brief}"),
            keywords=self._extract_keywords(f"{title} {tag}"),
            raw_data={
                "original_title": title,
                "reactions": reactions,
                "responses": responses,
                "tag": tag,
                "author": post.get("author", {}).get("username", ""),
            },
        )

    def _extract_project_idea(self, title: str) -> str:
        """Extract project name from article title."""
        patterns = [
            "How to build ",
            "Building ",
            "Creating ",
            "I built ",
            "Introducing ",
        ]

        clean = title
        for pattern in patterns:
            if clean.lower().startswith(pattern.lower()):
                clean = clean[len(pattern):].strip()
                break

        for sep in [" with ", " using ", " in ", " - "]:
            if sep in clean:
                clean = clean.split(sep)[0].strip()
                break

        return clean[:80]
