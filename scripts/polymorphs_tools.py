"""
Polymorphs Tool Generator Module

Generates alternative versions of tool websites using different AI models.
Used by generate_projects.py to create polymorphs variants.

Key Features:
- Forces specific models (no fallback to larger models during generation)
- Flat file structure: polymorphs/{slug}.html
- Uses main HTML as fallback on failure
"""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict, Any, Optional

import sys
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from src.core.config import Settings

logger = logging.getLogger('PolymorphsTool')


def generate_sidebar_html(models: List[dict], current_slug: str, is_hub: bool = False) -> str:
    """
    Generate the sidebar JavaScript initialization code.

    Args:
        models: List of model dicts with name, slug, size, provider
        current_slug: Current model's slug (to mark as active)
        is_hub: Whether this is for hub (True) or tool (False)

    Returns:
        JavaScript code to initialize sidebar
    """
    items = []
    for m in models:
        items.append(
            f'{{ name: "{m["name"]}", slug: "{m["slug"]}", '
            f'size: {m["size"]}, provider: "{m["provider"]}" }}'
        )

    models_array = "[\n        " + ",\n        ".join(items) + "\n      ]"

    # Flat file structure
    base_url = "polymorphs"

    return f"""
<script src="/universal/sidebar.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {{
  if (typeof Polymorphs !== 'undefined') {{
    const MODELS = {models_array};
    Polymorphs.init(MODELS, {{
      isHub: {str(is_hub).lower()},
      baseUrl: '{base_url}',
      currentSlug: '{current_slug}'
    }});
  }}
}});
</script>
"""


def inject_sidebar_into_html(html_content: str, sidebar_script: str) -> str:
    """
    Inject sidebar script into HTML content.

    Adds the sidebar script just before </body>.
    """
    if "</body>" in html_content:
        return html_content.replace("</body>", f"{sidebar_script}\n</body>")
    else:
        # Fallback: append to end
        return html_content + sidebar_script


def get_tool_polymorphs_prompt(tool: dict, sidebar_models: List[dict], current_slug: str) -> str:
    """
    Generate prompt for creating a tool website with polymorphs support.

    This is the prompt used for generating alternative versions of tools.
    """
    sidebar_js = generate_sidebar_html(sidebar_models, current_slug, is_hub=False)

    return f"""ROLE: You are the Apex Technical Authority (Jan 2026 Standards).
Expert Frontend Architect creating production-ready web tools.

TASK: Generate a COMPLETE, SINGLE-FILE tool website for: "{tool.get('title', tool['name'])}"

METADATA:
- Name: {tool['name']}
- Description: {tool.get('description', 'A privacy-focused browser tool.')}
- Features: {', '.join(tool.get('features', ['Fast', 'Free', 'Secure']))}
- Category: {tool.get('category', 'utility')}

REQUIREMENTS:

1. ARCHITECTURE (FRONTEND-ONLY):
   - ALL processing happens client-side in the browser
   - NO fetch() to external APIs for data processing
   - Use approved libraries via CDN (pdf-lib, ffmpeg.wasm, etc.)

2. UNIVERSAL ENGINE INTEGRATION:
   - Include in <head>:
     <script src="/universal/config.js" defer></script>
     <script src="/universal/core.js" defer></script>
   - DO NOT create <header> or <footer> tags (injected by Universal Engine)
   - Wrap ALL content in <main> with padding-top: 80px

3. UI COMPONENTS:
   - <input type="file" id="fileInput"> (hidden file input)
   - <label id="dropZone"> (drag-drop area, styled glass effect)
   - <button id="actionBtn"> (main CTA, disabled by default)
   - <div id="statusArea"> (progress bars, file list)
   - <div id="resultsContent"> (output/download area)

4. JAVASCRIPT QUALITY (ZERO RUNTIME ERRORS):
   - Validate all inputs before calling array methods
   - Check element existence: if (element) {{ ... }}
   - Wrap async operations in try-catch
   - Show user-friendly error messages in UI
   - Use IIFE pattern, no global variables
   - Clean up blob URLs with URL.revokeObjectURL()

5. DESIGN (2026 SPATIAL-GLASS):
   - Background: #030712 (dark)
   - Primary: #6366f1 (indigo)
   - Glass effects: backdrop-filter: blur(20px)
   - Border: 1px solid rgba(255,255,255,0.08)
   - Card hover: translateY(-4px), glow shadow
   - Smooth transitions: 0.3s cubic-bezier(0.4, 0, 0.2, 1)
   - Progress bars with gradient

6. POLYMORPHS SIDEBAR:
   Include this script before </body>:
{sidebar_js}

OUTPUT: Complete index.html with all HTML, CSS (in <style>), JS (in <script>).
Return ONLY the code wrapped in ```html blocks.
"""


class PolymorphsToolGenerator:
    """
    Generates alternative versions of tool websites using different AI models.

    Key features:
    - Forces specific models (calls _call_model directly)
    - Uses flat file structure (polymorphs/{slug}.html)
    - Falls back to main HTML on failure
    """

    def __init__(self, ai_client, sidebar_models: List[dict]):
        """
        Args:
            ai_client: UnifiedAIClient instance
            sidebar_models: List of model dicts for sidebar
        """
        self.ai = ai_client
        self.sidebar_models = sidebar_models

    def _call_specific_model(self, model, prompt: str, max_tokens: int = 32000):
        """Force the AI client to call a SPECIFIC model."""
        from src.ai.base import CompletionResult

        logger.info(f"    🎯 Forcing model: {model.name} ({model.size_billions}B)")

        return self.ai._call_model(
            model=model,
            prompt=prompt,
            system_prompt="",
            max_tokens=max_tokens,
            temperature=0.7,
            json_mode=False,
        )

    def generate_variant(
        self,
        tool: dict,
        model,
        fallback_html: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Generate a tool variant using a SPECIFIC model.

        Args:
            tool: Tool dict with name, title, description, features, category
            model: UnifiedModel to use (forced, no fallback to others)
            fallback_html: HTML to use if this model fails

        Returns:
            Tuple of (success: bool, html_content: str)
        """
        from src.ai.models import generate_model_slug

        slug = generate_model_slug(model)
        logger.info(f"    Generating variant: {model.name}")

        try:
            prompt = get_tool_polymorphs_prompt(tool, self.sidebar_models, slug)

            result = self._call_specific_model(model, prompt)

            if not result.success:
                raise Exception(f"Generation failed: {result.error}")

            content = result.content

            # Extract HTML from code blocks
            if "```html" in content:
                content = content.split("```html")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Ensure sidebar is included (inject if missing)
            if "Polymorphs.init" not in content:
                logger.info("    ⚠️ Sidebar missing, injecting...")
                sidebar_js = generate_sidebar_html(self.sidebar_models, slug, is_hub=False)
                content = inject_sidebar_into_html(content, sidebar_js)
            else:
                logger.info("    ✓ Sidebar already included")

            logger.info(f"    ✅ Generated {len(content)} bytes using {result.model_used}")
            return True, content

        except Exception as e:
            logger.error(f"    ❌ Generation failed: {e}")

            if fallback_html:
                logger.info("    ⚠️ Using fallback HTML")
                # Inject correct sidebar for this variant
                sidebar_js = generate_sidebar_html(
                    self.sidebar_models,
                    slug,
                    is_hub=False
                )
                return True, inject_sidebar_into_html(fallback_html, sidebar_js)

            return False, ""

    def generate_all_variants(
        self,
        tool: dict,
        models: List,
        output_dir: Path,
        main_html: str,
        max_workers: int = 5,
    ) -> Dict[str, Any]:
        """
        Generate all polymorphs variants for a tool CONCURRENTLY.

        Uses ThreadPoolExecutor to parallelize variant generation.

        Args:
            tool: Tool metadata dict
            models: List of UnifiedModel objects to generate variants for
            output_dir: Directory to save variants (e.g., .temp/polymorphs)
            main_html: Main HTML content (used as fallback)
            max_workers: Maximum concurrent AI calls (default: 5)

        Returns:
            Dict with files to be added to git push (flat structure)
        """
        from src.ai.models import generate_model_slug

        files = {}
        models_to_process = models[:10]  # Limit to 10 variants
        total = len(models_to_process)
        start_time = time.time()

        logger.info(f"\n  🔮 Generating {total} variants concurrently (workers: {max_workers})...")

        def process_variant(model_with_index):
            """Worker function to generate a single variant."""
            idx, model = model_with_index
            slug = generate_model_slug(model)
            logger.info(f"  [{idx}/{total}] Starting {model.name}...")

            try:
                success, content = self.generate_variant(
                    tool=tool,
                    model=model,
                    fallback_html=main_html
                )
                return slug, success, content, model.name
            except Exception as e:
                logger.error(f"  [{idx}] Error generating {model.name}: {e}")
                return slug, False, "", model.name

        # Use ThreadPoolExecutor for concurrent generation
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(process_variant, (i, model)): model
                for i, model in enumerate(models_to_process, 1)
            }

            for future in as_completed(futures):
                slug, success, content, name = future.result()
                if success and content:
                    file_path = f"polymorphs/{slug}.html"
                    files[file_path] = content
                    logger.info(f"    ✅ Added: {file_path}")
                else:
                    logger.warning(f"    ⚠️ Failed: {name}")

        elapsed = time.time() - start_time
        logger.info(f"  ⏱️ Generated {len(files)} variants in {elapsed:.1f}s")

        return files


def get_sidebar_models_from_chain() -> List[dict]:
    """
    Get sidebar models from the model chain.

    Returns list of dicts with name, slug, size, provider.
    """
    # Import here to avoid circular imports
    import sys
    from pathlib import Path

    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent
    sys.path.insert(0, str(root_dir))

    from src.ai.models import get_sidebar_models_for_html
    return get_sidebar_models_for_html()
