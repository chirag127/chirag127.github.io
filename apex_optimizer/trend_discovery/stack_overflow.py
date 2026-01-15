"""
Stack Overflow API Client - Fetches hot questions from Stack Exchange.

Uses official Stack Exchange API (free, no key required for basic usage).
Detects pain points and commonly requested tools.
"""

import logging

import requests

from .base import TrendItem, TrendSource

logger = logging.getLogger("TrendDiscovery.StackOverflow")


class StackOverflowSource(TrendSource):
    """
    Fetches hot questions from Stack Overflow to identify pain points.

    Pain points often translate to tool/extension opportunities.
    """

    API_URL = "https://api.stackexchange.com/2.3"
    SITES = ["stackoverflow"]
    TAGS = ["javascript", "python", "typescript", "react", "node.js", "chrome-extension"]

    def __init__(self, timeout: int = 30):
        super().__init__(timeout)
        self.session = requests.Session()

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        """Fetch hot questions that indicate tool opportunities."""
        trends: list[TrendItem] = []

        # Fetch hot questions
        try:
            hot = self._fetch_hot_questions(limit=20)
            trends.extend(hot)
        except Exception as e:
            logger.warning(f"Failed to fetch SO hot questions: {e}")

        # Fetch high-view questions by tag
        for tag in self.TAGS[:3]:
            try:
                tagged = self._fetch_by_tag(tag, limit=5)
                trends.extend(tagged)
            except Exception as e:
                logger.debug(f"Failed to fetch SO tag {tag}: {e}")

        # Deduplicate and filter for tool opportunities
        seen = set()
        unique = []
        for trend in trends:
            if trend.title not in seen and self._is_tool_opportunity(trend):
                seen.add(trend.title)
                unique.append(trend)

        unique.sort(key=lambda x: x.popularity_score, reverse=True)
        return unique[:limit]

    def _fetch_hot_questions(self, limit: int = 20) -> list[TrendItem]:
        """Fetch current hot questions."""
        url = f"{self.API_URL}/questions"
        params = {
            "site": "stackoverflow",
            "sort": "hot",
            "order": "desc",
            "pagesize": limit,
            "filter": "withbody",
        }

        response = self.session.get(url, params=params, timeout=self.timeout)

        if response.status_code != 200:
            return []

        data = response.json()
        questions = data.get("items", [])

        return [self._question_to_trend(q) for q in questions if q]

    def _fetch_by_tag(self, tag: str, limit: int = 5) -> list[TrendItem]:
        """Fetch high-view questions by tag."""
        url = f"{self.API_URL}/questions"
        params = {
            "site": "stackoverflow",
            "tagged": tag,
            "sort": "votes",
            "order": "desc",
            "pagesize": limit,
            "filter": "withbody",
        }

        response = self.session.get(url, params=params, timeout=self.timeout)

        if response.status_code != 200:
            return []

        data = response.json()
        questions = data.get("items", [])

        return [self._question_to_trend(q) for q in questions if q]

    def _question_to_trend(self, question: dict) -> TrendItem:
        """Convert Stack Overflow question to TrendItem."""
        title = question.get("title", "")
        views = question.get("view_count", 0)
        score = question.get("score", 0)
        answers = question.get("answer_count", 0)
        tags = question.get("tags", [])
        link = question.get("link", "")

        # High views with low answers = pain point
        pain_score = views / max(answers + 1, 1)

        # Calculate popularity
        popularity = self._normalize_score(score + (views / 100), 500)

        # Extract tool idea from question
        tool_idea = self._extract_tool_idea(title)

        description = f"Pain point: {title[:200]}. Views: {views}, Answers: {answers}"

        return TrendItem(
            title=tool_idea,
            description=description,
            source="stackoverflow",
            url=link,
            popularity_score=popularity,
            category=self._detect_category(f"{title} {' '.join(tags)}"),
            keywords=self._extract_keywords(f"{title} {' '.join(tags)}"),
            raw_data={
                "original_question": title,
                "views": views,
                "score": score,
                "answers": answers,
                "tags": tags,
                "pain_score": pain_score,
            },
        )

    def _extract_tool_idea(self, question: str) -> str:
        """Extract a tool idea from a question."""
        # Common question patterns that indicate tool needs
        patterns = [
            ("How to ", ""),
            ("How do I ", ""),
            ("Is there a way to ", ""),
            ("Best way to ", ""),
            ("Tool for ", ""),
            ("Library for ", ""),
        ]

        clean = question
        for prefix, replacement in patterns:
            if clean.lower().startswith(prefix.lower()):
                clean = replacement + clean[len(prefix):]
                break

        # Make it a tool name
        if not any(w in clean.lower() for w in ["tool", "helper", "generator", "manager"]):
            clean = f"{clean[:40]}-Tool"

        return clean[:80]

    def _is_tool_opportunity(self, trend: TrendItem) -> bool:
        """Identify if a question represents a tool opportunity."""
        # Look for questions that could be solved by a tool
        opportunity_keywords = [
            "automate", "generate", "convert", "manage", "organize",
            "track", "monitor", "analyze", "visualize", "format",
            "validate", "lint", "test", "deploy", "build",
        ]

        text = f"{trend.title} {trend.description}".lower()
        return any(kw in text for kw in opportunity_keywords)
