"""
AI Module - Model-Size-Based Unified AI Orchestration.

Dec 2025: Uses MODEL-BASED fallback (not provider-based).
Models ordered by size (405B → 1B) across ALL 6 providers.

Providers: Cerebras, Groq, Gemini, Mistral, NVIDIA, Cloudflare
Strategy: Try largest available model first, regardless of provider.
"""

# Use lazy imports to avoid circular import issues
def __getattr__(name):
    """Lazy import to prevent circular imports."""
    if name == "UnifiedAIClient":
        from .unified_client import UnifiedAIClient
        return UnifiedAIClient
    elif name == "UNIFIED_MODEL_CHAIN":
        from .unified_client import UNIFIED_MODEL_CHAIN
        return UNIFIED_MODEL_CHAIN
    elif name == "AIProvider":
        from .base import AIProvider
        return AIProvider
    elif name == "ModelConfig":
        from .base import ModelConfig
        return ModelConfig
    elif name == "ProviderConfig":
        from .base import ProviderConfig
        return ProviderConfig
    elif name == "CompletionResult":
        from .base import CompletionResult
        return CompletionResult
    raise AttributeError(f"module 'src.ai' has no attribute '{name}'")

__all__ = [
    "UnifiedAIClient",
    "UNIFIED_MODEL_CHAIN",
    "AIProvider",
    "ModelConfig",
    "ProviderConfig",
    "CompletionResult",
]
