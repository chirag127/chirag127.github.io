from .schema import UnifiedModel

TIER_5_MODELS: list[UnifiedModel] = [
    UnifiedModel(
        name="Llama 3.2 90B Vision Instruct Groq",
        size_billions=90.0,
        description="Llama 3.2 90B Vision - Multimodal Code",
        max_tokens=8192,
        working=True,
        include_in_sidebar=True,
        provider="groq",
        api_model_id="llama-3.2-90b-vision-preview"
    ),
    UnifiedModel(
        name="Llama 3.2 90B Vision Instruct OpenRouter",
        size_billions=90.0,
        description="Llama 3.2 90B Vision - Multimodal Code",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="meta-llama/llama-3.2-90b-vision-instruct:free"
    ),
    UnifiedModel(
        name="Qwen 2.5 72B Instruct Nvidia",
        size_billions=72.0,
        description="Qwen 2.5 72B - Strong Multilingual",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="nvidia",
        api_model_id="qwen/qwen2.5-72b-instruct"
    ),
    UnifiedModel(
        name="Qwen 2.5 72B Instruct OpenRouter",
        size_billions=72.0,
        description="Qwen 2.5 72B - Strong Multilingual",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="qwen/qwen2.5-72b-instruct:free"
    ),
    UnifiedModel(
        name="Llama 3.3 70B Instruct Groq",
        size_billions=70.0,
        description="Meta Llama 3.3 70B - Very Strong General",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="groq",
        api_model_id="llama-3.3-70b-versatile"
    ),
    UnifiedModel(
        name="Llama 3.3 70B Instruct Cerebras",
        size_billions=70.0,
        description="Meta Llama 3.3 70B - Very Strong General",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="cerebras",
        api_model_id="llama-3.3-70b"
    ),
    UnifiedModel(
        name="Llama 3.3 70B Instruct Nvidia",
        size_billions=70.0,
        description="Meta Llama 3.3 70B - Very Strong General",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="nvidia",
        api_model_id="meta/llama-3.3-70b-instruct"
    ),
    UnifiedModel(
        name="Llama 3.3 70B Instruct Cloudflare",
        size_billions=70.0,
        description="Meta Llama 3.3 70B - Very Strong General",
        max_tokens=8192,
        working=False,
        include_in_sidebar=False,
        provider="cloudflare",
        api_model_id="@cf/meta/llama-3.3-70b-instruct-fp8"
    ),
    UnifiedModel(
        name="Llama 3.3 70B Instruct OpenRouter",
        size_billions=70.0,
        description="Meta Llama 3.3 70B - Very Strong General",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="meta-llama/llama-3.3-70b-instruct:free"
    ),
    UnifiedModel(
        name="Llama 3.3 70B Instruct GitHub",
        size_billions=70.0,
        description="Meta Llama 3.3 70B - Very Strong General",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="github",
        api_model_id="Meta-Llama-3.3-70B-Instruct"
    ),
    UnifiedModel(
        name="DeepSeek R1 Distill Llama 70B Groq",
        size_billions=70.0,
        description="DeepSeek R1 Distill 70B - Reasoning",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="groq",
        api_model_id="deepseek-r1-distill-llama-70b"
    ),
    UnifiedModel(
        name="DeepSeek R1 Distill Llama 70B Nvidia",
        size_billions=70.0,
        description="DeepSeek R1 Distill 70B - Reasoning",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="nvidia",
        api_model_id="deepseek-ai/deepseek-r1-distill-llama-70b"
    ),
    UnifiedModel(
        name="DeepSeek R1 Distill Llama 70B OpenRouter",
        size_billions=70.0,
        description="DeepSeek R1 Distill 70B - Reasoning",
        max_tokens=32768,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="deepseek/deepseek-r1-distill-llama-70b:free"
    ),
    UnifiedModel(
        name="Llama 3.1 70B Instruct Nvidia",
        size_billions=70.0,
        description="Meta Llama 3.1 70B - Strong Reasoning",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="nvidia",
        api_model_id="meta/llama-3.1-70b-instruct"
    ),
    UnifiedModel(
        name="Llama 3.1 70B Instruct Cloudflare",
        size_billions=70.0,
        description="Meta Llama 3.1 70B - Strong Reasoning",
        max_tokens=8192,
        working=False,
        include_in_sidebar=False,
        provider="cloudflare",
        api_model_id="@cf/meta/llama-3.1-70b-instruct"
    ),
    UnifiedModel(
        name="Llama 3.1 70B Instruct OpenRouter",
        size_billions=70.0,
        description="Meta Llama 3.1 70B - Strong Reasoning",
        max_tokens=8192,
        working=True,
        include_in_sidebar=False,
        provider="openrouter",
        api_model_id="meta-llama/llama-3.1-70b-instruct:free"
    ),
]
