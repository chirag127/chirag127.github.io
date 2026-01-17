"""
Multiverse Tool Generator Module

Generates alternative versions of tool websites using different AI models.
Used by generate_projects.py to create multiverse variants.
"""

import logging
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger('MultiverseTool')


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

    base_url = "multiverse_sites" if is_hub else "multiverse"

    return f"""
<script src="https://chirag127.github.io/universal/sidebar.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {{
  if (typeof MultiverseSidebar !== 'undefined') {{
    const MODELS = {models_array};
    MultiverseSidebar.init(MODELS, {{
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


def get_tool_multiverse_prompt(tool: dict, sidebar_models: List[dict], current_slug: str) -> str:
    """
    Generate prompt for creating a tool website with multiverse support.

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
     <script src="https://chirag127.github.io/universal/config.js" defer></script>
     <script src="https://chirag127.github.io/universal/core.js" defer></script>
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

6. MULTIVERSE SIDEBAR:
   Include this script before </body>:
{sidebar_js}

OUTPUT: Complete index.html with all HTML, CSS (in <style>), JS (in <script>).
Return ONLY the code wrapped in ```html blocks.
"""


class MultiverseToolGenerator:
    """
    Generates alternative versions of tool websites using different AI models.
    """

    def __init__(self, ai_client, sidebar_models: List[dict]):
        """
        Args:
            ai_client: UnifiedAIClient instance
            sidebar_models: List of model dicts for sidebar
        """
        self.ai = ai_client
        self.sidebar_models = sidebar_models

    def generate_variant(
        self,
        tool: dict,
        model_slug: str,
        model_size: float,
        fallback_html: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Generate a tool variant using a specific model.

        Args:
            tool: Tool dict with name, title, description, features, category
            model_slug: Slug of the model to use
            model_size: Size in billions of the target model
            fallback_html: HTML to use if generation fails

        Returns:
            Tuple of (success: bool, html_content: str)
        """
        logger.info(f"  Generating variant with model size >= {model_size}B")

        try:
            prompt = get_tool_multiverse_prompt(tool, self.sidebar_models, model_slug)

            result = self.ai.generate(
                prompt=prompt,
                max_tokens=32000,
                min_model_size=max(0, model_size - 50),
                temperature=0.7
            )

            if not result.success:
                raise Exception(f"Generation failed: {result.error}")

            content = result.content

            # Extract HTML from code blocks
            if "```html" in content:
                content = content.split("```html")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            logger.info(f"  ✅ Generated {len(content)} bytes using {result.model_used}")
            return True, content

        except Exception as e:
            logger.error(f"  ❌ Generation failed: {e}")

            if fallback_html:
                logger.info("  ⚠️ Using fallback HTML")
                # Inject correct sidebar for this variant
                sidebar_js = generate_sidebar_html(
                    self.sidebar_models,
                    model_slug,
                    is_hub=False
                )
                return True, inject_sidebar_into_html(fallback_html, sidebar_js)

            return False, ""

    def generate_all_variants(
        self,
        tool: dict,
        models: List[dict],
        output_dir: Path,
        main_html: str
    ) -> Dict[str, Any]:
        """
        Generate all multiverse variants for a tool.

        Args:
            tool: Tool metadata dict
            models: List of models to generate variants for
            output_dir: Directory to save variants (e.g., .temp/multiverse)
            main_html: Main HTML content to use as fallback

        Returns:
            Dict with files to be added to git push
        """
        files = {}

        for i, model in enumerate(models[:10], 1):  # Limit to 10 variants
            logger.info(f"\n  [{i}/{min(len(models), 10)}] {model['name']}")

            success, content = self.generate_variant(
                tool=tool,
                model_slug=model['slug'],
                model_size=model['size'],
                fallback_html=main_html
            )

            if success and content:
                file_path = f"multiverse/{model['slug']}/index.html"
                files[file_path] = content
                logger.info(f"  + Added: {file_path}")

            # Rate limiting
            if i < len(models):
                time.sleep(1)

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
