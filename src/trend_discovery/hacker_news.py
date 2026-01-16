"""
HackerNews API Client - Fetches top stories from HackerNews.

Uses official Firebase API (free, no key required).
Filters for dev/coding related posts.
"""

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from .base import TrendItem, TrendSource

logger = logging.getLogger("TrendDiscovery.HackerNews")


class HackerNewsSource(TrendSource):
    """
    Fetches trending stories from HackerNews using Firebase API.

    Filters for stories related to software development, tools, and coding.
    """

    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    DEV_KEYWORDS = {
        "github", "dev", "code", "programming", "python", "javascript",
        "typescript", "rust", "go", "api", "cli", "tool", "open source",
        "ai", "ml", "llm", "gpt", "library", "framework", "extension",
        "browser", "chrome", "vscode", "editor", "terminal", "automation",
        "database", "sql", "nosql", "docker", "kubernetes", "devops",
    }

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.session = requests.Session()

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch top stories from HackerNews and filter for dev content."""
        try:
            # Get top story IDs
            response = self.session.get(
                f"{self.BASE_URL}/topstories.json",
                timeout=self.timeout
            )
            response.raise_for_status()
            story_ids = response.json()[:50]  # Get top 50 for filtering

        except requests.RequestException as e:
            logger.warning(f"Failed to fetch HN top stories: {e}")
            return []

        # Fetch stories in parallel
        stories = self._fetch_stories_parallel(story_ids)

        # Filter for dev-related content
        dev_stories = [s for s in stories if self._is_dev_related(s)]

        # Convert to TrendItems
        trends = []
        for story in dev_stories[:limit]:
            trend = self._story_to_trend(story)
            if trend:
                trends.append(trend)

        return trends

    def _fetch_stories_parallel(self, story_ids: list[int]) -> list[dict]:
        """Fetch multiple stories in parallel."""
        stories = []

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self._fetch_story, sid): sid
                for sid in story_ids
            }

            for future in as_completed(futures):
                try:
                    story = future.result()
                    if story:
                        stories.append(story)
                except Exception as e:
                    logger.debug(f"Failed to fetch story: {e}")

        return stories

    def _fetch_story(self, story_id: int) -> dict | None:
        """Fetch a single story by ID."""
        try:
            response = self.session.get(
                f"{self.BASE_URL}/item/{story_id}.json",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None

    def _is_dev_related(self, story: dict) -> bool:
        """Check if story is related to software development."""
        if not story:
            return False

        title = story.get("title", "").lower()
        url = story.get("url", "").lower()

        # Check URL for GitHub
        if "github.com" in url:
            return True

        # Check title for dev keywords
        return any(kw in title for kw in self.DEV_KEYWORDS)

    def _story_to_trend(self, story: dict) -> TrendItem | None:
        """Convert HackerNews story to TrendItem."""
        if not story:
            return None

        title = story.get("title", "")
        url = story.get("url", f"https://news.ycombinator.com/item?id={story.get('id')}")
        score = story.get("score", 0)

        # Extract idea from title
        description = f"HN Top Story: {title}"

        # Calculate popularity (HN scores are typically 10-1000+)
        popularity = self._normalize_score(score, 500)

        return TrendItem(
            title=self._extract_project_name(title),
            description=description[:300],
            source="hackernews",
            url=url,
            popularity_score=popularity,
            category=self._detect_category(title),
            keywords=self._extract_keywords(title),
            raw_data={
                "hn_id": story.get("id"),
                "score": score,
                "comments": story.get("descendants", 0),
                "original_title": title,
            },
        )

    def _extract_project_name(self, title: str) -> str:
        """Extract a potential project name from HN title."""
        # Remove common prefixes
        prefixes = ["Show HN:", "Ask HN:", "Launch HN:", "Tell HN:"]
        clean_title = title
        for prefix in prefixes:
            if clean_title.startswith(prefix):
                clean_title = clean_title[len(prefix):].strip()
                break

        # Take first part before common separators
        for sep in [" – ", " - ", " | ", ": ", " — "]:
            if sep in clean_title:
                clean_title = clean_title.split(sep)[0].strip()
                break

        return clean_title[:80]  # Limit length
