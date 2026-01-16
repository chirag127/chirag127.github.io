"""
Base classes for trend discovery sources.

Defines the abstract interface and common data structures for all trend sources.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger("TrendDiscovery")


class TrendCategory(Enum):
    """Categories for trending ideas."""
    WEB_APP = "web_app"
    CHROME_EXTENSION = "chrome_extension"
    CLI_TOOL = "cli_tool"
    LIBRARY = "library"
    AI_ML = "ai_ml"
    DEVTOOLS = "devtools"
    AUTOMATION = "automation"
    UTILITY = "utility"
    UNKNOWN = "unknown"


@dataclass
class TrendItem:
    """
    Represents a single trending idea/project.

    Attributes:
        title: Name or title of the trend
        description: Brief description
        source: Origin source (github, hackernews, reddit, etc.)
        url: Original URL
        popularity_score: Normalized score (0-100)
        category: Detected category
        keywords: Extracted keywords for matching
        raw_data: Original source data
    """
    title: str
    description: str
    source: str
    url: str
    popularity_score: float = 0.0
    category: TrendCategory = TrendCategory.UNKNOWN
    keywords: list[str] = field(default_factory=list)
    raw_data: dict[str, Any] = field(default_factory=dict)
    discovered_at: datetime = field(default_factory=datetime.now)

    def __hash__(self) -> int:
        return hash(self.title.lower())

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TrendItem):
            return False
        return self.title.lower() == other.title.lower()

    def to_dict(self) -> dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "source": self.source,
            "url": self.url,
            "popularity_score": self.popularity_score,
            "category": self.category.value,
            "keywords": self.keywords,
            "discovered_at": self.discovered_at.isoformat(),
        }


class TrendSource(ABC):
    """
    Abstract base class for all trend discovery sources.

    Subclasses must implement fetch_trends() method.
    """

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.name = self.__class__.__name__

    @abstractmethod
    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """
        Fetch trending items from the source.

        Args:
            limit: Maximum number of trends to return

        Returns:
            List of TrendItem objects
        """
        pass

    def _normalize_score(self, value: float, max_value: float) -> float:
        """Normalize a score to 0-100 range."""
        if max_value <= 0:
            return 0.0
        return min(100.0, (value / max_value) * 100)

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract relevant keywords from text."""
        if not text:
            return []

        # Common tech keywords to look for
        tech_keywords = {
            "ai", "ml", "api", "cli", "web", "app", "bot", "tool",
            "extension", "chrome", "firefox", "browser", "automation",
            "react", "vue", "svelte", "typescript", "python", "rust",
            "go", "node", "deno", "bun", "vite", "next", "nuxt",
            "database", "auth", "security", "performance", "testing",
            "docker", "kubernetes", "devops", "cicd", "github", "git",
            "llm", "gpt", "claude", "gemini", "openai", "ollama",
        }

        words = text.lower().split()
        found = [w.strip(".,!?()[]{}") for w in words if w.strip(".,!?()[]{}") in tech_keywords]
        return list(set(found))[:10]  # Dedupe and limit

    def _detect_category(self, text: str) -> TrendCategory:
        """Detect category from text content."""
        text_lower = text.lower()

        if any(kw in text_lower for kw in ["chrome extension", "browser extension", "firefox addon"]):
            return TrendCategory.CHROME_EXTENSION
        if any(kw in text_lower for kw in ["cli", "command line", "terminal"]):
            return TrendCategory.CLI_TOOL
        if any(kw in text_lower for kw in ["ai", "ml", "llm", "gpt", "model", "neural"]):
            return TrendCategory.AI_ML
        if any(kw in text_lower for kw in ["library", "package", "sdk", "framework"]):
            return TrendCategory.LIBRARY
        if any(kw in text_lower for kw in ["devtool", "developer tool", "debugging"]):
            return TrendCategory.DEVTOOLS
        if any(kw in text_lower for kw in ["automate", "automation", "workflow", "bot"]):
            return TrendCategory.AUTOMATION
        if any(kw in text_lower for kw in ["web", "app", "dashboard", "ui", "frontend"]):
            return TrendCategory.WEB_APP

        return TrendCategory.UTILITY
