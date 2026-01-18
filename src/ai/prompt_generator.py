"""
Prompt Generator - Creates prompts for AI code generation.

Simplified for tool website generation:
- Frontend-only architecture
- Central hub integration
- No CI/CD overhead
- Pure HTML/CSS/JS or React+Vite
"""

import logging

from src.core.config import Settings

logger = logging.getLogger("PromptGenerator")


class PromptGenerator:
    """
    Generates prompts for AI-powered tool generation.
    Aligned with central hub architecture.
    """

    CENTRAL_HUB = Settings.SITE_BASE_URL

    def __init__(self, agents_md_content: str = "") -> None:
        self.agents_md = agents_md_content

    def generate_tool_prompt(
        self,
        name: str,
        title: str,
        description: str,
        features: list[str],
        keywords: list[str],
    ) -> str:
        """
        Generate prompt for creating a tool website.

        Output: Pure HTML/CSS/JavaScript (no build step).
        """
        url = f"{self.CENTRAL_HUB}/{name}/"

        return f"""
Create a COMPLETE, PRODUCTION-READY web tool.

TOOL: {title}
DESCRIPTION: {description}
FEATURES: {', '.join(features)}
KEYWORDS: {', '.join(keywords)}
URL: {url}

## REQUIREMENTS

### 1. FRONTEND-ONLY (MANDATORY)
- All processing in browser (client-side)
- No backend servers, no APIs to build
- Static hosting (GitHub Pages)
- User files never leave device

### 2. TECH STACK
- Pure HTML5, CSS3, JavaScript ES6+
- No React, no build step
- Modern CSS (flexbox, grid, variables)
- Responsive design

### 3. CENTRAL HUB INTEGRATION
Include these scripts in every page:
```html
<script src="{self.CENTRAL_HUB}/shared/analytics.js" defer></script>
<script src="{self.CENTRAL_HUB}/shared/monetization.js" defer></script>
```

### 4. SEO OPTIMIZATION
- Meta description and keywords
- Open Graph tags
- Structured data (schema.org)
- Canonical URL: {url}

### 5. UI/UX
- Dark theme (#0f172a background)
- Glassmorphism cards
- Gradient accents (blue to purple)
- Drag-drop file handling
- Progress indicators
- Download functionality

### 6. FILES TO GENERATE

**index.html** - Complete working tool with:
- Hero section with title and description
- Tool interface (file input, options, buttons)
- Features section
- Privacy section
- Footer with author credit

**styles.css** - Modern CSS with:
- CSS variables for theming
- Responsive breakpoints
- Animations and transitions

**app.js** - Full functionality:
- File handling with FileReader
- Processing logic
- Progress updates
- Download results
- Error handling

**README.md** - Documentation with:
- Live demo link: {url}
- Features list
- Privacy notice
- Author: Chirag Singhal

### 7. AUTHOR INFO
- Name: Chirag Singhal
- GitHub: https://github.com/chirag127
- Support: https://buymeacoffee.com/chirag127

OUTPUT: JSON object with file paths as keys, content as values.
Make the tool FULLY FUNCTIONAL - no placeholders!
"""

    def generate_optimization_prompt(
        self,
        repo_name: str,
        description: str,
        files: list[str],
    ) -> str:
        """
        Generate prompt for optimizing an existing repository.
        """
        file_list = "\n".join(f"- {f}" for f in files[:50])

        return f"""
Optimize this repository for better SEO and discoverability.

REPOSITORY: {repo_name}
DESCRIPTION: {description}

FILES:
{file_list}

## OPTIMIZATION TASKS

### 1. README.md
- Add badges (GitHub stars, license)
- Add live demo link if web project
- Add clear features section
- Add author section with links

### 2. SEO (for web projects)
- Add meta description
- Add Open Graph tags
- Add structured data

### 3. CENTRAL HUB
If HTML files exist, add:
```html
<script src="{self.CENTRAL_HUB}/shared/analytics.js" defer></script>
<script src="{self.CENTRAL_HUB}/shared/monetization.js" defer></script>
```

### 4. AUTHOR
- Chirag Singhal
- GitHub: chirag127
- Website: {self.CENTRAL_HUB}

OUTPUT: JSON with file paths and updated content.
Only include files that need changes.
"""

    def generate_quick_prompt(
        self,
        repo: str,
        repo_type: str,
        files: list[str],
    ) -> str:
        """
        Quick prompt for fast optimization.
        """
        return f"""
Quick optimization for: {repo} ({repo_type})
Files: {len(files)}

Tasks:
1. Update README.md with badges and demo link
2. Add central hub scripts if web project
3. Ensure author credit (Chirag Singhal)

Central hub: {self.CENTRAL_HUB}

Return JSON with file changes only.
"""