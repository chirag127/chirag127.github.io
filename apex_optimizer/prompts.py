"""
Apex Optimizer Prompts - Modernized January 2026

Centralized prompts for AI-powered content generation.
Used by generate_projects.py and other automation scripts.
"""

import logging

logger = logging.getLogger("ApexOptimizer")


# =============================================================================
# CORE IDENTITY
# =============================================================================

APEX_IDENTITY = """You are an Expert Software Engineer and Technical Writer.
You create production-ready, high-quality content with zero placeholders.
Your output is always concise, professional, and immediately usable."""


# =============================================================================
# TOOL METADATA GENERATION PROMPT
# =============================================================================

TOOL_METADATA_PROMPT = """You are generating metadata for a web-based tool.

TOOL NAME: {tool_name}

TASK: Generate professional metadata for this tool based on its name.
Infer the tool's purpose from its name and create compelling, SEO-optimized content.

OUTPUT JSON FORMAT:
{{
  "title": "Human-readable title (e.g., 'PDF Merger & Splitter')",
  "description": "One-line description under 160 chars for SEO",
  "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"],
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4"],
  "category": "Category name (e.g., 'Document Tools', 'Image Tools')"
}}

RULES:
1. Title should be catchy and descriptive.
2. Description must be under 160 characters.
3. Exactly 5 features that highlight the tool's capabilities.
4. 4-6 SEO keywords.
5. Output ONLY the JSON object, no markdown."""


# =============================================================================
# TOOL LOGIC GENERATION PROMPT
# =============================================================================

TOOL_LOGIC_PROMPT = """You are an Expert Frontend Developer.

TASK: Write JavaScript logic (and optional CSS) for: "{title}"

DESCRIPTION: {description}
FEATURES: {features}

HTML STRUCTURE (Already exists, DO NOT output HTML):
- <input type="file" id="fileInput">
- <label id="dropZone"> (Drop area)
- <button id="actionBtn"> (Process button - disabled by default)
- <div id="statusArea"> (For progress bars, options)
- <div id="resultsContent"> (For final output)
- <div id="results"> (Container, hidden by default)

REQUIREMENTS:
1. Handle file selection (drag-drop or click).
2. Enable actionBtn when file is selected.
3. Process files CLIENT-SIDE ONLY (use FileReader, Canvas, etc.).
4. Show progress in statusArea.
5. Display results in resultsContent.
6. Use CSS variables: var(--primary), var(--bg-card).

OUTPUT JSON:
{{
  "js": "/* Pure JS code */",
  "css": "/* Optional CSS */"
}}"""


# =============================================================================
# README GENERATION PROMPT
# =============================================================================

README_PROMPT = """Generate a professional README.md for a GitHub repository.

REPO: {repo_name}
TITLE: {title}
DESCRIPTION: {description}
FEATURES: {features}
LIVE_URL: {live_url}

STRUCTURE:
1. Title with emoji
2. Badges (GitHub Stars, License)
3. One-line description
4. Live Demo link
5. Features list
6. Privacy note (client-side processing)
7. Author section with links

Keep it concise. Output ONLY the README content."""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_tool_metadata_prompt(tool_name: str) -> str:
    """Generate prompt for tool metadata generation."""
    return TOOL_METADATA_PROMPT.format(tool_name=tool_name)


def get_tool_logic_prompt(title: str, description: str, features: list) -> str:
    """Generate prompt for tool JavaScript logic."""
    return TOOL_LOGIC_PROMPT.format(
        title=title,
        description=description,
        features=", ".join(features)
    )


def get_readme_prompt(repo_name: str, title: str, description: str,
                      features: list, live_url: str) -> str:
    """Generate prompt for README content."""
    return README_PROMPT.format(
        repo_name=repo_name,
        title=title,
        description=description,
        features="\n".join(f"- {f}" for f in features),
        live_url=live_url
    )
