from .schema import UnifiedModel

TIER_1_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="glm-4.6-1t-moe",
        size_billions=1000.0,
        description="GLM-4.6 Ling-1T-style MoE (~1T total params); top-tier reasoning and coding.",
        max_tokens=200000,
        supports_json=True,
        providers=[
            ("cerebras", "z.ai/glm-4.6"),
            ("openrouter", "z-ai/glm-4.6:free"),
        ]
    ),
    UnifiedModel(
        name="mistral-large-3-675b-moe",
        size_billions=675.0,
        description="Mistral 'Large 3' 675B MoE; high-end dense model behavior for reasoning.",
        max_tokens=131072,
        supports_json=True,
        providers=[
            ("nvidia", "mistral/mistral-large-3-675b-instruct"),
            ("mistral", "mistral-large-3"),
        ]
    ),
    UnifiedModel(
        name="deepseek-v3", # Keeping original name for compatibility if needed, or update to specific
        size_billions=671.0,
        description="DeepSeek V3 - Top-tier Code & Chat",
        max_tokens=32768,
        providers=[
            ("nvidia", "deepseek-ai/deepseek-v3"),
            ("openrouter", "deepseek/deepseek-v3:free"),
        ]
    ),
    UnifiedModel(
        name="qwen3-coder-480b-moe",
        size_billions=480.0,
        description="Qwen3-Coder 480B MoE; top ranked for free coding on OpenRouter.",
        max_tokens=262144,
        supports_json=True,
        providers=[
            ("openrouter", "qwen/qwen3-coder:free"),
        ]
    ),
    UnifiedModel(
        name="llama-3.1-405b-instruct",
        size_billions=405.0,
        description="Meta Llama 3.1 405B Instruct; largest open Llama model.",
        max_tokens=131072,
        supports_json=True,
        providers=[
            ("openrouter", "meta-llama/llama-3.1-405b-instruct:free"),
            ("github", "Meta-Llama-3.1-405B-Instruct"),
            ("nvidia", "meta/llama-3.1-405b-instruct"),
            ("mistral", "meta-llama/llama-3.1-405b-instruct"),
        ]
    ),
    UnifiedModel(
        name="hermes-3-llama-3.1-405b",
        size_billions=405.0,
        description="Nous Hermes 3 fine-tune of Llama 3.1 405B; SOTA assistant behavior.",
        max_tokens=131072,
        supports_json=True,
        providers=[
            ("openrouter", "nousresearch/hermes-3-llama-3.1-405b:free"),
            ("github", "Hermes-3-Llama-3.1-405B"),
        ]
    ),
]
