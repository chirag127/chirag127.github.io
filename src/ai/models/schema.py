from dataclasses import dataclass, field

@dataclass
class UnifiedModel:
    """A model with multiple provider options, ordered by speed."""
    name: str
    size_billions: float
    description: str = ""
    max_tokens: int = 8192
    supports_json: bool = True
    priority: int = 0  # Higher priority (e.g., 100) models are tried first
    working: bool = True  # Whether the model is currently verified to be working
    include_in_sidebar: bool = True  # Whether to show this model in the Multiverse sidebar
    provider: str = ""
    api_model_id: str = ""
