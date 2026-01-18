"""
Unified AI Client - Model-Size-Based Fallback Chain.

This client implements a MODEL-BASED fallback strategy.
Models are ordered by size (largest → smallest) across ALL providers.

Strategy: Try largest available model first, regardless of provider.
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Any

from .base import AIProvider, CompletionResult, ProviderStatus
from .providers import (
    CerebrasProvider,
    GroqProvider,
    GeminiProvider,
    MistralProvider,
    NVIDIAProvider,
    CloudflareProvider,
    OpenRouterProvider,
    GitHubModelsProvider,
)
from .models import UNIFIED_MODEL_CHAIN, UnifiedModel, MODEL_COUNT


logger = logging.getLogger("AI.UnifiedClient")

@dataclass
class ProviderStats:
    """Statistics for provider usage."""
    name: str
    requests: int = 0
    successes: int = 0
    failures: int = 0
    total_tokens: int = 0


class UnifiedAIClient:
    """
    Single API for all AI operations with MODEL-SIZE-BASED fallback.

    Features:
    - 8 FREE providers: Cerebras, Groq, Gemini, Mistral, NVIDIA, Cloudflare, OpenRouter, GitHub
    - 45+ models sorted by size
    - Automatic model fallback on failure
    - Circuit breaker per model
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
        """Initialize 8 free-forever AI providers."""
        provider_classes = [
            ("groq", GroqProvider),
            ("cerebras", CerebrasProvider),
            ("nvidia", NVIDIAProvider),
            ("cloudflare", CloudflareProvider),
            ("openrouter", OpenRouterProvider),
            ("github", GitHubModelsProvider),
            ("gemini", GeminiProvider),
            ("mistral", MistralProvider),
        ]

        for name, cls in provider_classes:
            try:
                provider = cls()
                self.providers[name] = provider
                self.stats[name] = ProviderStats(name)
            except Exception as e:
                logger.warning(f"[UnifiedClient] Failed to init {name}: {e}")

    def _build_model_chain(self) -> list[UnifiedModel]:
        """Build available model chain from available providers, sorted by size (largest first)."""
        available_models = []

        for model in UNIFIED_MODEL_CHAIN:
            # Check availability (+ optional working flag check if desired)
            pname = model.provider
            if self.providers.get(pname) and self.providers[pname].is_available():
                available_models.append(model)

        # Sort by priority (highest first) then size (largest first)
        return sorted(available_models, key=lambda m: (m.priority, m.size_billions), reverse=True)

    def _is_model_available(self, model: UnifiedModel) -> bool:
        """Check if a model is available."""
        provider = self.providers.get(model.provider)
        if not provider or not provider.is_available():
            return False

        cooldown_key = f"{model.provider}:{model.api_model_id}"
        cooldown_until = self._model_cooldowns.get(cooldown_key, 0)
        return time.time() >= cooldown_until

    def _trigger_model_cooldown(self, model_name: str, seconds: int = 60) -> None:
        """Put a model in cooldown after failure."""
        self._model_cooldowns[model_name] = time.time() + seconds
        self._model_failures[model_name] = self._model_failures.get(model_name, 0) + 1

        logger.warning(f"[UnifiedClient] Model {model_name} in cooldown for {seconds}s")

    def _call_model(
        self,
        model: UnifiedModel,
        prompt: str,
        system_prompt: str,
        max_tokens: int,
        temperature: float,
        json_mode: bool = False,
    ) -> CompletionResult:
        """
        Call a model via its configured provider.
        """
        # Use adaptive timeout based on model size
        timeout = model.timeout_seconds

        provider_name = model.provider
        model_id = model.api_model_id

        logger.info(f"[UnifiedClient] 🚀 Calling {model.name} ({model.size_billions}B) via {provider_name}")

        # Check availability
        provider = self.providers.get(provider_name)
        if not provider or not provider.is_available():
            err = f"Provider {provider_name} not available"
            logger.debug(f"[UnifiedClient] {err}")
            return CompletionResult(success=False, error=err)

        # Check cooldown
        cooldown_key = f"{provider_name}:{model_id}"
        cooldown_until = self._model_cooldowns.get(cooldown_key, 0)
        if time.time() < cooldown_until:
            err = f"{cooldown_key} in cooldown"
            logger.debug(f"[UnifiedClient] {err}")
            return CompletionResult(success=False, error=err)

        try:
            if json_mode:
                result = provider.json_completion(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    model=model_id,
                    max_tokens=max_tokens,
                    timeout=timeout,
                )
            else:
                result = provider.chat_completion(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    model=model_id,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    timeout=timeout,
                )

            if result.success:
                logger.info(f"[UnifiedClient] ✅ Success: {model_id} via {provider_name}")
                # Update stats
                if provider_name in self.stats:
                    self.stats[provider_name].requests += 1
                    self.stats[provider_name].successes += 1
                    self.stats[provider_name].total_tokens += result.tokens_used
                # Clear failure count
                self._model_failures[cooldown_key] = 0
                return result

            # Provider returned but failed
            last_error = result.error or "Unknown error"
            logger.warning(f"[UnifiedClient] ❌ Failed: {model_id} via {provider_name}: {last_error}")

            # Put this specific provider:model in cooldown
            if provider_name in self.stats:
                self.stats[provider_name].requests += 1
                self.stats[provider_name].failures += 1

            failures = self._model_failures.get(cooldown_key, 0) + 1
            self._model_failures[cooldown_key] = failures
            cooldown = min(60 * failures, 300)  # Max 5 minutes
            self._model_cooldowns[cooldown_key] = time.time() + cooldown

            return CompletionResult(success=False, error=last_error)

        except Exception as e:
            last_error = str(e)
            logger.warning(f"[UnifiedClient] ❌ Exception: {model_id} via {provider_name}: {last_error}")
            return CompletionResult(success=False, error=last_error)

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        min_model_size: float = 0,
    ) -> CompletionResult:
        """Generate text completion using MODEL-SIZE-BASED fallback."""
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
            result = self._call_model(
                model=model,
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                json_mode=False,
            )

            if result.success:
                return result

            last_error = result.error or "Unknown error"
            time.sleep(0.5)

        return CompletionResult(
            success=False,
            error=f"All models failed. Last error: {last_error}",
        )

    def generate_with_tier(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
        start_tier: int = 0,
    ) -> CompletionResult:
        """
        Generate text completion starting from a specific tier (index) in the model chain.
        Useful for saving the largest models for critical tasks.
        """
        available_models = [
            m for m in self.model_chain
            if self._is_model_available(m)
        ]

        # Apply tier offset (skip top N models)
        if start_tier > 0 and start_tier < len(available_models):
            available_models = available_models[start_tier:]

        if not available_models:
            return CompletionResult(
                success=False,
                error="No AI models available for this tier. Check API keys or reduce start_tier.",
            )

        logger.info(f"[UnifiedClient] Tier {start_tier} generation, {len(available_models)} models available")

        last_error = ""

        for model in available_models:
            result = self._call_model(
                model=model,
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                json_mode=False,
            )

            if result.success:
                return result

            last_error = result.error or "Unknown error"
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
        """Generate JSON-structured completion using MODEL-SIZE-BASED fallback."""
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
            result = self._call_model(
                model=model,
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                temperature=0.3,
                json_mode=True,
            )

            if result.success and result.json_content is not None:
                return result

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
        """Use AI to select the best project ideas from discovered trends."""
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
            min_model_size=8,
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

        models_status = []
        for model in self.model_chain[:20]:  # Top 20 models
            cooldown_key = f"{model.provider}:{model.api_model_id}"
            total_failures = self._model_failures.get(cooldown_key, 0)

            models_status.append({
                "name": model.name,
                "provider": model.provider,
                "size_b": model.size_billions,
                "available": self._is_model_available(model),
                "failures": total_failures,
            })

        return {
            "providers": providers_status,
            "model_chain": models_status,
            "total_available_models": len([m for m in self.model_chain if self._is_model_available(m)]),
        }

    def print_status(self) -> None:
        """Print formatted status of all providers and models."""
        print("\n" + "=" * 70)
        print("AI UNIFIED CLIENT STATUS (Modular Model-Size-Based Fallback)")
        print("=" * 70)

        status = self.get_status()

        print("\nPROVIDERS:")
        for name, pstatus in status["providers"].items():
            icon = "[OK]" if pstatus["available"] else "[--]"
            print(f"  {icon} {name}: {pstatus['status']}")
            print(f"      Requests: {pstatus['requests']} | Success: {pstatus['successes']} | Tokens: {pstatus['total_tokens']}")

        print("\nMODEL CHAIN (Top 20 by size):")
        for m in status["model_chain"]:
            icon = "[OK]" if m["available"] else "[--]"
            print(f"  {icon} {m['size_b']:>5.0f}B | {m['name'][:40]:<40} ({m['provider']})")

        print(f"\nTotal Available Models: {status['total_available_models']}")
        print("=" * 70)
