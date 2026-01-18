import logging
import os
import requests
from ..base import AIProvider, CompletionResult, ProviderStatus, ProviderConfig

logger = logging.getLogger("AI.Providers.GitHub")

class GitHubModelsProvider(AIProvider):
    """GitHub Models Provider - Free access via GitHub token."""

    BASE_URL = "https://models.inference.ai.azure.com/chat/completions"

    def __init__(self):
        config = ProviderConfig(
            name="github",
            base_url=self.BASE_URL,
            api_key_env="GH_TOKEN"
        )
        super().__init__(config)
        self.api_key = os.environ.get("GH_TOKEN")  # Uses existing GitHub token
        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
        else:
            self.status = ProviderStatus.UNCONFIGURED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7, timeout: int = 60) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="GitHub token not configured")

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
            "temperature": temperature
        }

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=timeout)

            if response.status_code == 200:
                data = response.json()

                # Defensive check for response structure
                choices = data.get("choices")
                if not choices or not isinstance(choices, list) or len(choices) == 0:
                    return CompletionResult(success=False, error=f"GitHub Models Error: Invalid 'choices' in response: {data}")

                message = choices[0].get("message")
                if not message:
                    return CompletionResult(success=False, error=f"GitHub Models Error: Missing 'message' in first choice: {data}")

                content = message.get("content")
                if content is None:
                    return CompletionResult(success=False, error=f"GitHub Models Error: content is null in response: {data}")

                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                return CompletionResult(success=True, content=content, tokens_used=tokens, model_used=model)
            else:
                return CompletionResult(success=False, error=f"GitHub Models Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"GitHub Models Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, timeout: int = 60) -> CompletionResult:
        json_prompt = prompt + "\n\nRETURN ONLY VALID JSON."
        result = self.chat_completion(json_prompt, system_prompt, model, max_tokens, 0.2, timeout)
        if result.success:
            import json
            try:
                content = result.content.strip()
                if content.startswith("```json"):
                    content = content[7:]
                if content.endswith("```"):
                    content = content[:-3]
                json_obj = json.loads(content.strip())
                result.json_content = json_obj
            except json.JSONDecodeError as e:
                result.success = False
                result.error = f"Failed to parse JSON: {e}"
        return result
