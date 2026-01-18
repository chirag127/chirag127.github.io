import logging
import os
import requests
from ..base import AIProvider, CompletionResult, ProviderStatus, ProviderConfig

logger = logging.getLogger("AI.Providers.Cloudflare")

class CloudflareProvider(AIProvider):
    """Cloudflare Workers AI Provider."""

    def __init__(self):
        config = ProviderConfig(
            name="cloudflare",
            base_url="https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/",
            api_key_env="CLOUDFLARE_API_KEY"
        )
        super().__init__(config)
        self.api_key = os.environ.get("CLOUDFLARE_API_KEY")
        self.account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")

        if self.api_key and self.account_id:
            self.status = ProviderStatus.AVAILABLE
            self.base_url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/"
        else:
            self.status = ProviderStatus.UNCONFIGURED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7, timeout: int = 60) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="Cloudflare credentials not configured")

        url = f"{self.base_url}{model}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens, # Note: Cloudflare sometimes ignores this on smaller models
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    result = data.get("result")
                    if not result:
                        return CompletionResult(success=False, error=f"Cloudflare Error: Missing 'result' in successful response: {data}")

                    content = result.get("response")
                    if content is None:
                        return CompletionResult(success=False, error=f"Cloudflare Error: Missing 'response' in result: {data}")

                    return CompletionResult(success=True, content=content, tokens_used=0, model_used=model)
                else:
                    return CompletionResult(success=False, error=f"Cloudflare API Error: {data.get('errors')}")
            else:
                return CompletionResult(success=False, error=f"Cloudflare HTTP Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Cloudflare Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, timeout: int = 60) -> CompletionResult:
         # Fallback to chat with prompt injection
        return super().json_completion(prompt, system_prompt, model, max_tokens, timeout)
