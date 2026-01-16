"""
AI Provider Base Classes - Abstract interfaces for AI providers.

All AI providers must implement these interfaces for consistent behavior
across the fallback chain.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


logger = logging.getLogger("AI.Base")


class ProviderStatus(Enum):
    """Status of an AI provider."""
    AVAILABLE = "available"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"
    DISABLED = "disabled"
    UNCONFIGURED = "unconfigured"


@dataclass
class ModelConfig:
    """Configuration for a single AI model."""
    name: str
    tier: int  # 1 = best, higher = fallback
    description: str = ""
    max_tokens: int = 32768
    supports_json: bool = True


@dataclass
class ProviderConfig:
    """Configuration for an AI provider."""
    name: str
    base_url: str
    api_key_env: str
    models: list[ModelConfig] = field(default_factory=list)
    rpm_limit: int = 30
    rpd_limit: int = 14400
    timeout: int = 60


@dataclass
class CompletionResult:
    """Result from an AI completion request."""
    success: bool
    content: str | None = None
    json_content: dict | None = None
    model_used: str = ""
    provider_used: str = ""
    tokens_used: int = 0
    error: str | None = None


class AIProvider(ABC):
    """
    Abstract base class for AI providers.

    All providers (Cerebras, Gemini, Groq, Mistral, NVIDIA, Cloudflare)
    must implement this interface for seamless fallback handling.
    """

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config
        self.status = ProviderStatus.AVAILABLE
        self._cooldowns: dict[str, float] = {}
        self._request_count = 0

    @property
    def name(self) -> str:
        """Provider name."""
        return self.config.name

    @property
    def models(self) -> list[ModelConfig]:
        """Available models sorted by tier (best first)."""
        return sorted(self.config.models, key=lambda m: m.tier)

    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available (API key set, not rate limited)."""
        pass

    @abstractmethod
    def chat_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> CompletionResult:
        """
        Generate a chat completion.

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            model: Specific model to use (or None for best available)
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            CompletionResult with success status and content
        """
        pass

    @abstractmethod
    def json_completion(
        self,
        prompt: str,
        system_prompt: str = "",
        model: str | None = None,
        max_tokens: int = 4096,
    ) -> CompletionResult:
        """
        Generate a JSON-structured completion.

        Args:
            prompt: User prompt requesting JSON output
            system_prompt: System prompt for context
            model: Specific model to use (or None for best available)
            max_tokens: Maximum tokens in response

        Returns:
            CompletionResult with success status and json_content
        """
        pass

    def get_best_model(self, tier: int = 1) -> ModelConfig | None:
        """Get best available model at or above the specified tier."""
        for model in self.models:
            if model.tier >= tier and not self._is_model_cooling_down(model.name):
                return model
        return None

    def _is_model_cooling_down(self, model_name: str) -> bool:
        """Check if a model is in cooldown period."""
        import time
        cooldown_until = self._cooldowns.get(model_name, 0)
        return time.time() < cooldown_until

    def _trigger_cooldown(self, model_name: str, seconds: int = 60) -> None:
        """Put a model in cooldown after an error."""
        import time
        self._cooldowns[model_name] = time.time() + seconds
        logger.warning(f"[{self.name}] Model {model_name} in cooldown for {seconds}s")

    def _clean_json_response(self, text: str) -> str:
        """
        Clean JSON response from LLM output.

        Removes markdown code blocks and extracts JSON content.
        """
        import re

        # Remove markdown code blocks
        text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```\s*", "", text)

        # Find JSON object or array
        match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
        if match:
            text = match.group(0)

        # Remove control characters
        text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)

        return text.strip()

    def _parse_json(self, text: str) -> dict[str, Any] | None:
        """Parse JSON from text, handling common LLM output issues."""
        import json

        cleaned = self._clean_json_response(text)
        if not cleaned:
            return None

        try:
            data = json.loads(cleaned)
            # If we got a list, return first dict item
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                return data[0]
            return data if isinstance(data, dict) else None
        except json.JSONDecodeError as e:
            logger.warning(f"[{self.name}] JSON parse error: {e}")
            return None
