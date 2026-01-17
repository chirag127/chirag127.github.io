from .schema import UnifiedModel

TIER_4_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="Devstral 2 123B Instruct OpenRouter",
        size_billions=123.0,
        description="Mistral Devstral 2 123B coding MoE; state-of-the-art free coding model.",
        max_tokens=262144,
        supports_json=True,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="mistralai/devstral-2512:free"
    ),
    UnifiedModel(
        name="Devstral 2 123B Instruct Mistral",
        size_billions=123.0,
        description="Mistral Devstral 2 123B coding MoE; state-of-the-art free coding model.",
        max_tokens=262144,
        supports_json=True,
        working=True,
        include_in_sidebar=False,
        provider="mistral",
        api_model_id="codestral-latest"
    ),
    UnifiedModel(
        name="Mistral Large Latest Mistral",
        size_billions=123.0,
        description="Mistral Large 2 - Top-tier Reasoning",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="mistral",
        api_model_id="mistral-large-latest"
    ),
    UnifiedModel(
        name="Mistral Large Latest Nvidia",
        size_billions=123.0,
        description="Mistral Large 2 - Top-tier Reasoning",
        max_tokens=32768,
        working=False,
        include_in_sidebar=False,
        provider="nvidia",
        api_model_id="mistralai/mistral-large-2411"
    ),
    UnifiedModel(
        name="Mistral Large Latest OpenRouter",
        size_billions=123.0,
        description="Mistral Large 2 - Top-tier Reasoning",
        max_tokens=32768,
        working=False,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="mistral/mistral-large-latest:free"
    ),
    UnifiedModel(
        name="GPT OSS 120B OpenRouter",
        size_billions=120.0,
        description="OpenAI GPT-OSS 120B; open-weight reasoning model.",
        max_tokens=131072,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="openai/gpt-oss-120b:free"
    ),
    UnifiedModel(
        name="GPT OSS 120B Cerebras",
        size_billions=120.0,
        description="OpenAI GPT-OSS 120B; open-weight reasoning model.",
        max_tokens=131072,
        supports_json=True,
        working=True,
        include_in_sidebar=False,
        provider="cerebras",
        api_model_id="gpt-oss-120b"
    ),
    UnifiedModel(
        name="GPT OSS 120B Cloudflare",
        size_billions=120.0,
        description="OpenAI GPT-OSS 120B; open-weight reasoning model.",
        max_tokens=131072,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="cloudflare",
        api_model_id="@cf/openai/gpt-oss-120b"
    ),
    UnifiedModel(
        name="Jamba 1.5 Large GitHub",
        size_billions=120.0,
        description="AI21 Jamba 1.5 Large; hybrid Transformer-Mamba.",
        max_tokens=256000,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="github",
        api_model_id="AI21-Jamba-1.5-Large"
    ),
    UnifiedModel(
        name="Jamba 1.5 Large Gemini",
        size_billions=120.0,
        description="AI21 Jamba 1.5 Large; hybrid Transformer-Mamba.",
        max_tokens=256000,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="gemini",
        api_model_id="jamba-1.5-large"
    ),
    UnifiedModel(
        name="Jamba 1.5 Large OpenRouter",
        size_billions=120.0,
        description="AI21 Jamba 1.5 Large; hybrid Transformer-Mamba.",
        max_tokens=256000,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="ai21/jamba-1.5-large:free"
    ),
    UnifiedModel(
        name="Qwen1.5 110B Chat Cerebras",
        size_billions=110.0,
        description="Qwen1.5 110B Chat; strong on multilingual and code tasks.",
        max_tokens=32000,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="cerebras",
        api_model_id="Qwen1.5-110B-Chat"
    ),
    UnifiedModel(
        name="Command R Plus 104B GitHub",
        size_billions=104.0,
        description="Cohere Command R+ 104B - RAG Specialist",
        max_tokens=128000,
        working=False,
        include_in_sidebar=False,
        provider="github",
        api_model_id="Cohere-Command-R-plus-08-2024"
    ),
    UnifiedModel(
        name="Command R Plus 104B OpenRouter",
        size_billions=104.0,
        description="Cohere Command R+ 104B - RAG Specialist",
        max_tokens=128000,
        working=False,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="cohere/command-r-plus:free"
    ),
]
