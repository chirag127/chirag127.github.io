# Use lazy imports to avoid circular import issues
def __getattr__(name):
    """Lazy import to prevent circular imports."""
    if name == "CerebrasProvider":
        from .cerebras import CerebrasProvider
        return CerebrasProvider
    elif name == "GroqProvider":
        from .groq import GroqProvider
        return GroqProvider
    elif name == "NVIDIAProvider":
        from .nvidia import NVIDIAProvider
        return NVIDIAProvider
    elif name == "MistralProvider":
        from .mistral import MistralProvider
        return MistralProvider
    elif name == "GeminiProvider":
        from .gemini import GeminiProvider
        return GeminiProvider
    elif name == "CloudflareProvider":
        from .cloudflare import CloudflareProvider
        return CloudflareProvider
    elif name == "OpenRouterProvider":
        from .openrouter import OpenRouterProvider
        return OpenRouterProvider
    elif name == "GitHubModelsProvider":
        from .github import GitHubModelsProvider
        return GitHubModelsProvider
    raise AttributeError(f"module 'src.ai.providers' has no attribute '{name}'")

__all__ = [
    "CerebrasProvider",
    "GroqProvider",
    "NVIDIAProvider",
    "MistralProvider",
    "GeminiProvider",
    "CloudflareProvider",
    "OpenRouterProvider",
    "GitHubModelsProvider",
]
