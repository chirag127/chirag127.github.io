from .schema import UnifiedModel

TIER_4_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="devstral-2-123b-instruct",
        size_billions=123.0,
        description="Mistral Devstral 2 123B coding MoE; state-of-the-art free coding model.",
        max_tokens=262144,
        supports_json=True,
        providers=[
            ("openrouter", "mistralai/devstral-2512:free"),
            ("mistral", "codestral-latest"),
            ("mistral", "mistral-large-3-675b-instruct-2512"), # Fallback
        ]
    ),
    UnifiedModel(
        name="mistral-large-latest",
        size_billions=123.0,
        description="Mistral Large 2 - Top-tier Reasoning",
        max_tokens=32768,
        providers=[
            ("mistral", "mistral-large-latest"),
            ("nvidia", "mistralai/mistral-large-2411"),
            ("openrouter", "mistral/mistral-large-latest:free"),
        ],
    ),
    UnifiedModel(
        name="gpt-oss-120b",
        size_billions=120.0,
        description="OpenAI GPT-OSS 120B; open-weight reasoning model.",
        max_tokens=131072,
        supports_json=True,
        providers=[
            ("openrouter", "openai/gpt-oss-120b:free"),
            ("cerebras", "gpt-oss-120b"),
            ("cloudflare", "@cf/openai/gpt-oss-120b"),
        ]
    ),
    UnifiedModel(
        name="jamba-1.5-large",
        size_billions=120.0,
        description="AI21 Jamba 1.5 Large; hybrid Transformer-Mamba.",
        max_tokens=256000,
        supports_json=True,
        providers=[
            ("github", "AI21-Jamba-1.5-Large"),
            ("gemini", "jamba-1.5-large"), # Assuming available via some gateway or defined generic
            ("openrouter", "ai21/jamba-1.5-large:free"),
        ]
    ),
    UnifiedModel(
        name="qwen1.5-110b-chat",
        size_billions=110.0,
        description="Qwen1.5 110B Chat; strong on multilingual and code tasks.",
        max_tokens=32000,
        supports_json=True,
        providers=[
            ("cerebras", "Qwen1.5-110B-Chat"),
        ]
    ),
    UnifiedModel(
        name="command-r-plus-104b",
        size_billions=104.0,
        description="Cohere Command R+ 104B - RAG Specialist",
        max_tokens=128000,
        providers=[
            ("github", "Cohere-Command-R-plus-08-2024"),
            ("openrouter", "cohere/command-r-plus:free"),
        ],
    ),
    UnifiedModel(
        name="deepseek-r1-huge",
        size_billions=100.0,
        description="DeepSeek R1 (100B+); reasoning-focused model.",
        max_tokens=164000,
        supports_json=True,
        providers=[
            ("openrouter", "deepseek/deepseek-r1-0528:free"),
            ("github", "DeepSeek-R1-0528"),
        ]
    ),
]
