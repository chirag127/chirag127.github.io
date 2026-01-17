from .schema import UnifiedModel

TIER_1_MODELS: list[UnifiedModel] = [

    UnifiedModel(
        name="GLM 4.7 1T MoE Cerebras",
        size_billions=1000.0,
        description="GLM-4.7 Ling-1T-style MoE (~1T total params); top-tier reasoning and coding.",
        max_tokens=200000,
        supports_json=True,
        working=True,
        include_in_sidebar=True,
        provider="cerebras",
        api_model_id="zai-glm-4.7"
    ),
    UnifiedModel(
        name="Mistral Large 3 675B Instruct Nvidia",
        size_billions=675.0,
        description="Mistral 'Large 3' 675B MoE; high-end dense model behavior for reasoning.",
        max_tokens=131072,
        supports_json=True,
        working=True,
        include_in_sidebar=True,
        provider="nvidia",
        api_model_id="mistralai/mistral-large-3-675b-instruct-2512"
    ),
    UnifiedModel(
        name="Mistral Large 3 675B Instruct Mistral",
        size_billions=675.0,
        description="Mistral 'Large 3' 675B MoE; high-end dense model behavior for reasoning.",
        max_tokens=131072,
        supports_json=True,
        working=True,
        include_in_sidebar=True,
        provider="mistral",
        api_model_id="mistral-large-2512"
    ),
    UnifiedModel(
        name="DeepSeek R1T2 Chimera OpenRouter",
        size_billions=671.0,
        description="TNG DeepSeek R1T2 Chimera; 671B MoE merge of R1, V3; strong reasoning.",
        max_tokens=164000,
        supports_json=True,
        working=True,
        include_in_sidebar=True,
        provider="openrouter",
        api_model_id="tngtech/deepseek-r1t2-chimera:free"
    ),
    UnifiedModel(
        name="DeepSeek R1 0528 OpenRouter",
        size_billions=671.0,
        description="DeepSeek R1 May 28; 671B total params; SOTA open-source reasoning.",
        max_tokens=164000,
        supports_json=True,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="deepseek/deepseek-r1-0528:free"
    ),
    UnifiedModel(
        name="DeepSeek V3.2 Nvidia",
        size_billions=671.0,
        description="DeepSeek V3 - Top-tier Code & Chat",
        max_tokens=32768,
        working=True,
        include_in_sidebar=True,
        provider="nvidia",
        api_model_id="deepseek-ai/deepseek-v3.2"
    ),

    UnifiedModel(
        name="DeepSeek R1T Chimera OpenRouter",
        size_billions=671.0,
        description="TNG DeepSeek R1T Chimera; MoE merge of R1 and V3; efficiency focused.",
        max_tokens=164000,
        supports_json=True,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="tngtech/deepseek-r1t-chimera:free"
    ),
    UnifiedModel(
        name="Qwen3 Coder 480B MoE OpenRouter",
        size_billions=480.0,
        description="Qwen3-Coder 480B MoE; top ranked for free coding on OpenRouter.",
        max_tokens=262144,
        supports_json=True,
        working=True,  # User implies working=True for listed models even if duplicate
        include_in_sidebar=True,
        provider="openrouter",
        api_model_id="qwen/qwen3-coder:free"
    ),
    UnifiedModel(
        name="R1T Chimera OpenRouter",
        size_billions=450.0,
        description="TNG R1T Chimera; Experimental LLM for creative storytelling.",
        max_tokens=164000,
        supports_json=True,
        working=True,
        include_in_sidebar=True,
        provider="openrouter",
        api_model_id="tngtech/tng-r1t-chimera:free"
    ),
    UnifiedModel(
        name="Llama 3.1 405B Instruct OpenRouter",
        size_billions=405.0,
        description="Meta Llama 3.1 405B Instruct; largest open Llama model.",
        max_tokens=131072,
        supports_json=True,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="meta-llama/llama-3.1-405b-instruct:free"
    ),
    UnifiedModel(
        name="Llama 3.1 405B Instruct GitHub",
        size_billions=405.0,
        description="Meta Llama 3.1 405B Instruct; largest open Llama model.",
        max_tokens=131072,
        supports_json=True,
        working=True,
        include_in_sidebar=True,
        provider="github",
        api_model_id="Meta-Llama-3.1-405B-Instruct"
    ),
    UnifiedModel(
        name="Llama 3.1 405B Instruct Nvidia",
        size_billions=405.0,
        description="Meta Llama 3.1 405B Instruct; largest open Llama model.",
        max_tokens=131072,
        supports_json=True,
        working=True,
        include_in_sidebar=False,
        provider="nvidia",
        api_model_id="meta/llama-3.1-405b-instruct"
    ),
    UnifiedModel(
        name="Hermes 3 Llama 3.1 405B OpenRouter",
        size_billions=405.0,
        description="Nous Hermes 3 fine-tune of Llama 3.1 405B; SOTA assistant behavior.",
        max_tokens=131072,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="nousresearch/hermes-3-llama-3.1-405b:free"
    ),
    UnifiedModel(
        name="Hermes 3 Llama 3.1 405B GitHub",
        size_billions=405.0,
        description="Nous Hermes 3 fine-tune of Llama 3.1 405B; SOTA assistant behavior.",
        max_tokens=131072,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="github",
        api_model_id="Hermes-3-Llama-3.1-405B"
    ),
]
