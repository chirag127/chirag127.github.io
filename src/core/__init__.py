"""
Apex Optimizer - AI-Powered Repository Management Suite.

Components:
- Budget Manager: 100 session/day limit enforcement
- Cache Manager: Persistent caching for API responses
- Clients: Jules, GitHub, Cerebras, Groq API clients
- Deduplication: Fuzzy matching for trend classification
- Repository Analyzer: AI-powered repo analysis
- Repository Factory: Private repo creation
- Session Manager: Jules session lifecycle
- Trend Discovery: Multi-source trend aggregation
"""

from .budget_manager import BudgetManager
from .cache import CacheManager
from .config import Settings
from .session_manager import SessionManager

__all__ = [
    "BudgetManager",
    "CacheManager",
    "SessionManager",
    "Settings",
]

__version__ = "2.0.0"
