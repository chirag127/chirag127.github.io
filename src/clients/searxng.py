"""
SearXNG Universal Search Client - Research Everything.

Uses free SearXNG metasearch for:
- Profitable tool ideas (high traffic, monetizable)
- SEO keyword research (what competitors use)
- Implementation research (how to build)
- Frontend-only project discovery (no backend needed)
- Market validation (existing tools, gaps)
"""

import logging
import os
import random
from typing import Any
from urllib.parse import urlencode

import requests

logger = logging.getLogger("SearXNG")


class SearXNGClient:
    """
    Universal research client using SearXNG metasearch.

    Aggregates results from 70+ search engines:
    - Google, Bing, DuckDuckGo (web)
    - GitHub, GitLab, SourceHut (code)
    - Stack Overflow, Reddit (discussions)
    - arXiv, Google Scholar (research)
    - Amazon, eBay (commercial validation)

    No API key required - uses public instances.
    """

    def __init__(self, base_url: str | None = None):
        # STRICT: Use provided URL or env var. No public fallbacks.
        self.base_url = base_url or os.getenv("SEARXNG_URL")
        if not self.base_url:
            logger.warning("⚠️ SEARXNG_URL not set in environment!")

        self.session = requests.Session()
        # Browser-like headers to avoid blocking
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })
        self.timeout = 30  # Increased timeout for private instance

    # ... (search methods use existing logic but with new headers) ...

    def is_available(self) -> bool:
        """Check if SearXNG is accessible."""
        if not self.base_url:
            return False

        try:
            # Check homepage (HTML) instead of API to pass WAF/rate limits
            response = self.session.get(
                self.base_url,
                timeout=10,
                allow_redirects=True
            )
            return response.status_code == 200 and ("search" in response.text.lower() or "searx" in response.text.lower())
        except Exception:
            return False

    def search(
        self,
        query: str,
        categories: list[str] | None = None,
        engines: list[str] | None = None,
        language: str = "en",
        time_range: str | None = None,
        max_results: int = 20,
    ) -> list[dict[str, Any]]:
        """
        Perform a universal web search using the configured single instance.
        """
        if not self.base_url:
            logger.error("❌ SearXNG URL not configured")
            return []

        params = {
            "q": query,
            "format": "json",
            "language": language,
        }

        if categories:
            params["categories"] = ",".join(categories)
        if engines:
            params["engines"] = ",".join(engines)
        if time_range:
            params["time_range"] = time_range

        try:
            url = f"{self.base_url.rstrip('/')}/search"
            response = self.session.get(url, params=params, timeout=self.timeout)

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])[:max_results]
                logger.info(f"✅ SearXNG: {len(results)} results from {self.base_url}")
                return results
            else:
                logger.error(f"❌ SearXNG Error {response.status_code}: {response.text[:100]}")
                return []

        except Exception as e:
            logger.error(f"❌ SearXNG Request Failed: {e}")
            return []

    # =========================================================================
    # PROFITABLE TOOL DISCOVERY
    # =========================================================================

    def find_profitable_tools(self, category: str = "", max_results: int = 30) -> list[dict]:
        """
        Find profitable online tools with high traffic.

        Args:
            category: pdf, image, video, text, conversion, etc.
            max_results: Maximum results
        """
        queries = [
            f"best free {category} tool online 2026",
            f"popular {category} converter website",
            f"free {category} editor no signup",
            f"online {category} tool million users",
            f"top {category} websites traffic",
            f"alternative to {category} tool free",
            f"{category} tool SaaS free tier",
        ] if category else [
            "best free online tools high traffic",
            "popular web apps millions users",
            "free tools that make money",
            "successful micro SaaS examples",
            "profitable browser-based tools",
            "popular utility websites 2026",
            "free tools with ads revenue",
        ]

        all_results = []
        for q in queries[:5]:
            results = self.search(q, categories=["general"], max_results=10)
            all_results.extend(results)

        return self._dedupe_results(all_results)[:max_results]

    def find_frontend_only_projects(self, topic: str = "", max_results: int = 30) -> list[dict]:
        """
        Find tools that can be built as frontend-only (no backend server needed).

        These are ideal for GitHub Pages deployment.
        """
        queries = [
            f"client-side {topic} tool javascript",
            f"browser-based {topic} no server",
            f"frontend only {topic} web app",
            f"static site {topic} generator",
            f"javascript {topic} library browser",
            f"webassembly {topic} tool",
            f"PWA {topic} offline capable",
        ] if topic else [
            "client-side tools javascript no backend",
            "browser-based apps no server needed",
            "frontend only web applications",
            "static site tools github pages",
            "wasm web tools browser",
            "progressive web apps offline",
            "javascript tools run in browser",
        ]

        all_results = []
        for q in queries[:5]:
            results = self.search(q, categories=["it"], max_results=10)
            all_results.extend(results)

        return self._dedupe_results(all_results)[:max_results]

    # =========================================================================
    # SEO & KEYWORD RESEARCH
    # =========================================================================

    def research_keywords(self, tool_type: str, max_results: int = 20) -> list[dict]:
        """
        Research SEO keywords that competitors use.

        Returns search results showing what keywords work for similar tools.
        """
        queries = [
            f'"{tool_type}" site:github.com',
            f"best {tool_type} online free",
            f"how to {tool_type} online",
            f"{tool_type} alternative free",
            f"{tool_type} without signup",
            f"{tool_type} browser extension",
            f"top 10 {tool_type} tools",
        ]

        all_results = []
        for q in queries[:5]:
            results = self.search(q, max_results=10)
            all_results.extend(results)

        return self._dedupe_results(all_results)[:max_results]

    def extract_seo_keywords(self, results: list[dict]) -> dict[str, int]:
        """
        Extract common keywords from search results for SEO optimization.
        """
        from collections import Counter
        import re

        all_text = ""
        for r in results:
            all_text += f" {r.get('title', '')} {r.get('content', '')}"

        # Clean and extract words
        words = re.findall(r'\b[a-z]{3,15}\b', all_text.lower())

        # Filter common words
        stopwords = {
            "the", "and", "for", "you", "with", "this", "that", "from",
            "are", "was", "were", "been", "being", "have", "has", "had",
            "your", "can", "will", "just", "but", "not", "all", "any",
            "more", "some", "than", "into", "out", "about", "what", "which",
            "their", "there", "here", "when", "where", "how", "why", "www",
            "com", "org", "http", "https", "html", "css", "javascript",
        }

        keywords = [w for w in words if w not in stopwords]
        return dict(Counter(keywords).most_common(50))

    # =========================================================================
    # IMPLEMENTATION RESEARCH
    # =========================================================================

    def research_how_to_build(self, tool_name: str, max_results: int = 20) -> list[dict]:
        """
        Research how to build a specific type of tool.

        Returns tutorials, libraries, and implementation guides.
        """
        queries = [
            f"how to build {tool_name} javascript",
            f"create {tool_name} browser tutorial",
            f"{tool_name} javascript library npm",
            f"build {tool_name} react nextjs",
            f"{tool_name} open source github",
            f"{tool_name} web api tutorial",
            f"implement {tool_name} client-side",
        ]

        all_results = []
        for q in queries[:5]:
            results = self.search(q, categories=["it"], max_results=10)
            all_results.extend(results)

        return self._dedupe_results(all_results)[:max_results]

    def find_libraries(self, functionality: str, max_results: int = 15) -> list[dict]:
        """
        Find JavaScript/WebAssembly libraries for specific functionality.
        """
        queries = [
            f"{functionality} javascript library npm",
            f"{functionality} browser js library",
            f"{functionality} webassembly wasm",
            f"{functionality} client-side library",
            f"best {functionality} js library 2026",
        ]

        all_results = []
        for q in queries[:4]:
            results = self.search(q, categories=["it"], engines=["github", "npm"], max_results=10)
            all_results.extend(results)

        return self._dedupe_results(all_results)[:max_results]

    # =========================================================================
    # MARKET VALIDATION
    # =========================================================================

    def validate_market(self, tool_idea: str, max_results: int = 20) -> dict:
        """
        Validate market for a tool idea.

        Returns:
            - Existing competitors
            - Search volume indicators
            - Gap analysis hints
        """
        existing = self.search(f'"{tool_idea}" online free', max_results=10)
        alternatives = self.search(f"{tool_idea} alternative", max_results=10)
        problems = self.search(f"{tool_idea} not working problem", max_results=5)

        return {
            "existing_tools": existing,
            "alternatives": alternatives,
            "user_problems": problems,
            "competitor_count": len(existing),
            "market_exists": len(existing) > 0,
            "has_gaps": len(problems) > 2,
        }

    def find_underserved_niches(self, category: str = "tools") -> list[dict]:
        """
        Find underserved niches with demand but few solutions.
        """
        queries = [
            f"need free {category} but can't find",
            f"looking for {category} alternative to",
            f"why is there no free {category}",
            f"best {category} too expensive",
            f"free {category} with no limits",
            f"{category} for poor countries",
            f"open source {category} needed",
        ]

        all_results = []
        for q in queries[:5]:
            results = self.search(q, categories=["social media"], time_range="month", max_results=10)
            all_results.extend(results)

        return self._dedupe_results(all_results)

    # =========================================================================
    # MONETIZATION RESEARCH
    # =========================================================================

    def research_monetization(self, tool_type: str) -> list[dict]:
        """
        Research how similar tools monetize.
        """
        queries = [
            f"how does {tool_type} tool make money",
            f"{tool_type} website revenue model",
            f"{tool_type} SaaS pricing",
            f"free {tool_type} with ads",
            f"{tool_type} tool affiliate program",
        ]

        all_results = []
        for q in queries:
            results = self.search(q, max_results=5)
            all_results.extend(results)

        return self._dedupe_results(all_results)

    # =========================================================================
    # CATEGORY-SPECIFIC SEARCHES
    # =========================================================================

    def search_pdf_tools(self) -> list[dict]:
        """Find popular PDF tools and competitors."""
        return self.find_profitable_tools("pdf")

    def search_image_tools(self) -> list[dict]:
        """Find popular image tools and competitors."""
        return self.find_profitable_tools("image")

    def search_video_tools(self) -> list[dict]:
        """Find popular video tools and competitors."""
        return self.find_profitable_tools("video")

    def search_text_tools(self) -> list[dict]:
        """Find popular text/document tools and competitors."""
        return self.find_profitable_tools("text")

    def search_developer_tools(self) -> list[dict]:
        """Find popular developer tools and competitors."""
        return self.find_profitable_tools("developer")

    def search_conversion_tools(self) -> list[dict]:
        """Find popular file conversion tools."""
        return self.find_profitable_tools("converter")

    # =========================================================================
    # COMPREHENSIVE RESEARCH
    # =========================================================================

    def comprehensive_research(self, topic: str) -> dict:
        """
        Perform comprehensive research on a topic for building a tool.

        Returns everything needed to validate, build, and monetize.
        """
        logger.info(f"🔍 Starting comprehensive research on: {topic}")

        return {
            "topic": topic,
            "profitable_examples": self.find_profitable_tools(topic, max_results=20),
            "frontend_only": self.find_frontend_only_projects(topic, max_results=15),
            "how_to_build": self.research_how_to_build(topic, max_results=15),
            "libraries": self.find_libraries(topic, max_results=10),
            "seo_keywords": self.research_keywords(topic, max_results=15),
            "market_validation": self.validate_market(topic),
            "monetization": self.research_monetization(topic),
        }

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def _dedupe_results(self, results: list[dict]) -> list[dict]:
        """Remove duplicate URLs from results."""
        seen = set()
        unique = []
        for r in results:
            url = r.get("url", "")
            if url and url not in seen:
                seen.add(url)
                unique.append(r)
        return unique

    def is_available(self) -> bool:
        """Check if SearXNG is accessible using browser emulation."""
        try:
            # Check homepage (HTML) to pass WAF/rate limits
            response = self.session.get(
                self.base_url,
                timeout=10,
                allow_redirects=True
            )
            return response.status_code == 200 and ("search" in response.text.lower() or "searx" in response.text.lower())
        except Exception:
            return False


# Singleton instance
_client: SearXNGClient | None = None


def get_searxng_client() -> SearXNGClient:
    """Get or create SearXNG client singleton."""
    global _client
    if _client is None:
        _client = SearXNGClient()
    return _client
