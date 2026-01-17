from .schema import UnifiedModel

TIER_3_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="DeepSeek V3 236B MoE Nvidia",
        size_billions=236.0,
        description="DeepSeek V3 236B MoE; near-SOTA open model for reasoning and code.",
        max_tokens=164000,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="nvidia",
        api_model_id="deepseek/deepseek-v3"
    ),
    UnifiedModel(
        name="Qwen3 235B A22B Instruct Cerebras",
        size_billions=235.0,
        description="Qwen 3 235B A22B Instruct; massive MoE multilingual/coding.",
        max_tokens=131072,
        supports_json=True,
        working=False,
        include_in_sidebar=False,
        provider="cerebras",
        api_model_id="qwen-3-235b-a22b-instruct-2507"
    ),

]
