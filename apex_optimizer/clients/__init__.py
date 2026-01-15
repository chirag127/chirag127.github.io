"""
Client modules for external APIs (non-AI).

AI providers are in apex_optimizer/ai/providers/ - NOT here.
"""

from .github import GitHubClient
from .jules import JulesClient
from .searxng import SearXNGClient, get_searxng_client

__all__ = [
    "GitHubClient",
    "JulesClient",
    "SearXNGClient",
    "get_searxng_client",
]
