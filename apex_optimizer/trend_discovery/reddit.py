"""
Reddit API Client - Fetches trending posts from programming subreddits.

Uses public JSON API (no OAuth required for read-only).
User-Agent header required.
"""

import logging

import requests

from .base import TrendItem, TrendSource

logger = logging.getLogger("TrendDiscovery.Reddit")


class RedditSource(TrendSource):
    """
    Fetches trending posts from programming-related subreddits.

    Subreddits: r/programming, r/selfhosted, r/sideproject, r/webdev
    """

    BASE_URL = "https://www.reddit.com"
    SUBREDDITS = ["programming", "selfhosted", "sideproject", "webdev", "learnprogramming"]

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "PRFusion-TrendDiscovery/1.0 (github.com/chirag127/PRFusion)",
            "Accept": "application/json",
        })

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch top posts from programming subreddits."""
        trends: list[TrendItem] = []

        for subreddit in self.SUBREDDITS:
            try:
                posts = self._fetch_subreddit(subreddit, limit=5)
                trends.extend(posts)
            except Exception as e:
                logger.warning(f"Failed to fetch r/{subreddit}: {e}")
                continue

        # Sort by popularity and deduplicate
        trends.sort(key=lambda x: x.popularity_score, reverse=True)

        seen = set()
        unique = []
        for trend in trends:
            key = trend.title.lower()[:50]
            if key not in seen:
                seen.add(key)
                unique.append(trend)

        return unique[:limit]

    def _fetch_subreddit(self, subreddit: str, limit: int = 5) -> list[TrendItem]:
        """Fetch top posts from a single subreddit."""
        url = f"{self.BASE_URL}/r/{subreddit}/top.json"
        params = {
            "sort": "top",
            "t": "day",  # Today's top posts
            "limit": limit * 2,  # Extra for filtering
        }

        response = self.session.get(url, params=params, timeout=self.timeout)

        if response.status_code == 429:
            logger.warning("Reddit rate limited")
            return []

        if response.status_code != 200:
            logger.warning(f"Reddit returned {response.status_code}")
            return []

        data = response.json()
        posts = data.get("data", {}).get("children", [])

        trends = []
        for post in posts:
            trend = self._post_to_trend(post.get("data", {}), subreddit)
            if trend and self._is_relevant(trend):
                trends.append(trend)

        return trends[:limit]

    def _post_to_trend(self, post: dict, subreddit: str) -> TrendItem | None:
        """Convert Reddit post to TrendItem."""
        if not post:
            return None

        title = post.get("title", "")
        if not title:
            return None

        url = post.get("url", "")
        selftext = post.get("selftext", "")[:200]
        score = post.get("score", 0)
        num_comments = post.get("num_comments", 0)

        # Calculate popularity (Reddit scores can be very high)
        popularity = self._normalize_score(score + (num_comments * 2), 1000)

        # Build description
        description = selftext if selftext else f"Top post from r/{subreddit}"

        return TrendItem(
            title=self._clean_title(title),
            description=description[:300],
            source="reddit",
            url=f"https://reddit.com{post.get('permalink', '')}",
            popularity_score=popularity,
            category=self._detect_category(f"{title} {selftext}"),
            keywords=self._extract_keywords(f"{title} {selftext}"),
            raw_data={
                "subreddit": subreddit,
                "score": score,
                "num_comments": num_comments,
                "external_url": url,
            },
        )

    def _clean_title(self, title: str) -> str:
        """Clean and shorten Reddit title for use as project name."""
        # Remove common prefixes
        prefixes = ["[Project]", "[Show]", "[Showcase]", "[OC]", "[Discussion]"]
        clean = title
        for prefix in prefixes:
            if clean.startswith(prefix):
                clean = clean[len(prefix):].strip()

        # Take meaningful portion
        if " - " in clean:
            clean = clean.split(" - ")[0].strip()
        elif ": " in clean:
            clean = clean.split(": ")[0].strip()

        return clean[:80]

    def _is_relevant(self, trend: TrendItem) -> bool:
        """Filter for actionable project ideas."""
        title_lower = trend.title.lower()

        # Exclude meta posts, questions, etc.
        exclude_patterns = [
            "what do you think",
            "how do i",
            "help me",
            "question about",
            "looking for",
            "recommend",
            "best practices",
            "weekly thread",
            "daily thread",
        ]

        return not any(p in title_lower for p in exclude_patterns)
