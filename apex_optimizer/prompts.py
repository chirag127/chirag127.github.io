"""
Apex Optimizer Prompts - January 2026 Standards

APEX TECHNICAL AUTHORITY PROMPTS:
- Frontend-only architecture (NO backend)
- 2026 UI/UX (Spatial Glass, Kinetic Typography, Bento Grids)
- Client-side processing only
- Zero placeholders, production-ready output

Used by generate_projects.py and automation scripts.
"""

import logging

logger = logging.getLogger("ApexOptimizer")


# =============================================================================
# CORE IDENTITY (2026 APEX STANDARD)
# =============================================================================

APEX_IDENTITY = """You are the Apex Technical Authority (Jan 2026).
Role: Singularity Architect with 40+ years experience at Google/DeepMind.
Philosophy: Zero-Defect, High-Velocity, Future-Proof, AI-Native.
Output: EXECUTION-ONLY. Production-ready code. No placeholders. No chatter."""


# =============================================================================
# TOOL METADATA GENERATION PROMPT
# =============================================================================

TOOL_METADATA_PROMPT = """You are the Apex Technical Authority generating metadata for a web tool.

TOOL NAME: {tool_name}

TASK: Generate professional, SEO-optimized metadata for this tool.

CONTEXT (Jan 2026):
- All tools are frontend-only (client-side processing)
- Users value privacy (files never leave device)
- Target: High traffic, monetizable utility tools
- Deployed on GitHub Pages

OUTPUT JSON FORMAT:
{{
  "title": "Human-readable title (catchy, under 60 chars)",
  "description": "SEO meta description under 155 chars, include 'free' and 'privacy'",
  "features": [
    "Feature 1 (benefit-focused)",
    "Feature 2 (unique selling point)",
    "Feature 3 (ease of use)",
    "Feature 4 (privacy/security)",
    "Feature 5 (compatibility)"
  ],
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "category": "Category (Document, Image, Developer, Audio, Video, Utility)"
}}

RULES:
1. Title: Catchy, action-oriented (e.g., "PDF Merger & Splitter Pro")
2. Description: Under 155 chars, mention "free", "no upload", "privacy"
3. Features: 5 benefit-focused items (not just technical specs)
4. Keywords: 5-6 high-value SEO terms
5. Output ONLY valid JSON, no markdown code blocks."""


# =============================================================================
# TOOL LOGIC GENERATION PROMPT (2026 UI STANDARDS)
# =============================================================================

TOOL_LOGIC_PROMPT = """You are the Apex Technical Authority (Jan 2026 Standards).

TASK: Write production-ready JavaScript for: "{title}"

DESCRIPTION: {description}
FEATURES TO IMPLEMENT: {features}

{research_context}

HTML TEMPLATE ELEMENTS (Already exist):
- <input type="file" id="fileInput"> (Hidden file input)
- <label id="dropZone"> (Drag-drop area, triggers fileInput)
- <button id="actionBtn"> (Main CTA - disabled by default)
- <div id="statusArea"> (Progress bars, file list, options)
- <div id="resultsContent"> (Output/download area)
- <div id="results" class="hidden"> (Results container)

ARCHITECTURE RULES (CRITICAL):
1. FRONTEND-ONLY: All processing client-side. NO fetch() to external APIs.
2. Use libraries via CDN (pdf-lib, jszip, etc.) - include in comment
3. Event delegation: document.addEventListener('DOMContentLoaded', ...)
4. Zero global variables - use IIFE or modules

IMPLEMENTATION REQUIREMENTS:
1. Drag-drop handling: dragover, dragleave, drop events on dropZone
2. File validation: Check type/size before processing
3. Progress reporting: Update statusArea with percentage
4. Results display: Downloadable links in resultsContent
5. Error handling: try/catch with user-friendly messages
6. Memory cleanup: URL.revokeObjectURL() after downloads

UI/UX (2026 SPATIAL-ADAPTIVE):
1. Kinetic feedback: transform: scale(0.98) on button press
2. Transitions: all 0.3s cubic-bezier(0.4, 0, 0.2, 1)
3. Progress bars: linear-gradient with var(--primary)
4. File list: Removable items with × button
5. Success state: Green accent, celebrate animation

CSS VARIABLES AVAILABLE:
var(--primary), var(--secondary), var(--accent)
var(--success), var(--error)
var(--bg-card), var(--bg-dark)
var(--text-main), var(--text-muted)

OUTPUT FORMAT (JSON only, no markdown):
{{
  "js": "/* Complete JavaScript with CDN comment at top */",
  "css": "/* Additional CSS for custom elements */"
}}"""


# =============================================================================
# README GENERATION PROMPT (HERO-TIER)
# =============================================================================

README_PROMPT = """Generate a Hero-Tier README.md for GitHub.

REPO: {repo_name}
TITLE: {title}
DESCRIPTION: {description}
FEATURES: {features}
LIVE_URL: {live_url}

STRUCTURE:
1. # Title with relevant emoji
2. One-line description
3. Badges: ![GitHub Stars], ![License MIT]
4. ## 🚀 Live Demo (prominent link)
5. ## ✨ Features (bullet list)
6. ## 🔒 Privacy (client-side processing note)
7. ## 🛠️ Tech Stack (one line)
8. ## 👨‍💻 Author (links to GitHub, Support)

RULES:
1. Keep it concise (under 80 lines)
2. Use emojis strategically
3. Live demo link is MOST IMPORTANT
4. Highlight privacy/security
5. Output ONLY the README markdown"""


# =============================================================================
# GITHUB TOPICS PROMPT
# =============================================================================

TOPICS_PROMPT = """Generate GitHub repository topics (tags) for SEO.

TOOL: {tool_name}
DESCRIPTION: {description}

OUTPUT: JSON array of 5-10 lowercase topic strings.
Topics should be:
1. Relevant to the tool functionality
2. Popular/searchable on GitHub
3. Include technology keywords (javascript, html5, pwa)

Example: ["pdf", "pdf-merger", "javascript", "tool", "free", "privacy", "web-app"]

OUTPUT ONLY the JSON array, no other text."""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_tool_metadata_prompt(tool_name: str) -> str:
    """Generate prompt for tool metadata generation."""
    return TOOL_METADATA_PROMPT.format(tool_name=tool_name)


def get_tool_logic_prompt(title: str, description: str, features: list,
                          research_context: str = "") -> str:
    """Generate prompt for tool JavaScript logic with research context."""
    return TOOL_LOGIC_PROMPT.format(
        title=title,
        description=description,
        features=", ".join(features),
        research_context=research_context or "Use general best practices."
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


def get_topics_prompt(tool_name: str, description: str) -> str:
    """Generate prompt for GitHub topics."""
    return TOPICS_PROMPT.format(
        tool_name=tool_name,
        description=description
    )
