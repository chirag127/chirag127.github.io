"""
GitHub Trending Scraper - Fetches trending repositories from GitHub.

Uses BeautifulSoup to parse github.com/trending page.
No API key required, respects GitHub ToS.
"""

import logging
import re
from typing import Any

import requests
from bs4 import BeautifulSoup

from .base import TrendCategory, TrendItem, TrendSource

logger = logging.getLogger("TrendDiscovery.GitHub")


class GitHubTrendingSource(TrendSource):
    """
    Scrapes GitHub trending page for popular repositories.

    Supports daily, weekly, and monthly trends across multiple languages.
    """

    BASE_URL = "https://github.com/trending"
    LANGUAGES = ["", "python", "typescript", "javascript", "rust", "go"]

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml",
        })

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch trending repositories from GitHub."""
        trends: list[TrendItem] = []

        for language in self.LANGUAGES[:3]:  # Top 3 languages for speed
            try:
                url = f"{self.BASE_URL}/{language}?since=daily" if language else f"{self.BASE_URL}?since=daily"
                response = self.session.get(url, timeout=self.timeout)

                if response.status_code != 200:
                    logger.warning(f"GitHub trending returned {response.status_code}")
                    continue

                page_trends = self._parse_trending_page(response.text, language)
                trends.extend(page_trends)

                if len(trends) >= limit * 2:  # Get extra for deduplication
                    break

            except requests.RequestException as e:
                logger.warning(f"Failed to fetch GitHub trending ({language}): {e}")
                continue

        # Deduplicate and limit
        seen = set()
        unique_trends = []
        for trend in trends:
            key = trend.title.lower()
            if key not in seen:
                seen.add(key)
                unique_trends.append(trend)

        return unique_trends[:limit]

    def _parse_trending_page(self, html: str, language: str) -> list[TrendItem]:
        """Parse the GitHub trending HTML page."""
        soup = BeautifulSoup(html, "html.parser")
        trends: list[TrendItem] = []

        # Find all repository articles
        articles = soup.find_all("article", class_="Box-row")

        for article in articles[:20]:  # Limit per language
            try:
                trend = self._parse_article(article, language)
                if trend:
                    trends.append(trend)
            except Exception as e:
                logger.debug(f"Failed to parse article: {e}")
                continue

        return trends

    def _parse_article(self, article: Any, language: str) -> TrendItem | None:
        """Parse a single trending repository article."""
        # Get repo name (format: owner/repo)
        h2 = article.find("h2")
        if not h2:
            return None

        repo_link = h2.find("a")
        if not repo_link:
            return None

        href = repo_link.get("href", "").strip("/")
        if "/" not in href:
            return None

        owner, repo = href.split("/", 1) if "/" in href else ("", href)
        repo_name = repo.strip()

        # Get description
        desc_elem = article.find("p", class_="col-9")
        description = desc_elem.get_text(strip=True) if desc_elem else ""

        # Get stars today
        stars_today = 0
        stars_text = article.find(string=re.compile(r"stars today|stars this"))
        if stars_text:
            match = re.search(r"([\d,]+)", stars_text)
            if match:
                stars_today = int(match.group(1).replace(",", ""))

        # Get total stars
        total_stars = 0
        star_link = article.find("a", href=re.compile(r"/stargazers"))
        if star_link:
            star_text = star_link.get_text(strip=True)
            match = re.search(r"([\d,]+)", star_text)
            if match:
                total_stars = int(match.group(1).replace(",", ""))

        # Calculate popularity score (weighted by stars today)
        score = min(100, stars_today * 2 + (total_stars / 1000))

        # Detect category
        full_text = f"{repo_name} {description}"
        category = self._detect_category(full_text)

        return TrendItem(
            title=repo_name,
            description=description[:300] if description else f"Trending {language or 'repository'} on GitHub",
            source="github",
            url=f"https://github.com/{href}",
            popularity_score=score,
            category=category,
            keywords=self._extract_keywords(full_text) + ([language] if language else []),
            raw_data={
                "owner": owner,
                "repo": repo_name,
                "stars_today": stars_today,
                "total_stars": total_stars,
                "language": language,
            },
        )
