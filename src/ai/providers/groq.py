"""
Groq AI Provider - Ultra-fast inference fallback.

Groq offers blazing fast inference with free tier:
- 1k-14.4k RPD depending on model
- OpenAI-compatible API
"""

import logging
import os
import time

from groq import Groq

from ..base import (
    AIProvider,
    CompletionResult,
    ModelConfig,
    ProviderConfig,
    ProviderStatus,
)


logger = logging.getLogger("AI.Groq")


# Groq model configurations (Dec 2025 - VERIFIED via web search)
# NOTE: llama-3.1-405b deprecated as of Jan 2025
GROQ_MODELS = [
    ModelConfig("openai/gpt-oss-120b", 1, "GPT OSS 120B"),
    ModelConfig("llama-3.3-70b-versatile", 2, "Llama 3.3 70B Versatile"),
    ModelConfig("qwen/qwen3-32b", 3, "Qwen 3 32B"),
    ModelConfig("mistral-saba-24b", 4, "Mistral Saba 24B"),
    ModelConfig("meta-llama/llama-4-scout-17b-16e-instruct", 5, "Llama 4 Scout 17B"),
    ModelConfig("deepseek-r1-distill-llama-70b", 6, "DeepSeek R1 Distill 70B"),
    ModelConfig("gemma2-9b-it", 7, "Gemma 2 9B IT"),
    ModelConfig("llama-3.1-8b-instant", 8, "Llama 3.1 8B Instant"),
]


def get_groq_config() -> ProviderConfig:
    """Get Groq provider configuration."""
    return ProviderConfig(
        name="groq",
        base_url="https://api.groq.com/openai/v1",
        api_key_env="GROQ_API_KEY",
        models=GROQ_MODELS,
        rpm_limit=30,
        rpd_limit=14400,
        timeout=60,
    )


class GroqProvider(AIProvider):
    """
    Groq AI provider implementation.

    Uses Groq's ultra-fast LPU inference.
    Secondary fallback provider after Cerebras.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        if config is None:
            config = get_groq_config()
        super().__init__(config)

        self.api_key = os.getenv(config.api_key_env)
        self.client: Groq | None = None

        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                self.status = ProviderStatus.AVAILABLE
                logger.info(f"[Groq] Provider initialized")
            except Exception as e:
                logger.error(f"[Groq] Failed to initialize: {e}")
                self.status = ProviderStatus.ERROR
        else:
            logger.warning("[Groq] API key not found")
            self.status = ProviderStatus.DISABLED

    def is_available(self) -> bool:
        """Check if Groq is available."""
        return (
            self.status == ProviderStatus.AVAILABLE
            and self.client is not None
            and self.api_key is not None
        )

    def chat_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResult:
        """Generate chat completion using Groq."""
        if not self.is_available():
            return CompletionResult(
                success=False,
                error="Groq provider not available",
            )

        # Get model to use
        if model:
            model_name = model
        else:
            best_model = self.get_best_model()
            if not best_model:
                return CompletionResult(
                    success=False,
                    error="No available models",
                )
            model_name = best_model.name

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0

            return CompletionResult(
                success=True,
                content=content,
                model_used=model_name,
                provider_used="groq",
                tokens_used=tokens_used,
            )

        except Exception as e:
            error_msg = str(e)
            logger.warning(f"[Groq] {model_name} failed: {error_msg}")

            if "rate" in error_msg.lower() or "429" in error_msg:
                self._trigger_cooldown(model_name, 60)

            return CompletionResult(
                success=False,
                error=error_msg,
                model_used=model_name,
                provider_used="groq",
            )

    def json_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """Generate JSON-structured completion using Groq."""
        if not self.is_available():
            return CompletionResult(
                success=False,
                error="Groq provider not available",
            )

        # Get model to use
        if model:
            model_name = model
        else:
            best_model = self.get_best_model()
            if not best_model:
                return CompletionResult(
                    success=False,
                    error="No available models",
                )
            model_name = best_model.name

        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.3,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0

            # Parse JSON
            json_content = self._parse_json(content)

            return CompletionResult(
                success=json_content is not None,
                content=content,
                json_content=json_content,
                model_used=model_name,
                provider_used="groq",
                tokens_used=tokens_used,
                error="Failed to parse JSON" if json_content is None else None,
            )

        except Exception as e:
            error_msg = str(e)
            logger.warning(f"[Groq] JSON {model_name} failed: {error_msg}")

            if "rate" in error_msg.lower() or "429" in error_msg:
                self._trigger_cooldown(model_name, 60)

            return CompletionResult(
                success=False,
                error=error_msg,
                model_used=model_name,
                provider_used="groq",
            )

    def chat_completion_with_fallback(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResult:
        """Try chat completion with automatic model fallback."""
        for model_config in self.models:
            if self._is_model_cooling_down(model_config.name):
                continue

            result = self.chat_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                model=model_config.name,
                max_tokens=max_tokens,
                temperature=temperature,
            )

            if result.success:
                return result

            time.sleep(0.5)

        return CompletionResult(
            success=False,
            error="All Groq models failed",
            provider_used="groq",
        )

    def json_completion_with_fallback(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """Try JSON completion with automatic model fallback."""
        for model_config in self.models:
            if self._is_model_cooling_down(model_config.name):
                continue

            result = self.json_completion(
                prompt=prompt,
                system_prompt=system_prompt,
                model=model_config.name,
                max_tokens=max_tokens,
            )

            if result.success and result.json_content is not None:
                return result

            time.sleep(0.5)

        return CompletionResult(
            success=False,
            error="All Groq models failed for JSON",
            provider_used="groq",
        )
