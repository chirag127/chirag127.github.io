from .schema import UnifiedModel

TIER_4_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="Devstral 2 123B Instruct OpenRouter",
        size_billions=123.0,
        description="Mistral Devstral 2 123B coding MoE; state-of-the-art free coding model.",
        max_tokens=262144,
        supports_json=True,
        working=True, # ✅ Verified Working
        providers=[("openrouter", "mistralai/devstral-2512:free")]
    ),
    UnifiedModel(
        name="Devstral 2 123B Instruct Mistral",
        size_billions=123.0,
        description="Mistral Devstral 2 123B coding MoE; state-of-the-art free coding model.",
        max_tokens=262144,
        supports_json=True,
        working=True, # ✅ Verified Working (Available via codestral-latest or specific ep)
        providers=[("mistral", "codestral-latest")]
    ),
    UnifiedModel(
        name="Mistral Large Latest Mistral",
        size_billions=123.0,
        description="Mistral Large 2 - Top-tier Reasoning",
        max_tokens=32768,
        working=True, # ✅ Verified Working
        providers=[("mistral", "mistral-large-latest")],
    ),
    UnifiedModel(
        name="Mistral Large Latest Nvidia",
        size_billions=123.0,
        description="Mistral Large 2 - Top-tier Reasoning",
        max_tokens=32768,
        working=False, # 404
        providers=[("nvidia", "mistralai/mistral-large-2411")],
    ),
    UnifiedModel(
        name="Mistral Large Latest OpenRouter",
        size_billions=123.0,
        description="Mistral Large 2 - Top-tier Reasoning",
        max_tokens=32768,
        working=False, # 400 Invalid ID
        providers=[("openrouter", "mistral/mistral-large-latest:free")],
    ),
    UnifiedModel(
        name="GPT OSS 120B OpenRouter",
        size_billions=120.0,
        description="OpenAI GPT-OSS 120B; open-weight reasoning model.",
        max_tokens=131072,
        supports_json=True,
        working=False, # 404
        providers=[("openrouter", "openai/gpt-oss-120b:free")]
    ),
    UnifiedModel(
        name="GPT OSS 120B Cerebras",
        size_billions=120.0,
        description="OpenAI GPT-OSS 120B; open-weight reasoning model.",
        max_tokens=131072,
        supports_json=True,
        working=True, # ✅ Verified Working
        providers=[("cerebras", "gpt-oss-120b")]
    ),
    UnifiedModel(
        name="GPT OSS 120B Cloudflare",
        size_billions=120.0,
        description="OpenAI GPT-OSS 120B; open-weight reasoning model.",
        max_tokens=131072,
        supports_json=True,
        working=False, # Auth
        providers=[("cloudflare", "@cf/openai/gpt-oss-120b")]
    ),
    UnifiedModel(
        name="Jamba 1.5 Large GitHub",
        size_billions=120.0,
        description="AI21 Jamba 1.5 Large; hybrid Transformer-Mamba.",
        max_tokens=256000,
        supports_json=True,
        working=False, # 400 Unknown
        providers=[("github", "AI21-Jamba-1.5-Large")]
    ),
    UnifiedModel(
        name="Jamba 1.5 Large Gemini",
        size_billions=120.0,
        description="AI21 Jamba 1.5 Large; hybrid Transformer-Mamba.",
        max_tokens=256000,
        supports_json=True,
        working=False, # 404
        providers=[("gemini", "jamba-1.5-large")]
    ),
    UnifiedModel(
        name="Jamba 1.5 Large OpenRouter",
        size_billions=120.0,
        description="AI21 Jamba 1.5 Large; hybrid Transformer-Mamba.",
        max_tokens=256000,
        supports_json=True,
        working=False, # 400 Invalid ID
        providers=[("openrouter", "ai21/jamba-1.5-large:free")]
    ),
    UnifiedModel(
        name="Qwen1.5 110B Chat Cerebras",
        size_billions=110.0,
        description="Qwen1.5 110B Chat; strong on multilingual and code tasks.",
        max_tokens=32000,
        supports_json=True,
        working=False, # 404
        providers=[("cerebras", "Qwen1.5-110B-Chat")]
    ),
    UnifiedModel(
        name="Command R Plus 104B GitHub",
        size_billions=104.0,
        description="Cohere Command R+ 104B - RAG Specialist",
        max_tokens=128000,
        working=False, # 400 (Bad Request Context/Params)
        providers=[("github", "Cohere-Command-R-plus-08-2024")],
    ),
    UnifiedModel(
        name="Command R Plus 104B OpenRouter",
        size_billions=104.0,
        description="Cohere Command R+ 104B - RAG Specialist",
        max_tokens=128000,
        working=False, # 404
        providers=[("openrouter", "cohere/command-r-plus:free")],
    ),
    UnifiedModel(
        name="DeepSeek R1 Huge OpenRouter",
        size_billions=100.0,
        description="DeepSeek R1 (100B+); reasoning-focused model.",
        max_tokens=164000,
        supports_json=True,
        working=False, # 500/Exception
        providers=[("openrouter", "deepseek/deepseek-r1-0528:free")]
    ),
    UnifiedModel(
        name="DeepSeek R1 Huge GitHub",
        size_billions=100.0,
        description="DeepSeek R1 (100B+); reasoning-focused model.",
        max_tokens=164000,
        supports_json=True,
        working=True, # ✅ Verified Working
        providers=[("github", "DeepSeek-R1-0528")]
    ),
]
