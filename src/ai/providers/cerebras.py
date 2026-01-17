import logging
import os
import requests
from ..base import AIProvider, CompletionResult, ProviderStatus, ProviderConfig

logger = logging.getLogger("AI.Providers.Cerebras")

class CerebrasProvider(AIProvider):
    """Cerebras AI Provider (High Speed, Large Models)."""

    BASE_URL = "https://api.cerebras.ai/v1/chat/completions"

    def __init__(self):
        config = ProviderConfig(
            name="cerebras",
            base_url=self.BASE_URL,
            api_key_env="CEREBRAS_API_KEY"
        )
        super().__init__(config)
        self.api_key = os.environ.get("CEREBRAS_API_KEY")
        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
        else:
            self.status = ProviderStatus.UNCONFIGURED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7, timeout: int = 60) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="Cerebras API key not configured")

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
            "max_completion_tokens": max_tokens, # Cerebras uses max_completion_tokens
            "temperature": temperature,
            "top_p": 1,
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
                return CompletionResult(success=False, error=f"Cerebras Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Cerebras Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, timeout: int = 60) -> CompletionResult:
        # Append JSON instruction since structured output varies
        json_prompt = prompt + "\n\nRETURN ONLY RAW JSON. NO MARKDOWN."

        result = self.chat_completion(json_prompt, system_prompt, model, max_tokens, 0.2, timeout)
        if result.success:
            import json
            try:
                # Clean markdown blocks if present
                content = result.content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]

                json_obj = json.loads(content)
                result.json_content = json_obj
            except json.JSONDecodeError as e:
                result.success = False
                result.error = f"Failed to parse JSON: {e}"

        return result
