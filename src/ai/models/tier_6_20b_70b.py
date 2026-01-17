from .schema import UnifiedModel

TIER_6_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="mixtral-8x7b-instruct",
        size_billions=56.0,
        description="Mixtral 8x7B MoE - Excellent Code",
        max_tokens=32768,
        providers=[
            ("groq", "mistralai/mixtral-8x7b-instruct-v0.1"),
            ("openrouter", "mistralai/mixtral-8x7b-instruct:free"),
        ],
    ),
    UnifiedModel(
        name="phi-4",
        size_billions=40.0,
        description="Microsoft Phi-4 - Strong Reasoning",
        max_tokens=128000,
        providers=[
            ("github", "Phi-4"),
            ("openrouter", "microsoft/phi-4:free"),
        ],
    ),
    UnifiedModel(
        name="qwen-qwq-32b",
        size_billions=32.0,
        description="Qwen QwQ 32B - Reasoning Focused",
        max_tokens=32768,
        providers=[
            ("groq", "qwen-qwq-32b"),
            ("cloudflare", "@cf/qwen/qwq-32b"),
            ("openrouter", "qwen/qwq-32b:free"),
        ],
    ),
    UnifiedModel(
        name="qwen3-32b-instruct",
        size_billions=32.0,
        description="Qwen 3 32B - Solid Multilingual",
        max_tokens=32768,
        providers=[
            ("groq", "qwen/qwen3-32b"),
            ("cerebras", "Qwen-3-32B"),
            ("openrouter", "qwen/qwen3-32b:free"),
        ],
    ),
    UnifiedModel(
        name="qwen2.5-coder-32b-instruct",
        size_billions=32.0,
        description="Qwen 2.5 Coder 32B - Code Specialized",
        max_tokens=32768,
        providers=[
            ("cloudflare", "@cf/qwen/qwen2.5-coder-32b-instruct"),
            ("openrouter", "qwen/qwen2.5-coder-32b-instruct:free"),
        ],
    ),
    UnifiedModel(
        name="nemotron-3-nano-30b-a3b",
        size_billions=30.0,
        description="NVIDIA Nemotron 3 30B",
        max_tokens=8192,
        providers=[
            ("nvidia", "nvidia/nemotron-3-nano-30b-a3b"),
            ("openrouter", "nvidia/nemotron-3-nano-30b-a3b:free"),
        ],
    ),
    UnifiedModel(
        name="gemma-3-27b-instruct",
        size_billions=27.0,
        description="Gemma 3 27B - Strong Google Model",
        max_tokens=8192,
        providers=[
            ("gemini", "gemma-3-27b-it"),
            ("cloudflare", "@cf/google/gemma-3-27b-instruct"),
            ("openrouter", "google/gemma-3-27b-instruct:free"),
        ],
    ),
    UnifiedModel(
        name="mistral-small-3.1-24b-instruct",
        size_billions=24.0,
        description="Mistral Small 3.1 24B - All-rounder",
        max_tokens=32768,
        providers=[
            ("cloudflare", "@cf/mistral/mistral-small-3.1-24b-instruct"),
            ("github", "Mistral-Small-3.1"),
            ("openrouter", "mistral/mistral-small-3.1-24b-instruct:free"),
        ],
    ),
    UnifiedModel(
        name="codestral-25.01",
        size_billions=22.0,
        description="Codestral - Code Specialized",
        max_tokens=8192,
        providers=[
            ("mistral", "codestral-latest"),
            ("github", "Codestral-25.01"),
            ("openrouter", "mistral/codestral-25.01:free"),
        ],
    ),
    UnifiedModel(
        name="gpt-oss-20b",
        size_billions=20.0,
        description="GPT-OSS 20B - Fallback fallback",
        max_tokens=131072,
        providers=[
            ("openrouter", "openai/gpt-oss-20b:free"),
            ("cerebras", "gpt-oss-20b"),
            ("cloudflare", "@cf/openai/gpt-oss-20b"),
        ]
    ),
]
