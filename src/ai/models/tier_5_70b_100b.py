from .schema import UnifiedModel

TIER_5_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="llama-3.2-90b-vision-instruct",
        size_billions=90.0,
        description="Llama 3.2 90B Vision - Multimodal Code",
        max_tokens=8192,
        providers=[
            ("groq", "llama-3.2-90b-vision-preview"),
            ("github", "Llama-3.2-90B-Vision-Instruct"),
            ("openrouter", "meta-llama/llama-3.2-90b-vision-instruct:free"),
        ],
    ),
    UnifiedModel(
        name="qwen-2.5-72b-instruct",
        size_billions=72.0,
        description="Qwen 2.5 72B - Strong Multilingual",
        max_tokens=32768,
        providers=[
            ("nvidia", "qwen/qwen2.5-72b-instruct"),
            ("openrouter", "qwen/qwen2.5-72b-instruct:free"),
        ],
    ),
    UnifiedModel(
        name="llama-3.3-70b-instruct",
        size_billions=70.0,
        description="Meta Llama 3.3 70B - Very Strong General",
        max_tokens=8192,
        providers=[
            ("groq", "llama-3.3-70b-versatile"),
            ("cerebras", "llama-3.3-70b"),
            ("nvidia", "meta/llama-3.3-70b-instruct"),
            ("cloudflare", "@cf/meta/llama-3.3-70b-instruct-fp8"),
            ("openrouter", "meta-llama/llama-3.3-70b-instruct:free"),
            ("github", "Meta-Llama-3.3-70B-Instruct"),
        ],
    ),
    UnifiedModel(
        name="deepseek-r1-distill-llama-70b",
        size_billions=70.0,
        description="DeepSeek R1 Distill 70B - Reasoning",
        max_tokens=32768,
        providers=[
            ("groq", "deepseek-r1-distill-llama-70b"),
            ("nvidia", "deepseek-ai/deepseek-r1-distill-llama-70b"),
            ("openrouter", "deepseek/deepseek-r1-distill-llama-70b:free"),
        ],
    ),
    UnifiedModel(
        name="llama-3.1-70b-instruct",
        size_billions=70.0,
        description="Meta Llama 3.1 70B - Strong Reasoning",
        max_tokens=8192,
        providers=[
            ("nvidia", "meta/llama-3.1-70b-instruct"),
            ("cloudflare", "@cf/meta/llama-3.1-70b-instruct"),
            ("openrouter", "meta-llama/llama-3.1-70b-instruct:free"),
        ],
    ),
]
