"""
AI Helpers - Model Utilities for Polymorphs Generation

Functions for working with the unified model chain:
- Get sidebar-enabled models
- Generate URL-safe model slugs
- Get fallback models
"""

import re
from typing import List

from .schema import UnifiedModel
from .tier_1_400b_plus import TIER_1_MODELS
from .tier_2_300b_400b import TIER_2_MODELS
from .tier_3_200b_300b import TIER_3_MODELS
from .tier_4_100b_200b import TIER_4_MODELS
from .tier_5_70b_100b import TIER_5_MODELS
from .tier_6_20b_70b import TIER_6_MODELS

# Build the chain locally to avoid circular import
_ALL_MODELS = (
    TIER_1_MODELS +
    TIER_2_MODELS +
    TIER_3_MODELS +
    TIER_4_MODELS +
    TIER_5_MODELS +
    TIER_6_MODELS
)


def get_sidebar_enabled_models() -> List[UnifiedModel]:
    """
    Get all models with include_in_sidebar=True.

    Returns models sorted by size (largest first) for sidebar display.
    """
    sidebar_models = [
        model for model in _ALL_MODELS
        if model.include_in_sidebar and model.working
    ]
    # Sort by size descending
    return sorted(sidebar_models, key=lambda m: m.size_billions, reverse=True)


def generate_model_slug(model: UnifiedModel) -> str:
    """
    Generate a URL-safe slug for a model.

    Format: {model-name-cleaned}--{provider}
    Example: "deepseek-v3-671b--nvidia"

    Args:
        model: UnifiedModel instance

    Returns:
        URL-safe slug string
    """
    # Clean the model name (already includes provider info)
    name = model.name.lower()
    # Remove special characters, keep alphanumeric and spaces
    name = re.sub(r'[^a-z0-9\s\-.]', '', name)
    # Replace spaces and dots with hyphens
    name = re.sub(r'[\s.]+', '-', name)
    # Remove consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')

    # No need to append provider - model names already include it
    return name


def get_largest_model() -> UnifiedModel:
    """
    Get the largest working model from the chain.

    Used as fallback when specific model generation fails.
    """
    working_models = [m for m in _ALL_MODELS if m.working]
    if not working_models:
        raise RuntimeError("No working models available")
    return max(working_models, key=lambda m: m.size_billions)


def get_model_by_slug(slug: str) -> UnifiedModel | None:
    """
    Find a model by its slug.

    Args:
        slug: Model slug (e.g., "deepseek-v3-671b--nvidia")

    Returns:
        UnifiedModel if found, None otherwise
    """
    for model in _ALL_MODELS:
        if generate_model_slug(model) == slug:
            return model
    return None


def get_sidebar_models_for_html() -> List[dict]:
    """
    Get sidebar models formatted for HTML template generation.

    Returns list of dicts with:
    - name: Display name
    - slug: URL slug
    - size: Size in billions
    - provider: Provider name (capitalized)
    """
    models = get_sidebar_enabled_models()
    return [
        {
            "name": model.name,
            "slug": generate_model_slug(model),
            "size": model.size_billions,
            "provider": model.provider.capitalize(),
        }
        for model in models
    ]
