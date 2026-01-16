"""
Cerebras AI Provider - Primary provider for PRFusion.

Cerebras offers ultra-fast inference with generous free tier:
- 30 RPM, 14,400 RPD, 1M tokens/day
- OpenAI-compatible API
"""

import json
import logging
import os
import time
from typing import Any

from openai import OpenAI

from ..base import (
    AIProvider,
    CompletionResult,
    ModelConfig,
    ProviderConfig,
    ProviderStatus,
)


logger = logging.getLogger("AI.Cerebras")


# Cerebras model configurations (Dec 2025)
CEREBRAS_MODELS = [
    ModelConfig("qwen-3-235b-a22b-instruct-2507", 1, "Qwen 3 235B - Best quality"),
    ModelConfig("gpt-oss-120b", 2, "GPT OSS 120B"),
    ModelConfig("zai-glm-4.6", 3, "Z.ai GLM 4.6 (357B params)"),
    ModelConfig("llama-3.3-70b", 4, "Llama 3.3 70B"),
    ModelConfig("qwen-3-32b", 5, "Qwen 3 32B"),
    ModelConfig("llama3.1-8b", 6, "Llama 3.1 8B - Fastest"),
]


def get_cerebras_config() -> ProviderConfig:
    """Get Cerebras provider configuration."""
    return ProviderConfig(
        name="cerebras",
        base_url="https://api.cerebras.ai/v1",
        api_key_env="CEREBRAS_API_KEY",
        models=CEREBRAS_MODELS,
        rpm_limit=30,
        rpd_limit=14400,
        timeout=60,
    )


class CerebrasProvider(AIProvider):
    """
    Cerebras AI provider implementation.

    Uses OpenAI-compatible API for ultra-fast inference.
    Primary provider in the fallback chain.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        if config is None:
            config = get_cerebras_config()
        super().__init__(config)

        self.api_key = os.getenv(config.api_key_env)
        self.client: OpenAI | None = None

        if self.api_key:
            try:
                self.client = OpenAI(
                    api_key=self.api_key,
                    base_url=config.base_url,
                )
                self.status = ProviderStatus.AVAILABLE
                logger.info(f"[Cerebras] Provider initialized")
            except Exception as e:
                logger.error(f"[Cerebras] Failed to initialize: {e}")
                self.status = ProviderStatus.ERROR
        else:
            logger.warning("[Cerebras] API key not found")
            self.status = ProviderStatus.DISABLED

    def is_available(self) -> bool:
        """Check if Cerebras is available."""
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
        """Generate chat completion using Cerebras."""
        if not self.is_available():
            return CompletionResult(
                success=False,
                error="Cerebras provider not available",
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
                provider_used="cerebras",
                tokens_used=tokens_used,
            )

        except Exception as e:
            error_msg = str(e)
            logger.warning(f"[Cerebras] {model_name} failed: {error_msg}")

            # Check if rate limited
            if "rate" in error_msg.lower() or "429" in error_msg:
                self._trigger_cooldown(model_name, 60)

            return CompletionResult(
                success=False,
                error=error_msg,
                model_used=model_name,
                provider_used="cerebras",
            )

    def json_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """Generate JSON-structured completion using Cerebras."""
        if not self.is_available():
            return CompletionResult(
                success=False,
                error="Cerebras provider not available",
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
                temperature=0.3,  # Lower temp for structured output
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
                provider_used="cerebras",
                tokens_used=tokens_used,
                error="Failed to parse JSON" if json_content is None else None,
            )

        except Exception as e:
            error_msg = str(e)
            logger.warning(f"[Cerebras] JSON {model_name} failed: {error_msg}")

            if "rate" in error_msg.lower() or "429" in error_msg:
                self._trigger_cooldown(model_name, 60)

            return CompletionResult(
                success=False,
                error=error_msg,
                model_used=model_name,
                provider_used="cerebras",
            )

    def chat_completion_with_fallback(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResult:
        """
        Try chat completion with automatic model fallback.

        Tries each model in tier order until one succeeds.
        """
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

            # Brief pause before next model
            time.sleep(0.5)

        return CompletionResult(
            success=False,
            error="All Cerebras models failed",
            provider_used="cerebras",
        )

    def json_completion_with_fallback(
        self,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """
        Try JSON completion with automatic model fallback.
        """
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
            error="All Cerebras models failed for JSON",
            provider_used="cerebras",
        )
