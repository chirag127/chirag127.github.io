from .schema import UnifiedModel

TIER_2_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="llama-4-maverick-400b",
        size_billions=400.0,
        description="Llama 4 Maverick 400B - Next Gen MoE",
        max_tokens=8192,
        providers=[
            ("openrouter", "meta-llama/llama-4-maverick:free"),
        ],
    ),
    UnifiedModel(
        name="mimo-v2-flash-309b-moe",
        size_billions=309.0,
        description="Xiaomi MiMo V2 Flash 309B MoE; strong coding model on OpenRouter.",
        max_tokens=262144,
        supports_json=True,
        providers=[
            ("openrouter", "xiaomi/mimo-v2-flash:free"),
            ("cloudflare", "@cf/xiaomi/mimo-v2-flash"),
        ]
    ),
]
