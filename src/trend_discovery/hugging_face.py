"""
Hugging Face Source - AI/ML models, datasets, and papers.

API Docs: https://huggingface.co/docs/hub/api
Optional: HF_TOKEN for private models (public access without key).
"""

import logging
import os
import requests

from .base import TrendItem, TrendSource, TrendCategory

logger = logging.getLogger("TrendDiscovery.HuggingFace")


class HuggingFaceSource(TrendSource):
    """
    Fetches trending models and spaces from Hugging Face Hub.

    Features:
    - Trending ML models
    - Spaces (demos)
    - Associated papers

    Optional: Set HF_TOKEN for private model access.
    Works without key for public models.
    """

    BASE_URL = "https://huggingface.co/api"

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.token = os.getenv("HF_TOKEN")
        self.headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        self.enabled = True  # Works without key (public models)

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch trending models from Hugging Face."""
        if not self.enabled:
            return []

        trends: list[TrendItem] = []

        try:
            # Fetch trending models
            url = f"{self.BASE_URL}/models"
            params = {
                "sort": "likes",  # Sort by popularity
                "direction": -1,  # Descending
                "limit": limit,
                "filter": "text-generation",  # Focus on LLMs
            }

            response = requests.get(
                url, params=params, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()

            models = response.json()
            max_likes = max((m.get("likes", 0) for m in models), default=1)

            for model in models:
                model_id = model.get("modelId", "")
                likes = model.get("likes", 0)
                pipeline_tag = model.get("pipeline_tag", "")

                if not model_id:
                    continue

                # Extract model name from ID (e.g., "meta-llama/Llama-3.1-8B" -> "Llama-3.1-8B")
                name = model_id.split("/")[-1] if "/" in model_id else model_id

                trend = TrendItem(
                    title=self._format_title(name, pipeline_tag),
                    description=f"Trending {pipeline_tag} model with {likes} likes on Hugging Face.",
                    source="huggingface",
                    url=f"https://huggingface.co/{model_id}",
                    popularity_score=self._normalize_score(likes, max_likes),
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{name} {pipeline_tag} model transformer"),
                    raw_data=model,
                )
                trends.append(trend)

            logger.info(f"   🤗 HuggingFace: {len(trends)} models")

        except Exception as e:
            logger.warning(f"   ⚠️ HuggingFace: {e}")

        # Also fetch trending Spaces
        try:
            spaces_url = f"{self.BASE_URL}/spaces"
            params = {"sort": "likes", "direction": -1, "limit": limit // 2}

            response = requests.get(
                spaces_url, params=params, headers=self.headers, timeout=self.timeout
            )
            response.raise_for_status()

            spaces = response.json()

            for space in spaces:
                space_id = space.get("id", "")
                likes = space.get("likes", 0)

                if not space_id:
                    continue

                name = space_id.split("/")[-1] if "/" in space_id else space_id

                trend = TrendItem(
                    title=self._format_title(name, "demo"),
                    description=f"Trending AI demo Space with {likes} likes.",
                    source="huggingface",
                    url=f"https://huggingface.co/spaces/{space_id}",
                    popularity_score=self._normalize_score(likes, 1000),  # Normalized
                    category=TrendCategory.AI_ML,
                    keywords=self._extract_keywords(f"{name} demo ai space"),
                    raw_data=space,
                )
                trends.append(trend)

            logger.info(f"   🎨 HuggingFace Spaces: {len(spaces)} demos")

        except Exception as e:
            logger.debug(f"   ⚠️ HuggingFace Spaces: {e}")

        return trends

    def _format_title(self, name: str, pipeline_tag: str) -> str:
        """Convert model name to repo-friendly format."""
        clean = "".join(c if c.isalnum() or c.isspace() or c == "-" else " " for c in name)
        words = clean.split()[:6]
        formatted = "-".join(w.capitalize() for w in words if w)

        # Add suffix based on pipeline
        if pipeline_tag == "text-generation":
            formatted += "-LLM-Implementation"
        elif pipeline_tag == "image-classification":
            formatted += "-Vision-Model"
        elif pipeline_tag == "demo":
            formatted += "-AI-Demo-App"
        else:
            formatted += "-AI-Model"

        return formatted
