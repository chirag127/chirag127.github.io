import logging
import os
import requests
from ..base import AIProvider, CompletionResult, ProviderStatus, ProviderConfig

logger = logging.getLogger("AI.Providers.Gemini")

class GeminiProvider(AIProvider):
    """Google Gemini Provider (Generative Language API)."""

    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    def __init__(self):
        config = ProviderConfig(
            name="gemini",
            base_url=self.BASE_URL,
            api_key_env="GEMINI_API_KEY"
        )
        super().__init__(config)
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
        else:
            self.status = ProviderStatus.UNCONFIGURED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7, timeout: int = 60) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="Gemini API key not configured")

        url = self.BASE_URL.format(model=model) + f"?key={self.api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                try:
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    # Usage metadata is distinct in Gemini
                    usage = data.get("usageMetadata", {})
                    tokens = usage.get("totalTokenCount", 0)
                    return CompletionResult(success=True, content=content, tokens_used=tokens, model_used=model)
                except (KeyError, IndexError):
                    return CompletionResult(success=False, error=f"Gemini Malformed Response: {data}")
            else:
                return CompletionResult(success=False, error=f"Gemini Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Gemini Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, timeout: int = 60) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="Gemini API key not configured")

        url = self.BASE_URL.format(model=model) + f"?key={self.api_key}"

        headers = {
            "Content-Type": "application/json"
        }

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": 0.2,
                "response_mime_type": "application/json"
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=timeout)

            if response.status_code == 200:
                data = response.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                import json
                json_obj = json.loads(content)
                usage = data.get("usageMetadata", {})
                tokens = usage.get("totalTokenCount", 0)
                return CompletionResult(success=True, content=content, json_content=json_obj, tokens_used=tokens, model_used=model)
            else:
                return CompletionResult(success=False, error=f"Gemini JSON Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Gemini JSON Exception: {str(e)}")
