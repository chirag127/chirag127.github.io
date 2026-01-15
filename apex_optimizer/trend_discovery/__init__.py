"""
Trend Discovery Package - Aggregates trending software ideas from 15+ sources.

Dec 2025 Update: Now fetches 100+ topics for AI-powered selection.

Sources (No Keys Required):
- GitHub Trending (scraping)
- HackerNews (Firebase API)
- Reddit (JSON API)
- Dev.to (Forem API)
- Hashnode (GraphQL)
- StackOverflow (Stack Exchange API)
- ArXiv (Research papers)
- Papers with Code (ML research)
- Semantic Scholar (Academic papers)
- Lobsters (Tech community)

Sources (Optional API Keys):
- HuggingFace (ML models)
- Kaggle (Data science)
- ProductHunt (Startups)
- NewsAPI (Tech news)
- TechCrunch (RSS)
"""

from .aggregator import TrendAggregator, AggregatorConfig
from .base import TrendItem, TrendSource, TrendCategory
from .selector import TrendSelector, SelectedTrend
from .devto import DevToSource
from .github_trending import GitHubTrendingSource
from .hacker_news import HackerNewsSource
from .hashnode import HashnodeSource
from .reddit import RedditSource
from .stack_overflow import StackOverflowSource

__all__ = [
    # Core
    "TrendAggregator",
    "AggregatorConfig",
    "TrendSelector",
    "SelectedTrend",
    # Types
    "TrendItem",
    "TrendSource",
    "TrendCategory",
    # Sources
    "GitHubTrendingSource",
    "HackerNewsSource",
    "RedditSource",
    "DevToSource",
    "HashnodeSource",
    "StackOverflowSource",
]
