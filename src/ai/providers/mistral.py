"""
Mistral AI Provider.

Base URL: https://api.mistral.ai/v1
Limits: 1 RPS, ~86k RPD (Experiment plan).
"""

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


logger = logging.getLogger("AI.Mistral")


# Mistral model configurations (Dec 2025)
MISTRAL_MODELS = [
    ModelConfig("mistral-large-latest", 1, "Mistral Large", max_tokens=32768),
    ModelConfig("mistral-small-3.1-24b-instruct", 2, "Mistral Small 24B", max_tokens=32768),
    ModelConfig("open-mistral-nemo", 3, "Open Mistral Nemo 12B", max_tokens=32768),
]


def get_mistral_config() -> ProviderConfig:
    """Get Mistral provider configuration."""
    return ProviderConfig(
        name="mistral",
        base_url="https://api.mistral.ai/v1",
        api_key_env="MISTRAL_API_KEY",
        models=MISTRAL_MODELS,
        rpm_limit=60,  # 1 RPS
        rpd_limit=86400,
        timeout=60,
    )


class MistralProvider(AIProvider):
    """
    Mistral AI provider using raw REST API.

    OpenAI-compatible API format.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        if config is None:
            config = get_mistral_config()
        super().__init__(config)

        self.api_key = os.getenv(config.api_key_env)

        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
            logger.info(f"[Mistral] Provider initialized")
        else:
            logger.warning("[Mistral] API key not found")
            self.status = ProviderStatus.DISABLED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE and self.api_key is not None

    def _make_request(
        self,
        model: str,
        messages: list,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        response_format: dict | None = None,
    ) -> dict | None:
        """Make raw REST request to Mistral API."""
        url = f"{self.config.base_url}/chat/completions"

        body = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        if response_format:
            body["response_format"] = response_format

        try:
            response = requests.post(
                url,
                json=body,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                timeout=self.config.timeout,
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.warning(f"[Mistral] Request failed: {e}")
            return None

    def chat_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResult:
        """Generate chat completion using Mistral."""
        if not self.is_available():
            return CompletionResult(success=False, error="Mistral provider not available")

        model_name = model or self.models[0].name if self.models else "mistral-large-latest"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._make_request(model_name, messages, max_tokens, temperature)

        if response and "choices" in response:
            try:
                content = response["choices"][0]["message"]["content"]
                return CompletionResult(
                    success=True,
                    content=content,
                    model_used=model_name,
                    provider_used="mistral",
                    tokens_used=response.get("usage", {}).get("total_tokens", 0),
                )
            except (KeyError, IndexError) as e:
                return CompletionResult(success=False, error=f"Parse error: {e}")

        return CompletionResult(success=False, error="No response from Mistral")

    def json_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """Generate JSON completion using Mistral."""
        if not self.is_available():
            return CompletionResult(success=False, error="Mistral provider not available")

        model_name = model or self.models[0].name

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._make_request(
            model_name, messages, max_tokens, 0.3,
            response_format={"type": "json_object"}
        )

        if response and "choices" in response:
            try:
                content = response["choices"][0]["message"]["content"]
                json_content = self._parse_json(content)
                return CompletionResult(
                    success=json_content is not None,
                    content=content,
                    json_content=json_content,
                    model_used=model_name,
                    provider_used="mistral",
                    error="Failed to parse JSON" if json_content is None else None,
                )
            except (KeyError, IndexError) as e:
                return CompletionResult(success=False, error=f"Parse error: {e}")

        return CompletionResult(success=False, error="No response from Mistral")
