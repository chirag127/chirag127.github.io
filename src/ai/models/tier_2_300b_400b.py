from .schema import UnifiedModel

TIER_2_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="Llama 4 Maverick 400B OpenRouter",
        size_billions=400.0,
        description="Llama 4 Maverick 400B - Next Gen MoE",
        max_tokens=8192,
        working=False,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="meta-llama/llama-4-maverick:free"
    ),
    UnifiedModel(
        name="MiMo V2 Flash 309B MoE OpenRouter",
        size_billions=309.0,
        description="Xiaomi MiMo V2 Flash 309B MoE; strong coding model on OpenRouter.",
        max_tokens=262144,
        supports_json=True,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="xiaomi/mimo-v2-flash:free"
    ),
    UnifiedModel(
        name="MiMo V2 Flash 309B MoE Cloudflare",
        size_billions=309.0,
        description="Xiaomi MiMo V2 Flash 309B MoE; strong coding model on OpenRouter.",
        max_tokens=262144,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="cloudflare",
        api_model_id="@cf/xiaomi/mimo-v2-flash"
    ),
]
