"""
Unified AI Providers Module.
Consolidates all provider implementations into a single file to reduce fragmentation.
"""

import logging
import os
import requests
from typing import Any, Dict, Optional
from .base import AIProvider, CompletionResult, ProviderStatus, ProviderConfig

logger = logging.getLogger("AI.Providers")

# ============================================================================
# CEREBRAS PROVIDER
# ============================================================================
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

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7) -> CompletionResult:
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
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=60)

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

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096) -> CompletionResult:
        # Append JSON instruction since structured output varies
        json_prompt = prompt + "\n\nRETURN ONLY RAW JSON. NO MARKDOWN."

        result = self.chat_completion(json_prompt, system_prompt, model, max_tokens, 0.2)
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


# ============================================================================
# GROQ PROVIDER
# ============================================================================
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

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7) -> CompletionResult:
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
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=60)

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

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096) -> CompletionResult:
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
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=60)

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


# ============================================================================
# NVIDIA PROVIDER
# ============================================================================
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

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="NVIDIA API key not configured")

        # NVIDIA uses full model URLs often, but NIMs use the model name.
        # Ensure 'nvidia/' prefix if needed or just pass strict name.

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
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                return CompletionResult(success=True, content=content, tokens_used=tokens, model_used=model)
            else:
                return CompletionResult(success=False, error=f"NVIDIA Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"NVIDIA Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096) -> CompletionResult:
        # Fallback to chat completion with prompt engineering for JSON
        json_prompt = prompt + "\n\nRETURN ONLY VALID JSON."
        result = self.chat_completion(json_prompt, system_prompt, model, max_tokens, 0.2)

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


# ============================================================================
# MISTRAL PROVIDER
# ============================================================================
class MistralProvider(AIProvider):
    """Mistral AI Provider."""

    BASE_URL = "https://api.mistral.ai/v1/chat/completions"

    def __init__(self):
        config = ProviderConfig(
            name="mistral",
            base_url=self.BASE_URL,
            api_key_env="MISTRAL_API_KEY"
        )
        super().__init__(config)
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        if self.api_key:
            self.status = ProviderStatus.AVAILABLE
        else:
            self.status = ProviderStatus.UNCONFIGURED

    def is_available(self) -> bool:
        return self.status == ProviderStatus.AVAILABLE

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="Mistral API key not configured")

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
            "safe_prompt": False
        }

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                return CompletionResult(success=True, content=content, tokens_used=tokens, model_used=model)
            else:
                return CompletionResult(success=False, error=f"Mistral Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Mistral Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096) -> CompletionResult:
        if not self.is_available():
            return CompletionResult(success=False, error="Mistral API key not configured")

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
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(self.BASE_URL, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                import json
                json_obj = json.loads(content)
                usage = data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                return CompletionResult(success=True, content=content, json_content=json_obj, tokens_used=tokens, model_used=model)
            else:
                return CompletionResult(success=False, error=f"Mistral JSON Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Mistral JSON Exception: {str(e)}")


# ============================================================================
# GEMINI PROVIDER
# ============================================================================
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

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7) -> CompletionResult:
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
            response = requests.post(url, json=payload, headers=headers, timeout=60)

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

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096) -> CompletionResult:
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
            response = requests.post(url, json=payload, headers=headers, timeout=60)

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


# ============================================================================
# CLOUDFLARE PROVIDER
# ============================================================================
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

    def chat_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096, temperature: float = 0.7) -> CompletionResult:
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
            response = requests.post(url, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    content = data["result"]["response"]
                    return CompletionResult(success=True, content=content, tokens_used=0, model_used=model)
                else:
                    return CompletionResult(success=False, error=f"Cloudflare API Error: {data.get('errors')}")
            else:
                return CompletionResult(success=False, error=f"Cloudflare HTTP Error {response.status_code}: {response.text}")

        except Exception as e:
            return CompletionResult(success=False, error=f"Cloudflare Exception: {str(e)}")

    def json_completion(self, prompt: str, system_prompt: str, model: str, max_tokens: int = 4096) -> CompletionResult:
         # Fallback to chat with prompt injection
        return super().json_completion(prompt, system_prompt, model, max_tokens)
