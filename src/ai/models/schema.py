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
    providers: list[tuple[str, str]] = field(default_factory=list)

    @property
    def timeout_seconds(self) -> int:
        """Calculate timeout based on model size."""
        if self.size_billions >= 400:
            return 900
        elif self.size_billions >= 200:
            return 600
        elif self.size_billions >= 70:
            return 300
        elif self.size_billions >= 30:
            return 180
        else:
            return 90

    @property
    def primary_provider(self) -> str:
        return self.providers[0][0] if self.providers else "unknown"

    @property
    def primary_model_id(self) -> str:
        return self.providers[0][1] if self.providers else self.name
