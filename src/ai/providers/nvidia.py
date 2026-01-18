import logging
import os
import requests
from ..base import AIProvider, CompletionResult, ProviderStatus, ProviderConfig

logger = logging.getLogger("AI.Providers.NVIDIA")

class NVIDIAProvider(AIProvider):
    """NVIDIA NIM Provider."""

    BASE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

    def __init__(self):
        config = ProviderConfig(
            name="nvidia",
            base_url=self.BASE_URL,
            api_key_env="NVIDIA_API_KEY"
        )
        super().__init__(config)
        self.api_key = os.environ.get("NVIDIA_API_KEY")
        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
        else:
            self.status = ProviderStatus.UNCONFIGURED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7, timeout: int = 60) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="NVIDIA API key not configured")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
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

                # Defensive check for response structure
                choices = data.get("choices")
                if not choices or not isinstance(choices, list) or len(choices) == 0:
                    return CompletionResult(success=False, error=f"NVIDIA Error: Invalid 'choices' in response: {data}")

                message = choices[0].get("message")
                if not message:
                    return CompletionResult(success=False, error=f"NVIDIA Error: Missing 'message' in first choice: {data}")

                content = message.get("content")
                if content is None:
                    refusal = message.get("refusal")
                    if refusal:
                        return CompletionResult(success=False, error=f"NVIDIA Refusal: {refusal}")
                    return CompletionResult(success=False, error=f"NVIDIA Error: content is null in response: {data}")

                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                return CompletionResult(success=True, content=content, tokens_used=tokens, model_used=model)
            else:
                return CompletionResult(success=False, error=f"NVIDIA Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"NVIDIA Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, timeout: int = 60) -> CompletionResult:
        # Fallback to chat completion with prompt engineering for JSON
        json_prompt = prompt + "\n\nRETURN ONLY VALID JSON."
        result = self.chat_completion(json_prompt, system_prompt, model, max_tokens, 0.2, timeout)

        if result.success:
            import json
            try:
                # Clean markdown
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
