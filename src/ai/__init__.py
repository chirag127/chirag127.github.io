"""
AI Module - Model-Size-Based Unified AI Orchestration.

Dec 2025: Uses MODEL-BASED fallback (not provider-based).
Models ordered by size (405B → 1B) across ALL 6 providers.

Providers: Cerebras, Groq, Gemini, Mistral, NVIDIA, Cloudflare
Strategy: Try largest available model first, regardless of provider.
"""

from .unified_client import UnifiedAIClient, UNIFIED_MODEL_CHAIN
from .base import AIProvider, ModelConfig, ProviderConfig, CompletionResult

__all__ = [
    "UnifiedAIClient",
    "UNIFIED_MODEL_CHAIN",
    "AIProvider",
    "ModelConfig",
    "ProviderConfig",
    "CompletionResult",
]
