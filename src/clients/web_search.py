"""
Unified Web Search Client.
Supports multiple free/freemium search providers with fallback.

Providers:
1. Brave Search API (1 request/sec free)
2. Exa (Metaphor) API (Free tier available)
3. Tavily API (Free tier available)
4. DuckDuckGo (No key required, rate limited)
"""

import logging
import os
import requests
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger("Clients.WebSearch")

@dataclass
class SearchResult:
    title: str
    url: str
    description: str
    source: str

class WebSearchClient:
    """
    Unified client for web search with automatic fallback.
    """

    def __init__(self):
        self.brave_key = os.getenv("BRAVE_API_KEY")
        self.exa_key = os.getenv("EXA_API_KEY")
        self.tavily_key = os.getenv("TAVILY_API_KEY")

        # Initialize DuckDuckGo session
        self.ddg_session = requests.Session()
        self.ddg_session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })

    def search(self, query: str, limit: int = 10) -> List[SearchResult]:
        """
        Perform web search using available providers in priority order.
        """
        results = []

        # Priority 1: Tavily (Best for RAG/AI)
        if self.tavily_key:
            try:
                results = self._search_tavily(query, limit)
                if results: return results
            except Exception as e:
                logger.warning(f"Tavily search failed: {e}")

        # Priority 2: Exa (Good for semantic search)
        if self.exa_key:
            try:
                results = self._search_exa(query, limit)
                if results: return results
            except Exception as e:
                logger.warning(f"Exa search failed: {e}")

        # Priority 3: Brave (Good for general web)
        if self.brave_key:
            try:
                results = self._search_brave(query, limit)
                if results: return results
            except Exception as e:
                logger.warning(f"Brave search failed: {e}")

        # Priority 4: DuckDuckGo (Fallback, no key)
        try:
            results = self._search_ddg(query, limit)
            if results: return results
        except Exception as e:
            logger.warning(f"DuckDuckGo search failed: {e}")

        return []

    def _search_tavily(self, query: str, limit: int) -> List[SearchResult]:
        """Search using Tavily API."""
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"query": query, "max_results": limit, "api_key": self.tavily_key},
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()

        return [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                description=item.get("content", ""),
                source="tavily"
            ) for item in data.get("results", [])
        ]

    def _search_exa(self, query: str, limit: int) -> List[SearchResult]:
        """Search using Exa API."""
        headers = {
            "Authorization": f"Bearer {self.exa_key}",
            "Content-Type": "application/json"
        }
        resp = requests.post(
            "https://api.exa.ai/search",
            json={"query": query, "numResults": limit, "useAutoprompt": True},
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()

        return [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                description=item.get("text", "") or item.get("snippet", ""),
                source="exa"
            ) for item in data.get("results", [])
        ]

    def _search_brave(self, query: str, limit: int) -> List[SearchResult]:
        """Search using Brave Search API."""
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.brave_key
        }
        resp = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": query, "count": min(limit, 20)},
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()

        results = []
        if "web" in data and "results" in data["web"]:
            for item in data["web"]["results"]:
                results.append(SearchResult(
                    title=item.get("title", ""),
                    url=item.get("url", ""),
                    description=item.get("description", ""),
                    source="brave"
                ))
        return results

    def _search_ddg(self, query: str, limit: int) -> List[SearchResult]:
        """Search using DuckDuckGo HTML parsing (No API key)."""
        # Using the html endpoint which is easier to parse than the JS-heavy main site
        # Note: This is brittle and should be a last resort.
        # Alternatively, use the 'duckduckgo_search' PyPI package if available in env.

        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = []
                for r in ddgs.text(query, max_results=limit):
                    results.append(SearchResult(
                        title=r['title'],
                        url=r['href'],
                        description=r['body'],
                        source="duckduckgo"
                    ))
                return results
        except ImportError:
            # Fallback to crude requests if lib not installed
            # (Simulated for safety - user should install package)
            logger.info("duckduckgo_search library not found, skipping DDG")
            return []
