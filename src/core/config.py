import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ModelConfig:
    name: str
    tier: int
    description: str


class Settings:
    """
    Hyper-Configurable Settings Module.
    Loads from environment variables with strict validation.
    Supports ALL API providers for maximum automation coverage.
    """

    def __init__(self) -> None:
        # === GITHUB ===
        self.GH_TOKEN: str | None = os.getenv("GH_TOKEN")
        self.GH_USERNAME: str = os.getenv("GH_USERNAME", "chirag127")

        # === JULES AI ===
        self.JULES_API_KEY: str | None = os.getenv("JULES_API_KEY")
        self.JULES_BASE_URL: str = "https://jules.googleapis.com/v1alpha"
        self.JULES_DAILY_LIMIT: int = int(os.getenv("JULES_DAILY_LIMIT", "100"))
        self.JULES_POLL_INTERVAL: int = int(os.getenv("JULES_POLL_INTERVAL", "30"))
        self.JULES_MAX_WAIT: int = int(os.getenv("JULES_MAX_WAIT", "3600"))

        # === PRIMARY AI: CEREBRAS ===
        self.CEREBRAS_API_KEY: str | None = os.getenv("CEREBRAS_API_KEY")
        if not self.CEREBRAS_API_KEY:
            raise ValueError("❌ CRITICAL: CEREBRAS_API_KEY is missing in .env")
        self.CEREBRAS_BASE_URL: str = "https://api.cerebras.ai/v1"
        self.CEREBRAS_MAX_TOKENS: int = 32768
        self.CEREBRAS_MODELS: list[ModelConfig] = [
            ModelConfig("zai-glm-4.6", 1, "Z.ai GLM 4.6 (357B)"),
            ModelConfig("qwen-3-235b-a22b-instruct-2507", 2, "Qwen 3 235B Instruct"),
            ModelConfig("gpt-oss-120b", 3, "GPT OSS 120B"),
            ModelConfig("llama-3.3-70b", 4, "Llama 3.3 70B"),
            ModelConfig("qwen-3-32b", 5, "Qwen 3 32B"),
            ModelConfig("llama3.1-8b", 6, "Llama 3.1 8B"),
        ]

        # === BACKUP AI: GROQ ===
        self.GROQ_API_KEY: str | None = os.getenv("GROQ_API_KEY")
        self.GROQ_BASE_URL: str = "https://api.groq.com/openai/v1"
        self.GROQ_MODELS: list[ModelConfig] = [
            ModelConfig("openai/gpt-oss-120b", 1, "GPT OSS 120B"),
            ModelConfig("llama-3.3-70b-versatile", 2, "Llama 3.3 70B"),
            ModelConfig("qwen/qwen3-32b", 3, "Qwen 3 32B"),
            ModelConfig("llama-3.1-8b-instant", 4, "Llama 3.1 8B"),
        ]

        # === BACKUP AI: GEMINI ===
        self.GEMINI_API_KEY: str | None = os.getenv("GEMINI_API_KEY")
        self.GEMINI_API_KEYS: list[str] = [
            k.strip() for k in os.getenv("GEMINI_API_KEYS", "").split(",") if k.strip()
        ]
        self.GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"
        self.GEMINI_MODELS: list[ModelConfig] = [
            ModelConfig("gemma-3-27b-instruct", 1, "Gemma 3 27B"),
            ModelConfig("gemma-3-12b-instruct", 2, "Gemma 3 12B"),
            ModelConfig("gemma-3-4b-instruct", 3, "Gemma 3 4B"),
            ModelConfig("gemma-3-1b-instruct", 4, "Gemma 3 1B"),
        ]

        # === BACKUP AI: MISTRAL ===
        self.MISTRAL_API_KEY: str | None = os.getenv("MISTRAL_API_KEY")
        self.MISTRAL_BASE_URL: str = "https://api.mistral.ai/v1"
        self.MISTRAL_MODELS: list[ModelConfig] = [
            ModelConfig("mistral-large", 1, "Mistral Large"),
            ModelConfig("mistral-small-3.1-24b-instruct", 2, "Mistral Small 24B"),
            ModelConfig("open-mistral-nemo", 3, "Mistral Nemo"),
        ]

        # === BACKUP AI: NVIDIA NIM ===
        self.NVIDIA_API_KEY: str | None = os.getenv("NVIDIA_API_KEY")
        self.NVIDIA_BASE_URL: str = "https://api.nvidia.com/nim"
        self.NVIDIA_MODELS: list[ModelConfig] = [
            ModelConfig("meta-llama/llama-3.1-405b-instruct", 1, "Llama 3.1 405B"),
            ModelConfig("meta-llama/llama-3.3-70b-instruct", 2, "Llama 3.3 70B"),
        ]

        # === BACKUP AI: CLOUDFLARE WORKERS AI ===
        self.CLOUDFLARE_API_TOKEN: str | None = os.getenv("CLOUDFLARE_API_TOKEN")
        self.CLOUDFLARE_ACCOUNT_ID: str | None = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        self.CLOUDFLARE_BASE_URL: str = f"https://api.cloudflare.com/client/v4/accounts/{self.CLOUDFLARE_ACCOUNT_ID}/ai/run"
        self.CLOUDFLARE_MODELS: list[ModelConfig] = [
            ModelConfig("@cf/meta/llama-3.1-8b-instruct", 1, "Llama 3.1 8B"),
        ]

        # === SEARCH APIs (Multi-Provider Fallback) ===
        self.BRAVE_API_KEY: str | None = os.getenv("BRAVE_API_KEY")
        self.EXA_API_KEY: str | None = os.getenv("EXA_API_KEY")
        self.TAVILY_API_KEY: str | None = os.getenv("TAVILY_API_KEY")

        # === TREND DISCOVERY APIS ===
        self.PRODUCT_HUNT_API_KEY: str | None = os.getenv("PRODUCT_HUNT_API_KEY")
        self.REDDIT_CLIENT_ID: str | None = os.getenv("REDDIT_CLIENT_ID")
        self.REDDIT_CLIENT_SECRET: str | None = os.getenv("REDDIT_CLIENT_SECRET")
        self.DEV_TO_API_KEY: str | None = os.getenv("DEV_TO_API_KEY")
        self.NEWSAPI_AI_KEY: str | None = os.getenv("NEWSAPI_AI_KEY")
        self.HF_TOKEN: str | None = os.getenv("HF_TOKEN")
        self.KAGGLE_USERNAME: str | None = os.getenv("KAGGLE_USERNAME")
        self.KAGGLE_KEY: str | None = os.getenv("KAGGLE_KEY")
        self.SEMANTIC_SCHOLAR_API_KEY: str | None = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        self.UNPAYWALL_EMAIL: str | None = os.getenv("UNPAYWALL_EMAIL")

        # === CIRCUIT BREAKER ===
        self.COOLDOWN_FLASH: int = int(os.getenv("COOLDOWN_FLASH", "30"))
        self.COOLDOWN_PRO: int = int(os.getenv("COOLDOWN_PRO", "300"))
        self.MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "20"))

        # === PATHS ===
        self.CACHE_DIR: str = os.getenv("CACHE_DIR", os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "Cache"
        ))
        self.AGENTS_MD_PATH: str = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "AGENTS.md"
        )

        # === GITHUB API ===
        self.GITHUB_GRAPHQL_URL: str = "https://api.github.com/graphql"
        self.GITHUB_API_URL: str = "https://api.github.com"

    def get_available_providers(self) -> list[str]:
        """Returns list of available AI providers based on configured keys."""
        providers = ["cerebras"]  # Always available (required)
        if self.GROQ_API_KEY:
            providers.append("groq")
        if self.GEMINI_API_KEY or self.GEMINI_API_KEYS:
            providers.append("gemini")
        if self.MISTRAL_API_KEY:
            providers.append("mistral")
        if self.NVIDIA_API_KEY:
            providers.append("nvidia")
        if self.CLOUDFLARE_API_TOKEN and self.CLOUDFLARE_ACCOUNT_ID:
            providers.append("cloudflare")
        return providers

    def get_available_trend_sources(self) -> list[str]:
        """Returns list of available trend discovery sources."""
        sources = [
            "arxiv", "papers_with_code", "hacker_news", "lobsters",
            "github_trending", "techcrunch_rss", "hashnode", "stackoverflow"
        ]  # Always available (no API key needed)

        if self.PRODUCT_HUNT_API_KEY:
            sources.append("product_hunt")
        if self.REDDIT_CLIENT_ID and self.REDDIT_CLIENT_SECRET:
            sources.append("reddit")
        if self.DEV_TO_API_KEY:
            sources.append("devto")
        if self.NEWSAPI_AI_KEY:
            sources.append("newsapi")
        if self.HF_TOKEN:
            sources.append("huggingface")
        if self.KAGGLE_USERNAME and self.KAGGLE_KEY:
            sources.append("kaggle")
        if self.SEMANTIC_SCHOLAR_API_KEY:
            sources.append("semantic_scholar")

        # SearXNG always available (no key needed)
        sources.append("searxng")

        return sources
