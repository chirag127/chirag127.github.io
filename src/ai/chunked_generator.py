"""
Chunked Code Generator - Split HTML/CSS/JS Generation for Timeout Prevention.

Generates website code in separate chunks to avoid timeouts with large AI models.
Each component (HTML structure, CSS styles, JavaScript) is generated separately
with smaller token limits, then combined into a single file.

Key Features:
- Generates HTML structure first (8K tokens)
- Uses HTML context to generate CSS (8K tokens)
- Uses HTML context to generate JavaScript (8K tokens)
- Combines all chunks into a single HTML file
- Falls back to single-call generation if chunked fails
"""

import logging
import re
import time
from typing import TYPE_CHECKING

from src.core.config import Settings

if TYPE_CHECKING:
    from .unified_client import UnifiedAIClient

logger = logging.getLogger("AI.ChunkedGenerator")

# Central hub URL for prompt templates
CENTRAL_HUB = Settings.SITE_BASE_URL


# =============================================================================
# CHUNK-SPECIFIC PROMPTS
# =============================================================================

HTML_STRUCTURE_PROMPT = """
TASK: Generate the HTML STRUCTURE ONLY for: "{tool_name}"
Description: {description}
Features: {features}

REQUIREMENTS:
1. OUTPUT: HTML structure with semantic elements (<main>, <section>, <div>, etc.)
2. NO INLINE CSS - Use class names for styling (will be styled separately)
3. NO INLINE JS - Use id attributes for DOM interaction (will be scripted separately)
4. UNIVERSAL ARCHITECTURE (CRITICAL):
   - MUST include in <head>: <script src="{CENTRAL_HUB}/universal/config.js"></script>
   - MUST include in <head>: <script src="{CENTRAL_HUB}/universal/core.js"></script>
   - DO NOT generate <header> or <footer> tags (The Universal Engine injects them)
   - ALL content must be wrapped in <main> tag
5. Use meaningful class names (e.g., .tool-container, .input-section, .result-display)
6. Use meaningful IDs for interactive elements (e.g., #file-input, #process-btn, #output)

FORMAT: Return ONLY the HTML code block within ```html flags.
Return ONLY HTML structure - CSS and JS will be generated separately.
"""

CSS_STYLES_PROMPT = """
TASK: Generate CSS STYLES ONLY for the following HTML structure.
Tool: "{tool_name}"

HTML STRUCTURE TO STYLE:
```html
{html_preview}
```

REQUIREMENTS:
1. OUTPUT: CSS code inside <style> tags
2. AESTHETICS: **Apex 2026 Spatial-Adaptive** design
   - "Spatial Glass" look (backdrop-filter: blur(20px), rgba backgrounds)
   - "Bento Grid" layouts with modern spacing
   - Vibrant gradient accents
   - Smooth transitions (0.3s ease)
3. RESPONSIVE: Mobile-first, works on all screen sizes
4. DARK MODE: Use CSS variables for theming
5. Target all classes mentioned in the HTML structure above

FORMAT: Return ONLY the CSS code inside <style> tags.
Example:
```css
<style>
:root {{
  --primary: #...;
  ...
}}
...
</style>
```
"""

JAVASCRIPT_PROMPT = """
TASK: Generate JAVASCRIPT LOGIC ONLY for the following HTML structure.
Tool: "{tool_name}"
Description: {description}
Features: {features}

HTML STRUCTURE TO SCRIPT:
```html
{html_preview}
```

REQUIREMENTS:
1. OUTPUT: JavaScript code inside <script> tags at end of body
2. USE IIFE: Wrap all code in (function() {{ ... }})();
3. TARGET ELEMENTS: Use the IDs and classes from the HTML above
4. ERROR HANDLING: Robust try-catch blocks, user-friendly error messages
5. LIBRARIES: Load any needed CDN libraries (use cdnjs/unpkg)
6. CONFIGURATION: Use `window.SITE_CONFIG` for any external service keys
7. NO REDUNDANT DOM CREATION: Only script the existing HTML elements

FORMAT: Return ONLY the JavaScript code inside <script> tags.
Example:
```javascript
<script>
(function() {{
  // Your code here
}})();
</script>
```
"""


class ChunkedCodeGenerator:
    """
    Generate website code in separate chunks to avoid timeouts.

    Uses a 3-step approach:
    1. Generate HTML structure (smaller token limit)
    2. Generate CSS based on HTML context
    3. Generate JavaScript based on HTML context
    4. Combine all into single HTML file
    """

    def __init__(self, ai_client: "UnifiedAIClient") -> None:
        self.ai = ai_client
        self.chunk_max_tokens = 8000  # Smaller chunks = faster generation
        self.min_model_size = 32  # Use 32B+ models for quality

    def generate_html_structure(self, tool: dict, system_prompt: str = "") -> str:
        """Generate HTML structure without inline CSS/JS."""
        logger.info(f"  📄 Generating HTML structure for {tool['name']}...")

        prompt = HTML_STRUCTURE_PROMPT.format(
            tool_name=tool.get('title', tool['name']),
            description=tool.get('description', ''),
            features=', '.join(tool.get('features', []))
        )

        result = self.ai.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=self.chunk_max_tokens,
            min_model_size=self.min_model_size,
            temperature=0.7
        )

        if not result.success:
            logger.error(f"HTML generation failed: {result.error}")
            return ""

        html = self._extract_code(result.content, "html")
        logger.info(f"  ✅ HTML generated: {len(html)} bytes")
        return html

    def generate_css_styles(self, tool: dict, html_structure: str, system_prompt: str = "") -> str:
        """Generate CSS styles based on HTML structure."""
        logger.info(f"  🎨 Generating CSS styles for {tool['name']}...")

        # Truncate HTML preview if too long
        html_preview = html_structure[:4000] if len(html_structure) > 4000 else html_structure

        prompt = CSS_STYLES_PROMPT.format(
            tool_name=tool.get('title', tool['name']),
            html_preview=html_preview
        )

        result = self.ai.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=self.chunk_max_tokens,
            min_model_size=self.min_model_size,
            temperature=0.6
        )

        if not result.success:
            logger.error(f"CSS generation failed: {result.error}")
            return self._get_fallback_css()

        css = self._extract_code(result.content, "css")

        # Ensure it's wrapped in style tags
        if css and not css.strip().startswith("<style"):
            css = f"<style>\n{css}\n</style>"

        logger.info(f"  ✅ CSS generated: {len(css)} bytes")
        return css

    def generate_javascript(self, tool: dict, html_structure: str, system_prompt: str = "") -> str:
        """Generate JavaScript logic based on HTML structure."""
        logger.info(f"  ⚡ Generating JavaScript for {tool['name']}...")

        # Truncate HTML preview if too long
        html_preview = html_structure[:4000] if len(html_structure) > 4000 else html_structure

        prompt = JAVASCRIPT_PROMPT.format(
            tool_name=tool.get('title', tool['name']),
            description=tool.get('description', ''),
            features=', '.join(tool.get('features', [])),
            html_preview=html_preview
        )

        result = self.ai.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=self.chunk_max_tokens,
            min_model_size=self.min_model_size,
            temperature=0.7
        )

        if not result.success:
            logger.error(f"JavaScript generation failed: {result.error}")
            return self._get_fallback_js(tool['name'])

        js = self._extract_code(result.content, "javascript")

        # Ensure it's wrapped in script tags
        if js and not js.strip().startswith("<script"):
            js = f"<script>\n{js}\n</script>"

        logger.info(f"  ✅ JavaScript generated: {len(js)} bytes")
        return js

    def combine_chunks(self, html: str, css: str, js: str) -> str:
        """Combine HTML, CSS, and JS chunks into a single HTML file."""
        logger.info("  🔗 Combining chunks...")

        # Parse HTML and inject CSS/JS
        if "</head>" in html:
            # Inject CSS before </head>
            html = html.replace("</head>", f"{css}\n</head>")
        else:
            # No head tag, add one
            html = f"<head>\n{css}\n</head>\n" + html

        if "</body>" in html:
            # Inject JS before </body>
            html = html.replace("</body>", f"{js}\n</body>")
        elif "</html>" in html:
            # No body end tag, inject before </html>
            html = html.replace("</html>", f"{js}\n</html>")
        else:
            # No closing tags, append
            html = html + f"\n{js}"

        logger.info(f"  ✅ Combined file: {len(html)} bytes")
        return html

    def generate_full_page(self, tool: dict, system_prompt: str = "") -> str:
        """
        Orchestrate chunked generation with fallback to single-call.

        Steps:
        1. Generate HTML structure
        2. Generate CSS based on HTML
        3. Generate JavaScript based on HTML
        4. Combine all chunks

        Falls back to single-call if any step fails critically.
        """
        start_time = time.time()
        logger.info(f"🧩 Starting chunked generation for {tool['name']}")

        # Step 1: Generate HTML structure
        html = self.generate_html_structure(tool, system_prompt)
        if not html:
            logger.warning("HTML generation failed, falling back to single-call")
            return self._fallback_single_call(tool, system_prompt)

        # Step 2: Generate CSS
        css = self.generate_css_styles(tool, html, system_prompt)

        # Step 3: Generate JavaScript
        js = self.generate_javascript(tool, html, system_prompt)

        # Step 4: Combine
        combined = self.combine_chunks(html, css, js)

        elapsed = time.time() - start_time
        logger.info(f"🎉 Chunked generation completed in {elapsed:.1f}s")

        return combined

    def _extract_code(self, content: str, lang: str) -> str:
        """Extract code from markdown code blocks."""
        if not content:
            return ""

        # Try to extract from markdown code blocks
        patterns = [
            rf"```{lang}\s*([\s\S]*?)```",  # Specific language
            r"```\s*([\s\S]*?)```",          # Any code block
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # No code block found, return as-is (minus obvious prefixes)
        return content.strip()

    def _get_fallback_css(self) -> str:
        """Get minimal fallback CSS if generation fails."""
        return """<style>
:root {
  --primary: #6366f1;
  --bg: #0f172a;
  --surface: rgba(30, 41, 59, 0.8);
  --text: #f1f5f9;
}
body {
  font-family: 'Inter', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  margin: 0;
  min-height: 100vh;
}
main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
.glass {
  background: var(--surface);
  backdrop-filter: blur(20px);
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid rgba(255,255,255,0.1);
}
button {
  background: var(--primary);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: transform 0.2s;
}
button:hover { transform: scale(1.05); }
</style>"""

    def _get_fallback_js(self, tool_name: str) -> str:
        """Get minimal fallback JavaScript if generation fails."""
        return f"""<script>
(function() {{
  console.log('{tool_name} loaded');
  // Basic initialization
  document.addEventListener('DOMContentLoaded', function() {{
    console.log('DOM ready');
  }});
}})();
</script>"""

    def _fallback_single_call(self, tool: dict, system_prompt: str) -> str:
        """Fall back to single-call generation if chunked fails."""
        logger.warning("Falling back to single-call generation...")

        prompt = f"""
TASK: GENERATE THE COMPLETE SOURCE CODE FOR: "{tool.get('title', tool['name'])}"
DESCRIPTION: {tool.get('description', '')}
Features: {', '.join(tool.get('features', []))}

REQUIREMENTS:
1. OUTPUT: A SINGLE `index.html` file containing ALL HTML, CSS, and JavaScript.
2. UNIVERSAL ARCHITECTURE (CRITICAL):
   - MUST include in <head>: <script src="{CENTRAL_HUB}/universal/config.js"></script>
   - MUST include in <head>: <script src="{CENTRAL_HUB}/universal/core.js"></script>
   - DO NOT generate <header> or <footer> tags (The Universal Engine injects them).
   - ALL content must be wrapped in <main> tag.
3. AESTHETICS: **Apex 2026 Spatial-Adaptive** design.
4. LOGIC: Robust, error-handled JavaScript (IIFE).
5. FORMAT: Return ONLY the HTML code block within ```html flags.
"""

        result = self.ai.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            max_tokens=16000,
            min_model_size=32,
            temperature=0.7
        )

        if not result.success:
            logger.error(f"Fallback generation failed: {result.error}")
            return f"<h1>Generation Failed</h1><p>{result.error}</p>"

        return self._extract_code(result.content, "html")
