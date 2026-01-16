"""
Client modules for external APIs (non-AI).

AI providers are in apex_optimizer/ai/providers/ - NOT here.
"""

from .github import GitHubClient
from .jules import JulesClient
from .web_search import WebSearchClient

__all__ = [
    "GitHubClient",
    "JulesClient",
    "WebSearchClient",
]
