from .schema import UnifiedModel

TIER_3_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="DeepSeek V3 236B MoE OpenRouter",
        size_billions=236.0,
        description="DeepSeek V3 236B MoE; near-SOTA open model for reasoning and code.",
        max_tokens=164000,
        supports_json=True,
        working=False, # 400 Invalid ID
        providers=[("openrouter", "deepseek/deepseek-v3-0324:free")]
    ),
    UnifiedModel(
        name="DeepSeek V3 236B MoE GitHub",
        size_billions=236.0,
        description="DeepSeek V3 236B MoE; near-SOTA open model for reasoning and code.",
        max_tokens=164000,
        supports_json=True,
        working=True, # ✅ Verified Working
        providers=[("github", "DeepSeek-V3-0324")]
    ),
    UnifiedModel(
        name="DeepSeek V3 236B MoE Nvidia",
        size_billions=236.0,
        description="DeepSeek V3 236B MoE; near-SOTA open model for reasoning and code.",
        max_tokens=164000,
        supports_json=True,
        working=False, # 404
        providers=[("nvidia", "deepseek/deepseek-v3")]
    ),
    UnifiedModel(
        name="Qwen3 235B A22B Instruct Cerebras",
        size_billions=235.0,
        description="Qwen 3 235B A22B Instruct; massive MoE multilingual/coding.",
        max_tokens=131072,
        supports_json=True,
        working=False, # 404
        providers=[("cerebras", "Qwen-3-235B-A22B-Instruct")]
    ),
    UnifiedModel(
        name="Qwen3 235B A22B Instruct OpenRouter",
        size_billions=235.0,
        description="Qwen 3 235B A22B Instruct; massive MoE multilingual/coding.",
        max_tokens=131072,
        supports_json=True,
        working=False, # 400 Invalid ID
        providers=[("openrouter", "qwen/qwen3-235b-a22b-instruct:free")]
    ),
]
