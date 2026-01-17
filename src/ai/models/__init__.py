from .schema import UnifiedModel

# Import tiered models
from .tier_1_400b_plus import TIER_1_MODELS
from .tier_2_300b_400b import TIER_2_MODELS
from .tier_3_200b_300b import TIER_3_MODELS
from .tier_4_100b_200b import TIER_4_MODELS
from .tier_5_70b_100b import TIER_5_MODELS
from .tier_6_20b_70b import TIER_6_MODELS

# Combine all tiers into the unified chain
UNIFIED_MODEL_CHAIN: list[UnifiedModel] = (
    TIER_1_MODELS +
    TIER_2_MODELS +
    TIER_3_MODELS +
    TIER_4_MODELS +
    TIER_5_MODELS +
    TIER_6_MODELS
)

MODEL_COUNT = len(UNIFIED_MODEL_CHAIN)
