import logging
import os
import requests
from ..base import AIProvider, CompletionResult, ProviderStatus, ProviderConfig

logger = logging.getLogger("AI.Providers.Groq")

class GroqProvider(AIProvider):
    """Groq Provider (LPU Inference Engine)."""

    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(self):
        config = ProviderConfig(
            name="groq",
            base_url=self.BASE_URL,
            api_key_env="GROQ_API_KEY"
        )
        super().__init__(config)
        self.api_key = os.environ.get("GROQ_API_KEY")
        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
            self.client = None # Lazy init if using SDK, but we use requests for zero-dep
        else:
            self.status = ProviderStatus.UNCONFIGURED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7, timeout: int = 60) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="Groq API key not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                return CompletionResult(success=True, content=content, tokens_used=tokens, model_used=model)
            else:
                return CompletionResult(success=False, error=f"Groq Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Groq Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, timeout: int = 60) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="Groq API key not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Groq supports json_object response format
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt + " You must output JSON."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                import json
                json_obj = json.loads(content)
                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                return CompletionResult(success=True, content=content, json_content=json_obj, tokens_used=tokens, model_used=model)
            else:
                return CompletionResult(success=False, error=f"Groq Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Groq JSON Exception: {str(e)}")
