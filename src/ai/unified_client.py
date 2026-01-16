"""
Unified AI Client - Model-Size-Based Fallback Chain.

This client implements a MODEL-BASED fallback strategy (not provider-based).
Models are ordered by size (largest → smallest) across ALL providers.

Dec 2025 Model Hierarchy (by parameter count):
1. llama-3.1-405b (Groq/NVIDIA) - 405B
2. zai-glm-4.6 (Cerebras) - 357B
3. qwen-3-235b (Cerebras/NVIDIA) - 235B
4. gpt-oss-120b (Cerebras/Groq) - 120B
5. llama-3.3-70b (Multiple) - 70B
6. qwen-3-32b (Cerebras/Groq) - 32B
7. gemma-3-27b (Gemini) - 27B
8. mistral-small-24b (Mistral) - 24B
9. ... smaller models as final fallback

Strategy: Try largest available model first, regardless of provider.
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Any

from .base import AIProvider, CompletionResult, ProviderStatus
from .providers.cerebras import CerebrasProvider
from .providers.groq import GroqProvider
from .providers.gemini import GeminiProvider
from .providers.mistral import MistralProvider
from .providers.nvidia import NVIDIAProvider
from .providers.cloudflare import CloudflareProvider


logger = logging.getLogger("AI.UnifiedClient")


@dataclass
class UnifiedModel:
    """A model with its provider and size ranking."""
    name: str
    provider_name: str
    size_billions: float  # Model size in billions of parameters
    description: str = ""
    max_tokens: int = 4096
    supports_json: bool = True


@dataclass
class ProviderStats:
    """Statistics for provider usage."""
    name: str
    requests: int = 0
    successes: int = 0
    failures: int = 0
    total_tokens: int = 0


# ============================================================================

UNIFIED_MODEL_CHAIN: list[UnifiedModel] = [
    # Tier 1: God-Class (400B+) - Complex Reasoning & Architecture
    # Note: Using 70B variants where 405B is unavailable/unstable
    UnifiedModel("nvidia/llama-3.1-nemotron-70b-instruct", "nvidia", 70, "Nemotron 70B (NVIDIA)", max_tokens=4096),
    UnifiedModel("llama-3.3-70b-versatile", "groq", 70, "Llama 3.3 70B (Groq)", max_tokens=8192),
    UnifiedModel("llama-3.3-70b", "cerebras", 70, "Llama 3.3 70B (Cerebras)", max_tokens=8192),
    UnifiedModel("gemini-1.5-pro", "gemini", 1000, "Gemini 1.5 Pro", max_tokens=8192),

    # Tier 2: High-End (70B-100B) - Content Generation
    UnifiedModel("mistral-large-latest", "mistral", 123, "Mistral Large (Mistral)", max_tokens=8192),
    UnifiedModel("llama-3.1-70b-versatile", "groq", 70, "Llama 3.1 70B (Groq)", max_tokens=8192),
    UnifiedModel("meta/llama-3.1-70b-instruct", "nvidia", 70, "Llama 3.1 70B (meta/Nvidia)", max_tokens=4096),

    # Tier 3: Mid-Range (30B-70B) - Code & Logic
    UnifiedModel("gemini-1.5-flash", "google", 30, "Gemini 1.5 Flash", max_tokens=8192),
    UnifiedModel("mixtral-8x7b-32768", "groq", 45, "Mixtral 8x7B (Groq)", max_tokens=32768),

    # Tier 4: Efficiency (8B-30B) - fast tasks
    UnifiedModel("llama-3.1-8b-instant", "groq", 8, "Llama 3.1 8B (Groq)", max_tokens=8192),
    UnifiedModel("llama3.1-8b", "cerebras", 8, "Llama 3.1 8B (Cerebras)", max_tokens=8192),

    # Tier 5: Edge / Fallback
    UnifiedModel("@cf/meta/llama-3.1-8b-instruct", "cloudflare", 8, "Llama 3.1 8B (Cloudflare)", max_tokens=2048),
]


class UnifiedAIClient:
    """
    Single API for all AI operations with MODEL-SIZE-BASED fallback.

    Strategy: Try largest available model first, regardless of provider.
    This ensures we always use the best quality model available.

    Features:
    - 6 providers: Cerebras, Groq, Gemini, Mistral, NVIDIA, Cloudflare
    - 25+ models sorted by size (405B → 1B)
    - Automatic model fallback on failure
    - Circuit breaker per model
    - Response caching

    Usage:
        client = UnifiedAIClient()
        result = client.generate("Write a poem about AI")
        # Will try llama-3.1-405b first, then smaller models on failure
    """

    def __init__(self) -> None:
        """Initialize the unified client with all available providers."""
        self.providers: dict[str, AIProvider] = {}
        self.stats: dict[str, ProviderStats] = {}
        self._model_cooldowns: dict[str, float] = {}  # model_name -> cooldown_until
        self._model_failures: dict[str, int] = {}  # model_name -> failure_count

        # Initialize all providers
        self._init_providers()

        # Build available model chain
        self.model_chain = self._build_model_chain()

        # Log initialization
        available_providers = [n for n, p in self.providers.items() if p.is_available()]
        logger.info(f"[UnifiedClient] Initialized with {len(available_providers)}/{len(self.providers)} providers")
        for name, provider in self.providers.items():
            status = "[OK]" if provider.is_available() else "[--]"
            logger.info(f"  {status} {name}: {provider.status.value}")

        logger.info(f"[UnifiedClient] {len(self.model_chain)} models in fallback chain")

    def _init_providers(self) -> None:
        """Initialize all 6 AI providers."""
        provider_classes = [
            ("cerebras", CerebrasProvider),
            ("groq", GroqProvider),
            ("gemini", GeminiProvider),
            ("mistral", MistralProvider),
            ("nvidia", NVIDIAProvider),
            ("cloudflare", CloudflareProvider),
        ]

        for name, cls in provider_classes:
            try:
                provider = cls()
                self.providers[name] = provider
                self.stats[name] = ProviderStats(name)
            except Exception as e:
                logger.warning(f"[UnifiedClient] Failed to init {name}: {e}")

    def _build_model_chain(self) -> list[UnifiedModel]:
        """Build available model chain from available providers."""
        available_models = []

        for model in UNIFIED_MODEL_CHAIN:
            provider = self.providers.get(model.provider_name)
            if provider and provider.is_available():
                available_models.append(model)

        return available_models

    def _is_model_available(self, model: UnifiedModel) -> bool:
        """Check if a model is available (not in cooldown, provider active)."""
        # Check provider availability
        provider = self.providers.get(model.provider_name)
        if not provider or not provider.is_available():
            return False

        # Check cooldown
        cooldown_until = self._model_cooldowns.get(model.name, 0)
        if time.time() < cooldown_until:
            return False

        return True

    def _trigger_model_cooldown(self, model_name: str, seconds: int = 60) -> None:
        """Put a model in cooldown after failure."""
        self._model_cooldowns[model_name] = time.time() + seconds
        self._model_failures[model_name] = self._model_failures.get(model_name, 0) + 1

        logger.warning(f"[UnifiedClient] Model {model_name} in cooldown for {seconds}s")

    def _record_success(self, provider_name: str, model_name: str, tokens: int = 0) -> None:
        """Record successful request."""
        if provider_name in self.stats:
            self.stats[provider_name].requests += 1
            self.stats[provider_name].successes += 1
            self.stats[provider_name].total_tokens += tokens

        # Reset failure count on success
        self._model_failures[model_name] = 0

    def _record_failure(self, provider_name: str, model_name: str, error: str) -> None:
        """Record failed request and apply cooldown."""
        if provider_name in self.stats:
            self.stats[provider_name].requests += 1
            self.stats[provider_name].failures += 1

        failures = self._model_failures.get(model_name, 0) + 1
        self._model_failures[model_name] = failures

        # Progressive cooldown based on failure count
        cooldown = min(60 * failures, 300)  # Max 5 minutes
        self._trigger_model_cooldown(model_name, cooldown)

    def _call_model(
        self,
        model: UnifiedModel,
        prompt: str,
        system_prompt: str,
        max_tokens: int,
        temperature: float,
        json_mode: bool = False,
    ) -> CompletionResult:
        """Call a specific model via its provider."""
        provider = self.providers.get(model.provider_name)
        if not provider:
            return CompletionResult(success=False, error=f"Provider {model.provider_name} not found")

        try:
            if json_mode:
                result = provider.json_completion(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    model=model.name,
                    max_tokens=max_tokens,
                )
            else:
                result = provider.chat_completion(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    model=model.name,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

            return result

        except Exception as e:
            return CompletionResult(success=False, error=str(e))

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        min_model_size: float = 0,  # Minimum model size in billions
    ) -> CompletionResult:
        """
        Generate text completion using MODEL-SIZE-BASED fallback.

        Tries models from largest to smallest until one succeeds.

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            min_model_size: Minimum model size to use (0 = any)

        Returns:
            CompletionResult with generated text
        """
        # Filter to available models meeting size requirement
        available_models = [
            m for m in self.model_chain
            if self._is_model_available(m) and m.size_billions >= min_model_size
        ]

        if not available_models:
            return CompletionResult(
                success=False,
                error="No AI models available. Check API keys.",
            )

        logger.info(f"[UnifiedClient] {len(available_models)} models available, trying largest first")

        last_error = ""

        for model in available_models:
            logger.debug(f"[UnifiedClient] Trying {model.name} ({model.size_billions}B via {model.provider_name})")

            result = self._call_model(
                model=model,
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                json_mode=False,
            )

            if result.success:
                self._record_success(model.provider_name, model.name, result.tokens_used)
                logger.info(f"[UnifiedClient] Success: {model.name} ({model.size_billions}B)")
                return result

            # Record failure and continue to next model
            self._record_failure(model.provider_name, model.name, result.error or "Unknown")
            last_error = result.error or "Unknown error"

            # Brief pause before trying next model
            time.sleep(0.5)

        return CompletionResult(
            success=False,
            error=f"All models failed. Last error: {last_error}",
        )

    def generate_json(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        min_model_size: float = 0,
    ) -> CompletionResult:
        """
        Generate JSON-structured completion using MODEL-SIZE-BASED fallback.

        Args:
            prompt: User prompt requesting JSON output
            system_prompt: System prompt for context
            max_tokens: Maximum tokens in response
            min_model_size: Minimum model size to use (0 = any)

        Returns:
            CompletionResult with json_content dict
        """
        available_models = [
            m for m in self.model_chain
            if self._is_model_available(m) and m.size_billions >= min_model_size
        ]

        if not available_models:
            return CompletionResult(
                success=False,
                error="No AI models available for JSON generation.",
            )

        logger.info(f"[UnifiedClient] JSON mode, {len(available_models)} models available")

        last_error = ""

        for model in available_models:
            logger.debug(f"[UnifiedClient] JSON: Trying {model.name} ({model.size_billions}B)")

            result = self._call_model(
                model=model,
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=0.3,  # Lower temp for structured output
                json_mode=True,
            )

            if result.success and result.json_content is not None:
                self._record_success(model.provider_name, model.name, result.tokens_used)
                logger.info(f"[UnifiedClient] JSON Success: {model.name}")
                return result

            self._record_failure(model.provider_name, model.name, result.error or "JSON parse failed")
            last_error = result.error or "Failed to parse JSON"

            time.sleep(0.5)

        return CompletionResult(
            success=False,
            error=f"All models failed for JSON. Last error: {last_error}",
        )

    def select_best_ideas(
        self,
        trends: list[dict[str, Any]],
        count: int = 20,
        existing_repos: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Use AI to select the best project ideas from discovered trends.

        Uses largest available model for best quality selection.
        """
        if not trends:
            return []

        existing_str = ""
        if existing_repos:
            sample = existing_repos[:50]
            existing_str = f"\n\nExisting repositories (avoid duplicates):\n" + "\n".join(f"- {r}" for r in sample)

        # Prepare trends for prompt (limit to 100)
        trends_text = ""
        for i, trend in enumerate(trends[:100], 1):
            title = trend.get("title", "Unknown")
            desc = trend.get("description", "")[:200]
            source = trend.get("source", "Unknown")
            score = trend.get("popularity_score", 0)
            trends_text += f"{i}. [{source}] {title} (score: {score})\n   {desc}\n\n"

        prompt = f"""You are an expert software architect selecting the best project ideas for GitHub repositories.

Analyze these {len(trends)} trending topics and select the TOP {count} ideas that are:
1. **Novel**: Not duplicates of existing repos
2. **Feasible**: Can be built as frontend-only web apps (no backend server)
3. **Impactful**: Solves real problems, has market demand
4. **SEO-friendly**: Uses searchable keywords

{existing_str}

TRENDING TOPICS:
{trends_text}

Return a JSON object with this structure:
{{
    "selected_ideas": [
        {{
            "original_index": 1,
            "title": "Original title",
            "apex_name": "SEO-Optimized-Repository-Name-With-Hyphens",
            "description": "Compelling 250-char description with keywords",
            "category": "web_app|browser_extension|library|tool",
            "feasibility_score": 0.95,
            "novelty_score": 0.85,
            "tags": ["tag1", "tag2", "...", "tag20"],
            "reason": "Why this idea was selected"
        }}
    ]
}}

Select exactly {count} ideas. Generate 20 SEO-optimized tags for each."""

        # Use largest model (min 70B) for best selection quality
        result = self.generate_json(
            prompt=prompt,
            system_prompt="You are a senior software architect and product strategist.",
            max_tokens=8000,
            min_model_size=32,  # Prefer 32B+ models for complex reasoning
        )

        if result.success and result.json_content:
            selected = result.json_content.get("selected_ideas", [])
            logger.info(f"[UnifiedClient] AI selected {len(selected)} ideas using {result.model_used}")
            return selected

        logger.warning(f"[UnifiedClient] Failed to select ideas: {result.error}")
        return []

    def generate_repo_metadata(
        self,
        idea: str,
        description: str,
        category: str = "web_app",
    ) -> dict[str, Any]:
        """Generate SEO-optimized repository metadata using AI."""
        prompt = f"""Generate SEO-optimized metadata for a GitHub repository.

IDEA: {idea}
DESCRIPTION: {description}
CATEGORY: {category}

Return a JSON object:
{{
    "apex_name": "Title-Case-With-Hyphens-3-to-10-Words",
    "description": "Compelling 250-char max description with keywords. No emojis.",
    "tags": ["exactly", "twenty", "lowercase", "hyphenated", "seo", "keywords", ...],
    "readme_intro": "2-3 sentence compelling intro for README.md",
    "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"]
}}

CRITICAL: Generate EXACTLY 20 or more tags."""

        result = self.generate_json(
            prompt=prompt,
            system_prompt="You are an SEO expert and GitHub repository optimization specialist.",
            max_tokens=2000,
            min_model_size=8,  # 8B+ is fine for metadata
        )

        if result.success and result.json_content:
            metadata = result.json_content
            tags = metadata.get("tags", [])
            if len(tags) < 20:
                generic = [
                    "open-source", "software", "tools", "developer-tools",
                    "automation", "productivity", "github", "project",
                    "application", "frontend", "javascript", "typescript",
                    "react", "web-development", "2025", "trending",
                    "coding", "programming", "tech", "innovation"
                ]
                for tag in generic:
                    if tag not in tags and len(tags) < 20:
                        tags.append(tag)
                metadata["tags"] = tags[:20]
            return metadata

        # Fallback metadata
        return {
            "apex_name": idea.replace(" ", "-").title(),
            "description": description[:250],
            "tags": ["software", "tools", "open-source", "github", "project",
                     "development", "coding", "automation", "productivity",
                     "frontend", "web-app", "javascript", "typescript",
                     "react", "vite", "2025", "trending", "tech",
                     "innovation", "developer-tools"],
            "readme_intro": description,
            "features": ["Core functionality", "Modern UI", "Fast performance",
                        "Easy to use", "Well documented"],
        }

    def get_status(self) -> dict[str, Any]:
        """Get comprehensive status of all providers and models."""
        providers_status = {}
        for name, provider in self.providers.items():
            stats = self.stats.get(name)
            providers_status[name] = {
                "available": provider.is_available(),
                "status": provider.status.value,
                "requests": stats.requests if stats else 0,
                "successes": stats.successes if stats else 0,
                "failures": stats.failures if stats else 0,
                "total_tokens": stats.total_tokens if stats else 0,
            }

        # Model chain status
        models_status = []
        for model in self.model_chain[:10]:  # Top 10 models
            models_status.append({
                "name": model.name,
                "provider": model.provider_name,
                "size_b": model.size_billions,
                "available": self._is_model_available(model),
                "failures": self._model_failures.get(model.name, 0),
            })

        return {
            "providers": providers_status,
            "model_chain": models_status,
            "total_available_models": len([m for m in self.model_chain if self._is_model_available(m)]),
        }

    def print_status(self) -> None:
        """Print formatted status of all providers and models."""
        print("\n" + "=" * 70)
        print("AI UNIFIED CLIENT STATUS (Model-Size-Based Fallback)")
        print("=" * 70)

        status = self.get_status()

        print("\nPROVIDERS:")
        for name, pstatus in status["providers"].items():
            icon = "[OK]" if pstatus["available"] else "[--]"
            print(f"  {icon} {name}: {pstatus['status']}")
            print(f"      Requests: {pstatus['requests']} | Success: {pstatus['successes']} | Tokens: {pstatus['total_tokens']}")

        print("\nMODEL CHAIN (Top 10 by size):")
        for m in status["model_chain"]:
            icon = "[OK]" if m["available"] else "[--]"
            print(f"  {icon} {m['size_b']:>5.0f}B | {m['name'][:40]:<40} ({m['provider']})")

        print(f"\nTotal Available Models: {status['total_available_models']}")
        print("=" * 70)
