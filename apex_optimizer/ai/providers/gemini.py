"""
Google Gemini AI Provider.

Uses the Gemini REST API directly (no SDK per AGENTS.md).
Base URL: https://generativelanguage.googleapis.com/v1beta
"""

import json
import logging
import os

import requests

from ..base import (
    AIProvider,
    CompletionResult,
    ModelConfig,
    ProviderConfig,
    ProviderStatus,
)


logger = logging.getLogger("AI.Gemini")


# Gemini model configurations (Dec 2025 - VERIFIED)
# Note: Gemini API uses models/MODEL_NAME format
# Gemma 3 models use "-it" suffix for instruction-tuned
GEMINI_MODELS = [
    ModelConfig("gemma-3-27b-it", 1, "Gemma 3 27B IT", max_tokens=8192),
    ModelConfig("gemma-3-12b-it", 2, "Gemma 3 12B IT", max_tokens=8192),
    ModelConfig("gemma-3-4b-it", 3, "Gemma 3 4B IT", max_tokens=8192),
    ModelConfig("gemma-3-1b-it", 4, "Gemma 3 1B IT", max_tokens=8192),
]


def get_gemini_config() -> ProviderConfig:
    """Get Gemini provider configuration."""
    return ProviderConfig(
        name="gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_key_env="GEMINI_API_KEY",
        models=GEMINI_MODELS,
        rpm_limit=30,
        rpd_limit=14400,
        timeout=60,
    )


class GeminiProvider(AIProvider):
    """
    Google Gemini AI provider using raw REST API.

    Uses direct REST calls (no SDK) per AGENTS.md requirements.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        if config is None:
            config = get_gemini_config()
        super().__init__(config)

        self.api_key = os.getenv(config.api_key_env)

        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
            logger.info(f"[Gemini] Provider initialized")
        else:
            logger.warning("[Gemini] API key not found")
            self.status = ProviderStatus.DISABLED

    def is_available(self) -> bool:
        """Check if Gemini is available."""
        return self.status == ProviderStatus.AVAILABLE and self.api_key is not None

    def _make_request(
        self,
        model: str,
        prompt: str,
        system_prompt: str = "",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> dict | None:
        """Make raw REST request to Gemini API."""
        url = f"{self.config.base_url}/models/{model}:generateContent?key={self.api_key}"

        # Build request body
        contents = []
        if system_prompt:
            contents.append({
                "role": "user",
                "parts": [{"text": f"System: {system_prompt}"}]
            })
            contents.append({
                "role": "model",
                "parts": [{"text": "Understood. I will follow these instructions."}]
            })

        contents.append({
            "role": "user",
            "parts": [{"text": prompt}]
        })

        body = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            }
        }

        try:
            response = requests.post(
                url,
                json=body,
                headers={"Content-Type": "application/json"},
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"[Gemini] Request failed: {e}")
            return None

    def chat_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResult:
        """Generate chat completion using Gemini."""
        if not self.is_available():
            return CompletionResult(success=False, error="Gemini provider not available")

        model_name = model or self.models[0].name if self.models else "gemma-3-27b-instruct"

        response = self._make_request(model_name, prompt, system_prompt, max_tokens, temperature)

        if response and "candidates" in response:
            try:
                content = response["candidates"][0]["content"]["parts"][0]["text"]
                return CompletionResult(
                    success=True,
                    content=content,
                    model_used=model_name,
                    provider_used="gemini",
                )
            except (KeyError, IndexError) as e:
                return CompletionResult(success=False, error=f"Parse error: {e}")

        return CompletionResult(success=False, error="No response from Gemini")

    def json_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """Generate JSON completion using Gemini."""
        result = self.chat_completion(
            prompt=f"{prompt}\n\nRespond with valid JSON only.",
            system_prompt=system_prompt,
            model=model,
            max_tokens=max_tokens,
            temperature=0.3,
        )

        if result.success and result.content:
            json_content = self._parse_json(result.content)
            if json_content:
                result.json_content = json_content
            else:
                result.success = False
                result.error = "Failed to parse JSON"

        return result
