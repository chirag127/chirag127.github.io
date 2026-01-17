from .schema import UnifiedModel

TIER_3_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="deepseek-v3-236b-moe",
        size_billions=236.0,
        description="DeepSeek V3 236B MoE; near-SOTA open model for reasoning and code.",
        max_tokens=164000,
        supports_json=True,
        providers=[
            ("openrouter", "deepseek/deepseek-v3-0324:free"),
            ("github", "DeepSeek-V3-0324"),
            ("nvidia", "deepseek/deepseek-v3"),
        ]
    ),
    UnifiedModel(
        name="qwen3-235b-a22b-instruct",
        size_billions=235.0,
        description="Qwen 3 235B A22B Instruct; massive MoE multilingual/coding.",
        max_tokens=131072,
        supports_json=True,
        providers=[
            ("cerebras", "Qwen-3-235B-A22B-Instruct"),
            ("openrouter", "qwen/qwen3-235b-a22b-instruct:free"),
        ]
    ),
]
