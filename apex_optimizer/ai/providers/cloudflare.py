"""
Cloudflare Workers AI Provider.

Base URL: https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run
Limits: 100k req/day.
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


logger = logging.getLogger("AI.Cloudflare")


# Cloudflare Workers AI model configurations (Dec 2025)
CLOUDFLARE_MODELS = [
    ModelConfig("@cf/meta/llama-3.1-70b-instruct", 1, "Llama 3.1 70B", max_tokens=4096),
    ModelConfig("@cf/meta/llama-3.3-70b-instruct-fp8-fast", 2, "Llama 3.3 70B Fast", max_tokens=4096),
    ModelConfig("@cf/qwen/qwen1.5-14b-chat-awq", 3, "Qwen 1.5 14B", max_tokens=4096),
    ModelConfig("@cf/meta/llama-3.1-8b-instruct", 4, "Llama 3.1 8B", max_tokens=4096),
]


def get_cloudflare_config() -> ProviderConfig:
    """Get Cloudflare Workers AI provider configuration."""
    return ProviderConfig(
        name="cloudflare",
        base_url="https://api.cloudflare.com/client/v4/accounts",
        api_key_env="CLOUDFLARE_API_TOKEN",
        models=CLOUDFLARE_MODELS,
        rpm_limit=100,
        rpd_limit=100000,
        timeout=60,
    )


class CloudflareProvider(AIProvider):
    """
    Cloudflare Workers AI provider using raw REST API.

    Requires CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN.
    """

    def __init__(self, config: ProviderConfig | None = None) -> None:
        if config is None:
            config = get_cloudflare_config()
        super().__init__(config)

        self.api_key = os.getenv(config.api_key_env)
        self.account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")

        if self.api_key and self.account_id:
            self.status = ProviderStatus.AVAILABLE
            logger.info(f"[Cloudflare] Provider initialized")
        else:
            missing = []
            if not self.api_key:
                missing.append("CLOUDFLARE_API_TOKEN")
            if not self.account_id:
                missing.append("CLOUDFLARE_ACCOUNT_ID")
            logger.warning(f"[Cloudflare] Missing: {', '.join(missing)}")
            self.status = ProviderStatus.DISABLED

    def is_available(self) -> bool:
        return (
            self.status == ProviderStatus.AVAILABLE
            and self.api_key is not None
            and self.account_id is not None
        )

    def _make_request(
        self,
        model: str,
        messages: list,
        max_tokens: int = 4096,
    ) -> dict | None:
        """Make raw REST request to Cloudflare Workers AI."""
        url = f"{self.config.base_url}/{self.account_id}/ai/run/{model}"

        body = {
            "messages": messages,
            "max_tokens": max_tokens,
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
            logger.warning(f"[Cloudflare] Request failed: {e}")
            return None

    def chat_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResult:
        """Generate chat completion using Cloudflare Workers AI."""
        if not self.is_available():
            return CompletionResult(success=False, error="Cloudflare provider not available")

        model_name = model or self.models[0].name if self.models else "@cf/meta/llama-3.1-70b-instruct"

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self._make_request(model_name, messages, max_tokens)

        if response and "result" in response:
            try:
                content = response["result"]["response"]
                return CompletionResult(
                    success=True,
                    content=content,
                    model_used=model_name,
                    provider_used="cloudflare",
                )
            except (KeyError, IndexError) as e:
                return CompletionResult(success=False, error=f"Parse error: {e}")

        return CompletionResult(success=False, error="No response from Cloudflare")

    def json_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """Generate JSON completion using Cloudflare Workers AI."""
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
