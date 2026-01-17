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
    include_in_sidebar: bool = True  # Whether to show this model in the Polymorphs sidebar
    provider: str = ""
    api_model_id: str = ""

    @property
    def timeout_seconds(self) -> int:
        """Calculate timeout based on model size (New Tier Planning)."""
        if self.size_billions >= 400:
            return 1200  # Tier 1 (20 mins)
        elif self.size_billions >= 200:
            return 900   # Tier 2 & 3 (15 mins)
        elif self.size_billions >= 100:
            return 600   # Tier 4 (10 mins)
        elif self.size_billions >= 70:
            return 300   # Tier 5 (5 mins)
        elif self.size_billions >= 30:
            return 180   # Tier 6 (Top half)
        else:
            return 90    # Tier 6 (Bottom half)
