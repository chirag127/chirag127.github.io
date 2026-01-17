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

# Export helper functions
from .helpers import (
    get_sidebar_enabled_models,
    generate_model_slug,
    get_largest_model,
    get_model_by_slug,
    get_sidebar_models_for_html,
)
