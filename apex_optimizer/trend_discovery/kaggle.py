"""
Kaggle Source - Datasets, competitions, and notebooks.

API Docs: https://github.com/Kaggle/kaggle-api
Requires: KAGGLE_USERNAME and KAGGLE_KEY (Optional)
"""

import logging
import os
import requests

from .base import TrendItem, TrendSource, TrendCategory

logger = logging.getLogger("TrendDiscovery.Kaggle")


class KaggleSource(TrendSource):
    """
    Fetches trending datasets and competitions from Kaggle.

    Features:
    - Trending datasets
    - Active competitions
    - Popular notebooks

    Optional: Set KAGGLE_USERNAME and KAGGLE_KEY for access.
    If not set, this source is silently disabled.
    """

    BASE_URL = "https://www.kaggle.com/api/v1"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.username = os.getenv("KAGGLE_USERNAME")
        self.key = os.getenv("KAGGLE_KEY")
        self.enabled = bool(self.username and self.key)

        if not self.enabled:
            logger.debug("   ℹ️ Kaggle: Disabled (no credentials)")

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch trending datasets and competitions from Kaggle."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            # Fetch trending datasets
            url = f"{self.BASE_URL}/datasets/list"
            params = {"sortBy": "hottest", "maxSize": limit}

            auth = (self.username, self.key)
            response = requests.get(
                url, params=params, auth=auth, timeout=self.timeout
            )
            response.raise_for_status()

            datasets = response.json()

            for i, dataset in enumerate(datasets[:limit]):
                title = dataset.get("title", "")
                subtitle = dataset.get("subtitle", "")
                ref = dataset.get("ref", "")
                usability = dataset.get("usabilityRating", 0)

                if not title:
                    continue

                trend = TrendItem(
                    title=self._format_title(title),
                    description=subtitle[:300] if subtitle else f"Trending Kaggle dataset (usability: {usability}).",
                    source="kaggle",
                    url=f"https://www.kaggle.com/datasets/{ref}",
                    popularity_score=usability * 10,  # 0-10 -> 0-100
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{title} {subtitle} dataset"),
                    raw_data=dataset,
                )
                trends.append(trend)

            logger.info(f"   📊 Kaggle: {len(trends)} datasets")

        except Exception as e:
            logger.warning(f"   ⚠️ Kaggle: {e}")

        # Fetch competitions
        try:
            comp_url = f"{self.BASE_URL}/competitions/list"
            params = {"sortBy": "recentlyCreated", "maxSize": limit // 2}

            response = requests.get(
                comp_url, params=params, auth=auth, timeout=self.timeout
            )
            response.raise_for_status()

            competitions = response.json()

            for comp in competitions:
                title = comp.get("title", "")
                description = comp.get("description", "")
                ref = comp.get("ref", "")
                reward = comp.get("reward", "")

                if not title:
                    continue

                trend = TrendItem(
                    title=self._format_title(title, "Competition"),
                    description=f"{description[:200]}... Reward: {reward}" if description else f"Kaggle competition. Reward: {reward}",
                    source="kaggle",
                    url=f"https://www.kaggle.com/competitions/{ref}",
                    popularity_score=80.0,  # Competitions are high-value
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{title} competition ml"),
                    raw_data=comp,
                )
                trends.append(trend)

            logger.info(f"   🏆 Kaggle Competitions: {len(competitions)} active")

        except Exception as e:
            logger.debug(f"   ⚠️ Kaggle Competitions: {e}")

        return trends

    def _format_title(self, title: str, suffix: str = "Dataset") -> str:
        """Convert dataset/competition name to repo-friendly format."""
        clean = "".join(c if c.isalnum() or c.isspace() else " " for c in title)
        words = clean.split()[:6]
        formatted = "-".join(w.capitalize() for w in words if w)
        return f"{formatted}-{suffix}-Analysis-Tool"
