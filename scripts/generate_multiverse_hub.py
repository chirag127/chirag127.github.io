#!/usr/bin/env python3
"""
Generate Multiverse Hub - Alternative Hub Homepage Generator

Creates alternative versions of the Chirag Hub homepage using different AI models.
Each version is saved directly to multiverse_sites/{slug}.html (flat files, no subfolders).

Usage:
    python generate_multiverse_hub.py              # Generate all multiverse hubs
    python generate_multiverse_hub.py --dry-run    # Show what would be generated
    python generate_multiverse_hub.py --model NAME # Generate for specific model
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Setup paths
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from src.ai.unified_client import UnifiedAIClient
from src.ai.base import CompletionResult
from src.ai.models import (
    get_sidebar_enabled_models,
    generate_model_slug,
    get_sidebar_models_for_html,
    UnifiedModel,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ParallelHub')

# Paths
PARALLEL_DIR = ROOT_DIR / "multiverse_sites"  # Keep folder name for URL compatibility
MAIN_INDEX = ROOT_DIR / "index.html"

# Hub Homepage Generation Prompt
HUB_PROMPT = """ROLE: You are the Apex Technical Authority (Jan 2026 Standards).
Expert Frontend Architect creating a premium, production-ready homepage.

TASK: Generate a COMPLETE Chirag Hub homepage that:
1. Fetches repositories from GitHub API (https://api.github.com/users/chirag127/repos)
2. Displays them as filterable, searchable tool cards
3. Has premium 2026 glassmorphism design

REQUIREMENTS:

1. DATA FETCHING:
   - Fetch repos with pagination (100 per page, up to 10 pages)
   - Filter out forks and excluded repos: ['chirag127.github.io', 'chirag127']
   - Extract: name, description, stars, has_pages, pushed_at

2. UI COMPONENTS:
   - Hero section with gradient text: "Every Tool You Need. Free. Private. Forever."
   - Stats bar: Tool count (dynamic), Stars (4k+), Trackers (0)
   - Search box with glass effect (pill shape)
   - Category filter pills: All, PDF, Image, Media, Dev, Text, Math, Finance, Health, Convert, Security, Games
   - Responsive grid of tool cards (min-width 340px)
   - Each card: category icon, title, badge, description, stars, date

3. CATEGORY DETECTION (from repo name/description/topics):
   - pdf: ['pdf', 'document', 'merge', 'split']
   - image: ['image', 'photo', 'png', 'jpg', 'crop', 'resize']
   - media: ['video', 'audio', 'mp3', 'youtube']
   - dev: ['json', 'xml', 'sql', 'html', 'code', 'api']
   - text: ['text', 'word', 'markdown', 'string']
   - math: ['math', 'calculator', 'algebra']
   - finance: ['loan', 'mortgage', 'tax', 'currency']
   - health: ['bmi', 'calorie', 'health']
   - converter: ['convert', 'unit', 'encoder']
   - security: ['password', 'hash', 'encrypt']
   - game: ['game', 'puzzle', 'sudoku']

4. DESIGN (2026 SPATIAL-GLASS):
   - Background: #030712 (very dark blue)
   - Primary: #6366f1 (indigo)
   - Glass effects: backdrop-filter: blur(20px)
   - Gradient text: linear-gradient(135deg, #6366f1, #a855f7, #ec4899)
   - Card hover: translateY(-6px), glow shadow
   - Smooth animations: fadeInUp, elastic easing

5. CRITICAL REQUIREMENTS:
   - Single index.html file (inline CSS in <style>, JS in <script>)
   - Include Universal Engine scripts in <head>:
     <script src="https://chirag127.github.io/universal/config.js" defer></script>
     <script src="https://chirag127.github.io/universal/core.js" defer></script>
     <script src="https://chirag127.github.io/universal/sidebar.js" defer></script>
   - NO <header> or <footer> tags (Universal Engine injects them)
   - Wrap content in <main> element
   - Use IIFE pattern for JavaScript (no global variables)

6. MULTIVERSE SIDEBAR:
   Include JavaScript at the end to initialize the sidebar with these models:
   {sidebar_models}

   Call: MultiverseSidebar.init(MODELS_ARRAY, {{ isHub: true, baseUrl: 'multiverse_sites', currentSlug: '{current_slug}' }});

OUTPUT: Complete index.html. Return ONLY the code wrapped in ```html blocks.
"""


def get_sidebar_html_data() -> str:
    """Get sidebar models formatted as JavaScript array."""
    models = get_sidebar_models_for_html()
    items = []
    for m in models:
        items.append(
            f'{{ name: "{m["name"]}", slug: "{m["slug"]}", '
            f'size: {m["size"]}, provider: "{m["provider"]}" }}'
        )
    return "[\n        " + ",\n        ".join(items) + "\n      ]"


def call_specific_model(
    ai: UnifiedAIClient,
    model: UnifiedModel,
    prompt: str,
    max_tokens: int = 32000,
    temperature: float = 0.7,
) -> CompletionResult:
    """
    Force the AI client to call a SPECIFIC model (not fallback to others).

    This bypasses the normal fallback chain and calls the exact model specified.
    """
    logger.info(f"  🎯 Forcing model: {model.name} ({model.size_billions}B) via {model.provider}")

    # Directly call _call_model to force this specific model
    return ai._call_model(
        model=model,
        prompt=prompt,
        system_prompt="",
        max_tokens=max_tokens,
        temperature=temperature,
        json_mode=False,
    )


def generate_hub_for_model(
    model: UnifiedModel,
    ai: UnifiedAIClient,
    sidebar_data: str,
    fallback_html: Optional[str] = None,
    dry_run: bool = False
) -> tuple[bool, str]:
    """
    Generate hub homepage using a SPECIFIC model.

    Returns (success, html_content).
    If the model fails, uses fallback_html (from largest model) if available.
    """
    slug = generate_model_slug(model)
    output_file = PARALLEL_DIR / f"{slug}.html"  # Flat file, no subfolder

    logger.info(f"\n{'='*60}")
    logger.info(f"Model: {model.name} ({model.size_billions}B)")
    logger.info(f"Slug: {slug}")
    logger.info(f"Output: {output_file}")
    logger.info(f"{'='*60}")

    if dry_run:
        logger.info("DRY RUN - skipping generation")
        return True, ""

    # Create prompt with sidebar data
    prompt = HUB_PROMPT.format(
        sidebar_models=sidebar_data,
        current_slug=slug
    )

    try:
        # Force this SPECIFIC model (no fallback to others)
        logger.info(f"Generating with {model.name}...")
        start_time = time.time()

        result = call_specific_model(ai, model, prompt)

        elapsed = time.time() - start_time

        if not result.success:
            raise Exception(f"Generation failed: {result.error}")

        content = result.content

        # Extract HTML from markdown code blocks if present
        if "```html" in content:
            content = content.split("```html")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        # Validate it looks like HTML
        if not content.strip().startswith("<!DOCTYPE") and not content.strip().startswith("<html"):
            logger.warning("Generated content doesn't look like HTML, may need adjustment")

        # Save to file
        output_file.write_text(content, encoding="utf-8")

        logger.info(f"✅ Generated {len(content)} bytes in {elapsed:.1f}s using {result.model_used}")
        return True, content

    except Exception as e:
        logger.error(f"❌ Generation failed for {model.name}: {e}")

        # Fallback: copy the main index.html (already generated separately)
        if MAIN_INDEX.exists():
            logger.info("⚠️ Using fallback: copying main index.html")
            fallback_content = MAIN_INDEX.read_text(encoding="utf-8")
            output_file.write_text(fallback_content, encoding="utf-8")
            return True, fallback_content

        return False, ""


def generate_all_hubs(
    models: Optional[List[str]] = None,
    dry_run: bool = False
) -> dict:
    """
    Generate hub homepages for all sidebar-enabled models.

    Each model generates its own content.
    On failure, falls back to main index.html.
    """
    logger.info("=" * 60)
    logger.info("PARALLEL HUB GENERATOR")
    logger.info("=" * 60)

    # Get sidebar-enabled models (sorted largest first)
    all_models = get_sidebar_enabled_models()
    logger.info(f"Found {len(all_models)} sidebar-enabled models")

    # Filter if specific models requested
    if models:
        all_models = [m for m in all_models if m.name in models or generate_model_slug(m) in models]
        logger.info(f"Filtered to {len(all_models)} requested models")

    if not all_models:
        logger.error("No models to process")
        return {"success": 0, "failed": 0}

    # Ensure parallel directory exists
    PARALLEL_DIR.mkdir(parents=True, exist_ok=True)

    # Initialize AI client
    if not dry_run:
        ai = UnifiedAIClient()
    else:
        ai = None

    # Get sidebar data (same for all)
    sidebar_data = get_sidebar_html_data()

    # Generate for each model
    results = {"success": 0, "failed": 0, "models": []}

    for i, model in enumerate(all_models, 1):
        logger.info(f"\n[{i}/{len(all_models)}] Processing {model.name}...")

        success, content = generate_hub_for_model(
            model=model,
            ai=ai,
            sidebar_data=sidebar_data,
            dry_run=dry_run
        )

        # Store first model's content as fallback for others
        if i == 1 and content:
            largest_model_content = content
            logger.info("  📦 Stored as fallback content for failed models")

        if success:
            results["success"] += 1
            results["models"].append({"name": model.name, "status": "success"})
        else:
            results["failed"] += 1
            results["models"].append({"name": model.name, "status": "failed"})

        # Rate limiting between generations
        if not dry_run and i < len(all_models):
            time.sleep(2)

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("GENERATION COMPLETE")
    logger.info(f"Success: {results['success']}")
    logger.info(f"Failed: {results['failed']}")
    logger.info("=" * 60)

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate Multiverse Hub homepages")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without generating")
    parser.add_argument("--model", type=str, help="Generate for specific model name or slug")
    parser.add_argument("--list-models", action="store_true", help="List all sidebar-enabled models")

    args = parser.parse_args()

    if args.list_models:
        models = get_sidebar_enabled_models()
        print(f"\nSidebar-enabled models ({len(models)}):\n")
        for m in models:
            slug = generate_model_slug(m)
            print(f"  {m.name}")
            print(f"    Size: {m.size_billions}B | Provider: {m.provider}")
            print(f"    Slug: {slug}")
            print()
        return

    # Generate
    models_to_generate = [args.model] if args.model else None
    results = generate_all_hubs(
        models=models_to_generate,
        dry_run=args.dry_run
    )

    # Exit code based on results
    if results["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
