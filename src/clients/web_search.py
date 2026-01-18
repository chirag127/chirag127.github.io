"""
Unified Web Search Client.
Supports multiple free/freemium search providers with fallback.

Providers:
1. Brave Search API (1 request/sec free)
2. Exa (Metaphor) API (Free tier available)
3. Tavily API (Free tier available)
4. DDGS - Dux Distributed Global Search (No key required, multi-backend metasearch)
   - Text backends: bing, brave, duckduckgo, google, grokipedia, mojeek, yandex, yahoo, wikipedia
   - Images backend: duckduckgo
   - Videos backend: duckduckgo
   - News backends: bing, duckduckgo, yahoo
   - Books backend: annasarchive
"""

import logging
import os
import requests
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

logger = logging.getLogger("Clients.WebSearch")


@dataclass
class SearchResult:
    """Standard search result for text searches."""
    title: str
    url: str
    description: str
    source: str


@dataclass
class ImageResult:
    """Search result for image searches."""
    title: str
    image_url: str
    thumbnail_url: str
    source_url: str
    width: int
    height: int
    source: str


@dataclass
class VideoResult:
    """Search result for video searches."""
    title: str
    content_url: str
    description: str
    duration: str
    publisher: str
    published: str
    embed_url: str
    thumbnail: str
    view_count: int
    source: str


@dataclass
class NewsResult:
    """Search result for news searches."""
    title: str
    url: str
    body: str
    date: str
    image: str
    source_name: str
    source: str


@dataclass
class BookResult:
    """Search result for book searches."""
    title: str
    author: str
    publisher: str
    info: str
    url: str
    thumbnail: str
    source: str


class WebSearchClient:
    """
    Unified client for web search with automatic fallback.
    Uses DDGS (Dux Distributed Global Search) as the primary metasearch engine
    with multi-backend support for comprehensive results.
    """

    def __init__(self, proxy: Optional[str] = None, timeout: int = 10):
        """
        Initialize the web search client.

        Args:
            proxy: Optional proxy URL (http/https/socks5 supported)
            timeout: Timeout for HTTP requests in seconds
        """
        self.brave_key = os.getenv("BRAVE_API_KEY")
        self.exa_key = os.getenv("EXA_API_KEY")
        self.tavily_key = os.getenv("TAVILY_API_KEY")
        self.proxy = proxy
        self.timeout = timeout

        # Initialize DDGS instance (lazy-loaded)
        self._ddgs = None

    def _get_ddgs(self):
        """Get or initialize DDGS instance."""
        if self._ddgs is None:
            try:
                from ddgs import DDGS
                self._ddgs = DDGS(proxy=self.proxy, timeout=self.timeout)
                logger.info("DDGS metasearch client initialized")
            except ImportError:
                logger.warning("ddgs library not installed. Install with: pip install ddgs")
                raise
        return self._ddgs

    def search(
        self,
        query: str,
        limit: int = 10,
        backend: str = "auto",
        max_retries: int = 3
    ) -> List[SearchResult]:
        """
        Perform web search using available providers in priority order with retry logic.

        Args:
            query: Search query string
            limit: Maximum number of results to return
            backend: DDGS backend(s) - "auto", or specific backends like
                     "bing,google,duckduckgo" (comma-separated)
            max_retries: Maximum number of retry attempts for failed searches

        Returns:
            List of SearchResult objects
        """
        results = []

        # Priority 1: Tavily (Best for RAG/AI)
        if self.tavily_key:
            for attempt in range(max_retries):
                try:
                    results = self._search_tavily(query, limit)
                    if results:
                        return results
                except Exception as e:
                    logger.warning(f"Tavily search attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)

        # Priority 2: Exa (Good for semantic search)
        if self.exa_key:
            for attempt in range(max_retries):
                try:
                    results = self._search_exa(query, limit)
                    if results:
                        return results
                except Exception as e:
                    logger.warning(f"Exa search attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)

        # Priority 3: Brave (Good for general web)
        if self.brave_key:
            for attempt in range(max_retries):
                try:
                    results = self._search_brave(query, limit)
                    if results:
                        return results
                except Exception as e:
                    logger.warning(f"Brave search attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(1)

        # Priority 4: DDGS Metasearch (Fallback with multi-backend support and retry)
        for attempt in range(max_retries):
            try:
                results = self._search_ddgs_text(query, limit, backend=backend)
                if results:
                    return results
            except Exception as e:
                logger.warning(f"DDGS text search attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    # Try different backends on retry
                    if backend == "auto":
                        backend = "bing,duckduckgo,google"  # Skip problematic backends
                    time.sleep(2)

        return []

    def search_comprehensive(
        self,
        query: str,
        limit: int = 10,
        include_images: bool = False,
        include_videos: bool = False,
        include_news: bool = False,
        include_books: bool = False,
        backend: str = "auto"
    ) -> Dict[str, Any]:
        """
        Perform comprehensive search across multiple content types.

        Args:
            query: Search query string
            limit: Maximum results per category
            include_images: Include image search results
            include_videos: Include video search results
            include_news: Include news search results
            include_books: Include book search results
            backend: DDGS backend preference

        Returns:
            Dictionary with results by category:
            {
                "text": List[SearchResult],
                "images": List[ImageResult],
                "videos": List[VideoResult],
                "news": List[NewsResult],
                "books": List[BookResult]
            }
        """
        results = {
            "text": self.search(query, limit, backend),
            "images": [],
            "videos": [],
            "news": [],
            "books": []
        }

        if include_images:
            try:
                results["images"] = self.search_images(query, limit)
            except Exception as e:
                logger.warning(f"Image search failed: {e}")

        if include_videos:
            try:
                results["videos"] = self.search_videos(query, limit)
            except Exception as e:
                logger.warning(f"Video search failed: {e}")

        if include_news:
            try:
                results["news"] = self.search_news(query, limit, backend=backend)
            except Exception as e:
                logger.warning(f"News search failed: {e}")

        if include_books:
            try:
                results["books"] = self.search_books(query, limit)
            except Exception as e:
                logger.warning(f"Book search failed: {e}")

        return results

    def search_images(
        self,
        query: str,
        limit: int = 10,
        size: Optional[str] = None,
        color: Optional[str] = None,
        type_image: Optional[str] = None,
        layout: Optional[str] = None,
        license_image: Optional[str] = None
    ) -> List[ImageResult]:
        """
        Search for images using DDGS.

        Args:
            query: Image search query
            limit: Maximum number of results
            size: Image size filter - "Small", "Medium", "Large", "Wallpaper"
            color: Color filter - "Monochrome", "Red", "Orange", "Yellow", "Green",
                   "Blue", "Purple", "Pink", "Brown", "Black", "Gray", "Teal", "White"
            type_image: Image type - "photo", "clipart", "gif", "transparent", "line"
            layout: Layout filter - "Square", "Tall", "Wide"
            license_image: License filter - "any", "Public", "Share",
                          "ShareCommercially", "Modify", "ModifyCommercially"

        Returns:
            List of ImageResult objects
        """
        try:
            ddgs = self._get_ddgs()
            raw_results = ddgs.images(
                query=query,
                max_results=limit,
                size=size,
                color=color,
                type_image=type_image,
                layout=layout,
                license_image=license_image
            )

            return [
                ImageResult(
                    title=r.get("title", ""),
                    image_url=r.get("image", ""),
                    thumbnail_url=r.get("thumbnail", ""),
                    source_url=r.get("url", ""),
                    width=r.get("width", 0),
                    height=r.get("height", 0),
                    source=r.get("source", "ddgs")
                )
                for r in raw_results
            ]
        except ImportError:
            logger.warning("ddgs library not installed for image search")
            return []

    def search_videos(
        self,
        query: str,
        limit: int = 10,
        resolution: Optional[str] = None,
        duration: Optional[str] = None,
        license_videos: Optional[str] = None
    ) -> List[VideoResult]:
        """
        Search for videos using DDGS.

        Args:
            query: Video search query
            limit: Maximum number of results
            resolution: Resolution filter - "high", "standard"
            duration: Duration filter - "short", "medium", "long"
            license_videos: License filter - "creativeCommon", "youtube"

        Returns:
            List of VideoResult objects
        """
        try:
            ddgs = self._get_ddgs()
            raw_results = ddgs.videos(
                query=query,
                max_results=limit,
                resolution=resolution,
                duration=duration,
                license_videos=license_videos
            )

            return [
                VideoResult(
                    title=r.get("title", ""),
                    content_url=r.get("content", ""),
                    description=r.get("description", ""),
                    duration=r.get("duration", ""),
                    publisher=r.get("publisher", ""),
                    published=r.get("published", ""),
                    embed_url=r.get("embed_url", ""),
                    thumbnail=r.get("images", {}).get("medium", "") if isinstance(r.get("images"), dict) else "",
                    view_count=r.get("statistics", {}).get("viewCount", 0) if isinstance(r.get("statistics"), dict) else 0,
                    source=r.get("provider", "ddgs")
                )
                for r in raw_results
            ]
        except ImportError:
            logger.warning("ddgs library not installed for video search")
            return []

    def search_news(
        self,
        query: str,
        limit: int = 10,
        timelimit: Optional[str] = None,
        backend: str = "auto"
    ) -> List[NewsResult]:
        """
        Search for news using DDGS.

        Args:
            query: News search query
            limit: Maximum number of results
            timelimit: Time filter - "d" (day), "w" (week), "m" (month)
            backend: Backend(s) to use - "auto", "bing", "duckduckgo", "yahoo"

        Returns:
            List of NewsResult objects
        """
        try:
            ddgs = self._get_ddgs()
            raw_results = ddgs.news(
                query=query,
                max_results=limit,
                timelimit=timelimit,
                backend=backend
            )

            return [
                NewsResult(
                    title=r.get("title", ""),
                    url=r.get("url", ""),
                    body=r.get("body", ""),
                    date=r.get("date", ""),
                    image=r.get("image", ""),
                    source_name=r.get("source", ""),
                    source="ddgs"
                )
                for r in raw_results
            ]
        except ImportError:
            logger.warning("ddgs library not installed for news search")
            return []

    def search_books(
        self,
        query: str,
        limit: int = 10,
        backend: str = "auto"
    ) -> List[BookResult]:
        """
        Search for books using DDGS (Anna's Archive backend).

        Args:
            query: Book search query (title, author, ISBN, etc.)
            limit: Maximum number of results
            backend: Backend to use (default: annasarchive)

        Returns:
            List of BookResult objects
        """
        try:
            ddgs = self._get_ddgs()
            raw_results = ddgs.books(
                query=query,
                max_results=limit,
                backend=backend
            )

            return [
                BookResult(
                    title=r.get("title", ""),
                    author=r.get("author", ""),
                    publisher=r.get("publisher", ""),
                    info=r.get("info", ""),
                    url=r.get("url", ""),
                    thumbnail=r.get("thumbnail", ""),
                    source="annasarchive"
                )
                for r in raw_results
            ]
        except ImportError:
            logger.warning("ddgs library not installed for book search")
            return []

    def _search_tavily(self, query: str, limit: int) -> List[SearchResult]:
        """Search using Tavily API."""
        resp = requests.post(
            "https://api.tavily.com/search",
            json={"query": query, "max_results": limit, "api_key": self.tavily_key},
            timeout=self.timeout
        )
        resp.raise_for_status()
        data = resp.json()

        return [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                description=item.get("content", ""),
                source="tavily"
            )
            for item in data.get("results", [])
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
            timeout=self.timeout
        )
        resp.raise_for_status()
        data = resp.json()

        return [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                description=item.get("text", "") or item.get("snippet", ""),
                source="exa"
            )
            for item in data.get("results", [])
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
            timeout=self.timeout
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

    def _search_ddgs_text(
        self,
        query: str,
        limit: int,
        region: str = "us-en",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        backend: str = "auto"
    ) -> List[SearchResult]:
        """
        Search using DDGS text metasearch with multi-backend support.

        Args:
            query: Search query
            limit: Maximum number of results
            region: Region code (e.g., "us-en", "uk-en", "ru-ru")
            safesearch: SafeSearch setting - "on", "moderate", "off"
            timelimit: Time limit - "d" (day), "w" (week), "m" (month), "y" (year)
            backend: Backend(s) - "auto" or comma-separated list:
                     "bing,brave,duckduckgo,google,grokipedia,mojeek,yandex,yahoo,wikipedia"

        Returns:
            List of SearchResult objects from multiple backends
        """
        try:
            ddgs = self._get_ddgs()
            raw_results = ddgs.text(
                query=query,
                region=region,
                safesearch=safesearch,
                timelimit=timelimit,
                max_results=limit,
                backend=backend
            )

            return [
                SearchResult(
                    title=r.get("title", ""),
                    url=r.get("href", ""),
                    description=r.get("body", ""),
                    source="ddgs"
                )
                for r in raw_results
            ]
        except ImportError:
            logger.warning("ddgs library not installed. Install with: pip install ddgs")
            return []


def search_everything(
    query: str,
    limit: int = 10,
    backend: str = "auto"
) -> Dict[str, Any]:
    """
    Convenience function for comprehensive search across all content types.

    Args:
        query: Search query string
        limit: Maximum results per category
        backend: DDGS backend preference

    Returns:
        Dictionary with results from text, images, videos, news, and books
    """
    client = WebSearchClient()
    return client.search_comprehensive(
        query=query,
        limit=limit,
        include_images=True,
        include_videos=True,
        include_news=True,
        include_books=True,
        backend=backend
    )
