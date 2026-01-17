from .schema import UnifiedModel

TIER_1_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="GLM 4.6 1T MoE Cerebras",
        size_billions=1000.0,
        description="GLM-4.6 Ling-1T-style MoE (~1T total params); top-tier reasoning and coding.",
        max_tokens=200000,
        supports_json=True,
        providers=[("cerebras", "z.ai/glm-4.6")]
    ),
    UnifiedModel(
        name="GLM 4.6 1T MoE OpenRouter",
        size_billions=1000.0,
        description="GLM-4.6 Ling-1T-style MoE (~1T total params); top-tier reasoning and coding.",
        max_tokens=200000,
        supports_json=True,
        providers=[("openrouter", "z-ai/glm-4.6:free")]
    ),
    UnifiedModel(
        name="Mistral Large 3 675B MoE Nvidia",
        size_billions=675.0,
        description="Mistral 'Large 3' 675B MoE; high-end dense model behavior for reasoning.",
        max_tokens=131072,
        supports_json=True,
        providers=[("nvidia", "mistral/mistral-large-3-675b-instruct")]
    ),
    UnifiedModel(
        name="Mistral Large 3 675B MoE Mistral",
        size_billions=675.0,
        description="Mistral 'Large 3' 675B MoE; high-end dense model behavior for reasoning.",
        max_tokens=131072,
        supports_json=True,
        providers=[("mistral", "mistral-large-3")]
    ),
    UnifiedModel(
        name="DeepSeek V3 Nvidia",
        size_billions=671.0,
        description="DeepSeek V3 - Top-tier Code & Chat",
        max_tokens=32768,
        providers=[("nvidia", "deepseek-ai/deepseek-v3")]
    ),
    UnifiedModel(
        name="DeepSeek V3 OpenRouter",
        size_billions=671.0,
        description="DeepSeek V3 - Top-tier Code & Chat",
        max_tokens=32768,
        providers=[("openrouter", "deepseek/deepseek-v3:free")]
    ),
    UnifiedModel(
        name="Qwen3 Coder 480B MoE OpenRouter",
        size_billions=480.0,
        description="Qwen3-Coder 480B MoE; top ranked for free coding on OpenRouter.",
        max_tokens=262144,
        supports_json=True,
        providers=[("openrouter", "qwen/qwen3-coder:free")]
    ),
    UnifiedModel(
        name="Llama 3.1 405B Instruct OpenRouter",
        size_billions=405.0,
        description="Meta Llama 3.1 405B Instruct; largest open Llama model.",
        max_tokens=131072,
        supports_json=True,
        providers=[("openrouter", "meta-llama/llama-3.1-405b-instruct:free")]
    ),
    UnifiedModel(
        name="Llama 3.1 405B Instruct GitHub",
        size_billions=405.0,
        description="Meta Llama 3.1 405B Instruct; largest open Llama model.",
        max_tokens=131072,
        supports_json=True,
        providers=[("github", "Meta-Llama-3.1-405B-Instruct")]
    ),
    UnifiedModel(
        name="Llama 3.1 405B Instruct Nvidia",
        size_billions=405.0,
        description="Meta Llama 3.1 405B Instruct; largest open Llama model.",
        max_tokens=131072,
        supports_json=True,
        providers=[("nvidia", "meta/llama-3.1-405b-instruct")]
    ),
    UnifiedModel(
        name="Llama 3.1 405B Instruct Mistral",
        size_billions=405.0,
        description="Meta Llama 3.1 405B Instruct; largest open Llama model.",
        max_tokens=131072,
        supports_json=True,
        providers=[("mistral", "meta-llama/llama-3.1-405b-instruct")]
    ),
    UnifiedModel(
        name="Hermes 3 Llama 3.1 405B OpenRouter",
        size_billions=405.0,
        description="Nous Hermes 3 fine-tune of Llama 3.1 405B; SOTA assistant behavior.",
        max_tokens=131072,
        supports_json=True,
        providers=[("openrouter", "nousresearch/hermes-3-llama-3.1-405b:free")]
    ),
    UnifiedModel(
        name="Hermes 3 Llama 3.1 405B GitHub",
        size_billions=405.0,
        description="Nous Hermes 3 fine-tune of Llama 3.1 405B; SOTA assistant behavior.",
        max_tokens=131072,
        supports_json=True,
        providers=[("github", "Hermes-3-Llama-3.1-405B")]
    ),
]
