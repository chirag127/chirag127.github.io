"""
NVIDIA NIM AI Provider.

Base URL: https://integrate.api.nvidia.com/v1
Limits: 40 RPM (~57k RPD). Phone verify required.
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


logger = logging.getLogger("AI.NVIDIA")


# NVIDIA NIM model configurations (Dec 2025)
NVIDIA_MODELS = [
    ModelConfig("nvidia/llama-3.1-nemotron-70b-instruct", 1, "Nemotron 70B", max_tokens=4096),
    ModelConfig("meta/llama-3.1-70b-instruct", 2, "Llama 3.1 70B", max_tokens=4096),
    ModelConfig("meta/llama-3.1-8b-instruct", 3, "Llama 3.1 8B", max_tokens=4096),
]


def get_nvidia_config() -> ProviderConfig:
    """Get NVIDIA NIM provider configuration."""
    return ProviderConfig(
        name="nvidia",
        base_url="https://integrate.api.nvidia.com/v1",
        api_key_env="NVIDIA_API_KEY",
        models=NVIDIA_MODELS,
        rpm_limit=40,
        rpd_limit=57600,
        timeout=90,  # NVIDIA can be slower
    )


class NVIDIAProvider(AIProvider):
    """
    NVIDIA NIM AI provider using raw REST API.

    OpenAI-compatible API format.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        if config is None:
            config = get_nvidia_config()
        super().__init__(config)

        self.api_key = os.getenv(config.api_key_env)

        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
            logger.info(f"[NVIDIA] Provider initialized")
        else:
            logger.warning("[NVIDIA] API key not found")
            self.status = ProviderStatus.DISABLED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE and self.api_key is not None

    def _make_request(
        self,
        model: str,
        messages: list,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> dict | None:
        """Make raw REST request to NVIDIA NIM API."""
        url = f"{self.config.base_url}/chat/completions"

        body = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

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
            logger.warning(f"[NVIDIA] Request failed: {e}")
            return None

    def chat_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResult:
        """Generate chat completion using NVIDIA NIM."""
        if not self.is_available():
            return CompletionResult(success=False, error="NVIDIA provider not available")

        model_name = model or self.models[0].name if self.models else "meta/llama-3.1-405b-instruct"

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
                    provider_used="nvidia",
                    tokens_used=response.get("usage", {}).get("total_tokens", 0),
                )
            except (KeyError, IndexError) as e:
                return CompletionResult(success=False, error=f"Parse error: {e}")

        return CompletionResult(success=False, error="No response from NVIDIA")

    def json_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """Generate JSON completion using NVIDIA NIM."""
        result = self.chat_completion(
            prompt=f"{prompt}\n\nRespond with valid JSON only, no markdown.",
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
