from .schema import UnifiedModel

TIER_6_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="Mixtral 8x7B Instruct Groq",
        size_billions=56.0,
        description="Mixtral 8x7B MoE - Excellent Code",
        max_tokens=32768,
        working=True,
        include_in_sidebar=True,
        provider="groq",
        api_model_id="mistralai/mixtral-8x7b-instruct-v0.1"
    ),
    UnifiedModel(
        name="Mixtral 8x7B Instruct OpenRouter",
        size_billions=56.0,
        description="Mixtral 8x7B MoE - Excellent Code",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="mistralai/mixtral-8x7b-instruct:free"
    ),
    UnifiedModel(
        name="Phi 4 GitHub",
        size_billions=40.0,
        description="Microsoft Phi-4 - Strong Reasoning",
        max_tokens=128000,
        working=True,
        include_in_sidebar=False,
        provider="github",
        api_model_id="Phi-4"
    ),
    UnifiedModel(
        name="Phi 4 OpenRouter",
        size_billions=40.0,
        description="Microsoft Phi-4 - Strong Reasoning",
        max_tokens=128000,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="microsoft/phi-4:free"
    ),
    UnifiedModel(
        name="Qwen QwQ 32B Groq",
        size_billions=32.0,
        description="Qwen QwQ 32B - Reasoning Focused",
        max_tokens=32768,
        working=True,
        include_in_sidebar=True,
        provider="groq",
        api_model_id="qwen-qwq-32b"
    ),
    UnifiedModel(
        name="Qwen QwQ 32B Cloudflare",
        size_billions=32.0,
        description="Qwen QwQ 32B - Reasoning Focused",
        max_tokens=32768,
        working=False,
        include_in_sidebar=False,
        provider="cloudflare",
        api_model_id="@cf/qwen/qwq-32b"
    ),
    UnifiedModel(
        name="Qwen QwQ 32B OpenRouter",
        size_billions=32.0,
        description="Qwen QwQ 32B - Reasoning Focused",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="qwen/qwq-32b:free"
    ),
    UnifiedModel(
        name="Qwen3 32B Instruct Groq",
        size_billions=32.0,
        description="Qwen 3 32B - Solid Multilingual",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="groq",
        api_model_id="qwen/qwen3-32b"
    ),
    UnifiedModel(
        name="Qwen3 32B Instruct Cerebras",
        size_billions=32.0,
        description="Qwen 3 32B - Solid Multilingual",
        max_tokens=32768,
        working=True,
        include_in_sidebar=True,
        provider="cerebras",
        api_model_id="Qwen-3-32B"
    ),
    UnifiedModel(
        name="Qwen3 32B Instruct OpenRouter",
        size_billions=32.0,
        description="Qwen 3 32B - Solid Multilingual",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="qwen/qwen3-32b:free"
    ),
    UnifiedModel(
        name="Qwen 2.5 Coder 32B Instruct Cloudflare",
        size_billions=32.0,
        description="Qwen 2.5 Coder 32B - Code Specialized",
        max_tokens=32768,
        working=False,
        include_in_sidebar=False,
        provider="cloudflare",
        api_model_id="@cf/qwen/qwen2.5-coder-32b-instruct"
    ),
    UnifiedModel(
        name="Qwen 2.5 Coder 32B Instruct OpenRouter",
        size_billions=32.0,
        description="Qwen 2.5 Coder 32B - Code Specialized",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="qwen/qwen2.5-coder-32b-instruct:free"
    ),
    UnifiedModel(
        name="Nemotron 3 Nano 30B Nvidia",
        size_billions=30.0,
        description="NVIDIA Nemotron 3 30B",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="nvidia",
        api_model_id="nvidia/nemotron-3-nano-30b-a3b"
    ),
    UnifiedModel(
        name="Nemotron 3 Nano 30B OpenRouter",
        size_billions=30.0,
        description="NVIDIA Nemotron 3 30B",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="nvidia/nemotron-3-nano-30b-a3b:free"
    ),
    UnifiedModel(
        name="Gemma 3 27B Instruct Gemini",
        size_billions=27.0,
        description="Gemma 3 27B - Strong Google Model",
        max_tokens=8192,
        working=True,
        include_in_sidebar=True,
        provider="gemini",
        api_model_id="gemma-3-27b-it"
    ),
    UnifiedModel(
        name="Mistral Small 3.1 24B Instruct Cloudflare",
        size_billions=24.0,
        description="Mistral Small 3.1 24B - All-rounder",
        max_tokens=32768,
        working=False,
        include_in_sidebar=False,
        provider="cloudflare",
        api_model_id="@cf/mistral/mistral-small-3.1-24b-instruct"
    ),
    UnifiedModel(
        name="Mistral Small 3.1 24B Instruct GitHub",
        size_billions=24.0,
        description="Mistral Small 3.1 24B - All-rounder",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="github",
        api_model_id="Mistral-Small-3.1"
    ),
    UnifiedModel(
        name="Mistral Small 3.1 24B Instruct OpenRouter",
        size_billions=24.0,
        description="Mistral Small 3.1 24B - All-rounder",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="mistral/mistral-small-3.1-24b-instruct:free"
    ),
    UnifiedModel(
        name="Codestral 25.01 Mistral",
        size_billions=22.0,
        description="Codestral - Code Specialized",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="mistral",
        api_model_id="codestral-latest"
    ),
    UnifiedModel(
        name="Codestral 25.01 GitHub",
        size_billions=22.0,
        description="Codestral - Code Specialized",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="github",
        api_model_id="Codestral-25.01"
    ),
    UnifiedModel(
        name="Codestral 25.01 OpenRouter",
        size_billions=22.0,
        description="Codestral - Code Specialized",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="mistral/codestral-25.01:free"
    ),
    UnifiedModel(
        name="GPT OSS 20B OpenRouter",
        size_billions=20.0,
        description="GPT-OSS 20B - Fallback fallback",
        max_tokens=131072,
        working=False,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="openai/gpt-oss-20b:free"
    ),
    UnifiedModel(
        name="GPT OSS 20B Cerebras",
        size_billions=20.0,
        description="GPT-OSS 20B - Fallback fallback",
        max_tokens=131072,
        working=True,
        include_in_sidebar=True,
        provider="cerebras",
        api_model_id="gpt-oss-120b"
    ),
    UnifiedModel(
        name="GPT OSS 20B Cloudflare",
        size_billions=20.0,
        description="GPT-OSS 20B - Fallback fallback",
        max_tokens=131072,
        working=False,
        include_in_sidebar=False,
        provider="cloudflare",
        api_model_id="@cf/openai/gpt-oss-20b"
    ),
    UnifiedModel(
        name="GLM 4.5 Air OpenRouter",
        size_billions=20.0,
        description="Z.AI GLM 4.5 Air; Lightweight MoE for agents.",
        max_tokens=131072,
        supports_json=True,
        working=True,
        include_in_sidebar=True,
        provider="openrouter",
        api_model_id="z-ai/glm-4.5-air:free"
    ),
]
