"""
Tests for trend discovery module.
"""

import pytest

from apex_optimizer.trend_discovery.base import TrendCategory, TrendItem, TrendSource


class TestTrendItem:
    """Tests for TrendItem dataclass."""

    def test_create_trend_item(self):
        """Test creating a TrendItem."""
        trend = TrendItem(
            title="Test Tool",
            description="A test tool for testing",
            source="github",
            url="https://github.com/test/test",
            popularity_score=85.0,
            category=TrendCategory.CLI_TOOL,
            keywords=["cli", "test"],
        )

        assert trend.title == "Test Tool"
        assert trend.source == "github"
        assert trend.popularity_score == 85.0
        assert trend.category == TrendCategory.CLI_TOOL

    def test_trend_item_to_dict(self):
        """Test serialization to dict."""
        trend = TrendItem(
            title="Test",
            description="Desc",
            source="hackernews",
            url="https://example.com",
        )

        data = trend.to_dict()

        assert data["title"] == "Test"
        assert data["source"] == "hackernews"
        assert "discovered_at" in data

    def test_trend_item_equality(self):
        """Test equality comparison based on title."""
        trend1 = TrendItem(title="Tool", description="", source="a", url="")
        trend2 = TrendItem(title="tool", description="", source="b", url="")  # Same title, different case

        assert trend1 == trend2  # Should be equal

    def test_trend_item_hash(self):
        """Test hashing for set operations."""
        trend1 = TrendItem(title="Tool", description="", source="a", url="")
        trend2 = TrendItem(title="tool", description="", source="b", url="")

        # Same normalized title should have same hash
        assert hash(trend1) == hash(trend2)


class TestTrendCategory:
    """Tests for TrendCategory enum."""

    def test_categories_exist(self):
        """Test all expected categories exist."""
        assert TrendCategory.WEB_APP
        assert TrendCategory.CHROME_EXTENSION
        assert TrendCategory.CLI_TOOL
        assert TrendCategory.AI_ML
        assert TrendCategory.DEVTOOLS
        assert TrendCategory.UNKNOWN


class MockTrendSource(TrendSource):
    """Mock trend source for testing."""

    def fetch_trends(self, limit: int = 10) -> list[TrendItem]:
        return [
            TrendItem(
                title=f"Test Trend {i}",
                description=f"Description {i}",
                source="mock",
                url=f"https://example.com/{i}",
                popularity_score=100 - i,
            )
            for i in range(limit)
        ]


class TestTrendSource:
    """Tests for TrendSource base class."""

    def test_normalize_score(self):
        """Test score normalization."""
        source = MockTrendSource()

        assert source._normalize_score(50, 100) == 50.0
        assert source._normalize_score(100, 100) == 100.0
        assert source._normalize_score(200, 100) == 100.0  # Capped
        assert source._normalize_score(0, 100) == 0.0

    def test_extract_keywords(self):
        """Test keyword extraction."""
        source = MockTrendSource()

        keywords = source._extract_keywords("A python CLI tool for automation")

        assert "python" in keywords
        assert "cli" in keywords
        assert "tool" in keywords
        assert "automation" in keywords

    def test_detect_category_chrome_extension(self):
        """Test category detection for chrome extension."""
        source = MockTrendSource()

        category = source._detect_category("Chrome extension for productivity")
        assert category == TrendCategory.CHROME_EXTENSION

    def test_detect_category_cli(self):
        """Test category detection for CLI tools."""
        source = MockTrendSource()

        category = source._detect_category("Command line tool for git")
        assert category == TrendCategory.CLI_TOOL

    def test_detect_category_ai(self):
        """Test category detection for AI/ML."""
        source = MockTrendSource()

        category = source._detect_category("LLM-powered AI assistant")
        assert category == TrendCategory.AI_ML

    def test_fetch_trends(self):
        """Test fetching trends from mock source."""
        source = MockTrendSource()

        trends = source.fetch_trends(limit=5)

        assert len(trends) == 5
        assert trends[0].source == "mock"
        assert trends[0].popularity_score > trends[4].popularity_score
