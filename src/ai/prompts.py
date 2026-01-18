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
Role: Singularity Architect with 40+ years experience at Google/DeepMind. Code name: Armstrong.
Philosophy: Zero-Defect, High-Velocity, Future-Proof, AI-Native. "Everything, everywhere, all at once."
Output: EXECUTION-ONLY. Production-ready code. No placeholders. No chatter."""


# =============================================================================
# CATEGORY DETECTION & SPECIALIZED PROMPTS (NEW)
# =============================================================================

# Website category detection based on name prefixes
WEBSITE_CATEGORIES = {
    "pdf": ["PDF-", "Document-", "Merge-", "Split-", "Compress-PDF", "Extract-PDF"],
    "image": ["Image-", "Photo-", "Background-", "Crop-", "Resize-", "Convert-JPG", "Convert-PNG", "HEIC-", "SVG-", "Base64-Image", "Meme-", "Watermark-", "Color-Palette", "Blur-", "Pixelate-"],
    "video": ["Video-", "Screen-", "Record-", "Trim-Video", "Convert-MP4", "Convert-MOV", "Convert-AVI", "Convert-MKV", "Convert-WEBM", "GIF-"],
    "audio": ["Audio-", "Voice-", "BPM-", "Microphone-", "Tone-", "Music-", "Convert-WAV", "Convert-MP3", "Convert-M4A"],
    "text": ["Text-", "Word-", "Lorem-", "Diff-", "Remove-", "Slug-", "Morse-", "Unicode-", "Zalgo-", "Repeater-", "ASCII-", "Markdown-", "Regex-", "Email-", "Phonetic-", "Encrypt-", "Count-"],
    "dev": ["JSON-", "XML-", "SQL-", "HTML-", "CSS-", "JS-", "UUID-", "Hash-", "Cron-", "HTPasswd-", "Meta-Tag", "Git-", "Docker-", "JWT-", "Minify-", "Format-"],
    "calc": ["Calculate-", "Calculator-", "Percentage-", "Geometry-", "Algebra-", "Fraction-", "Binary-", "Prime-", "Standard-", "Physics-", "Electrical-", "Resistor-", "Permutation-", "Triangle-"],
    "finance": ["Loan-", "Mortgage-", "Interest-", "Discount-", "Salary-", "Currency-", "Inflation-", "Credit-", "ROI-", "Break-Even", "Tax-", "Tip-", "Fuel-", "Retirement-", "Stock-", "SaaS-", "Freelance-", "Real-Estate", "Crypto-"],
    "convert": ["Convert-", "Converter-", "Encoder-", "Decoder-", "EPUB-", "MOBI-", "AZW3-", "WEBP-", "Unit-"],
    "game": ["Game-", "Sudoku-", "Wordle-", "Crossword-", "Tic-Tac-", "Rock-Paper-", "Typing-", "Reaction-", "Biorhythm-", "Love-", "Magic-8-", "Bingo-", "Memory-", "Stopwatch-", "Timer-", "Dice-", "Coin-", "Random-", "Wheel-"],
    "utility": ["QR-", "Barcode-", "URL-", "IP-", "Password-", "Subnet-", "Unix-", "Date-", "Time-", "Age-", "Clock-", "Speed-Test", "Screen-", "Keyboard-", "File-", "ZIP-", "MIME-", "VCard-", "ICS-", "Duplicate-", "Bulk-"]
}

# Category-specific libraries and UI elements
CATEGORY_CONFIGS = {
    "pdf": {
        "libraries": ["pdf-lib (https://cdn.jsdelivr.net/npm/pdf-lib/dist/pdf-lib.min.js)"],
        "ui_elements": "PDF page preview canvas, page thumbnails, page reordering",
        "file_types": ".pdf"
    },
    "image": {
        "libraries": ["Cropper.js for crop", "FileSaver.js for download"],
        "ui_elements": "Image preview canvas, before/after slider, zoom controls",
        "file_types": ".jpg,.jpeg,.png,.webp,.gif,.svg,.heic"
    },
    "video": {
        "libraries": ["ffmpeg.wasm for processing (OPTIONAL - use native if possible)"],
        "ui_elements": "Video preview, timeline scrubber, frame selector",
        "file_types": ".mp4,.webm,.mov,.avi,.mkv"
    },
    "audio": {
        "libraries": ["WaveSurfer.js for waveform, Howler.js for playback"],
        "ui_elements": "Waveform display, playback controls, time markers",
        "file_types": ".mp3,.wav,.ogg,.m4a,.flac"
    },
    "text": {
        "libraries": [],
        "ui_elements": "Large textarea input, live output panel, copy button, character counter",
        "file_types": "none"
    },
    "dev": {
        "libraries": ["Prism.js for syntax highlighting", "CodeMirror for editing"],
        "ui_elements": "Code editor with line numbers, syntax highlighting, format/minify toggles",
        "file_types": "none"
    },
    "calc": {
        "libraries": ["Math.js for complex calculations"],
        "ui_elements": "Input fields with labels, formula display, result with copy",
        "file_types": "none"
    },
    "finance": {
        "libraries": ["Chart.js for graphs"],
        "ui_elements": "Input fields, calculation result, optional chart visualization",
        "file_types": "none"
    },
    "convert": {
        "libraries": ["Various per format"],
        "ui_elements": "Dual panel (input/output), swap button, format selector",
        "file_types": "varies"
    },
    "game": {
        "libraries": [],
        "ui_elements": "Game canvas, score display, restart button, instructions",
        "file_types": "none"
    },
    "utility": {
        "libraries": ["QRCode.js for QR", "JsBarcode for barcodes"],
        "ui_elements": "Tool-specific interface, result display, download/copy",
        "file_types": "varies"
    }
}


def detect_category(tool_name: str) -> str:
    """Detect website category from its name."""
    name_upper = tool_name.upper()
    for category, prefixes in WEBSITE_CATEGORIES.items():
        for prefix in prefixes:
            if name_upper.startswith(prefix.upper()) or prefix.upper() in name_upper:
                return category
    return "utility"  # Default fallback


def get_category_config(category: str) -> dict:
    """Get configuration for a website category."""
    return CATEGORY_CONFIGS.get(category, CATEGORY_CONFIGS["utility"])


# =============================================================================
# REPO NAME ONLY PROMPT - Derives everything from just the repo name
# Jan 2026: Simplified metadata generation, no prompt enhancement needed
# =============================================================================

REPO_NAME_ONLY_PROMPT = """You are the Apex Technical Authority. Generate complete project metadata from ONLY the repository name.

REPOSITORY NAME: {repo_name}

CRITICAL: Derive ALL information from the repository name alone. Infer:
1. What the website does (from name)
2. What category it belongs to (PDF, Image, Text, Dev, Calculator, etc.)
3. What features it should have (based on website type)
4. What keywords users would search for

OUTPUT JSON FORMAT:
{{
  "title": "Human-readable title (catchy, under 60 chars)",
  "description": "SEO meta description under 155 chars, include 'free' and 'privacy'",
  "features": [
    "Feature 1 (core functionality)",
    "Feature 2 (unique selling point)",
    "Feature 3 (ease of use)",
    "Feature 4 (privacy/security)",
    "Feature 5 (compatibility)"
  ],
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
  "category": "One of: pdf, image, video, audio, text, dev, calc, finance, convert, game, utility"
}}

RULES:
1. ONLY use the repository name as input - no additional context needed
2. Infer the website's purpose from naming (e.g., "pdf-merge" = PDF merger website)
3. Generate realistic, production-ready metadata
4. Output ONLY valid JSON, no markdown code blocks."""


def get_repo_name_only_prompt(repo_name: str) -> str:
    """Generate prompt that derives all metadata from repository name only."""
    return REPO_NAME_ONLY_PROMPT.format(repo_name=repo_name)


# =============================================================================
# WEBSITE METADATA GENERATION PROMPT
# =============================================================================

WEBSITE_METADATA_PROMPT = """You are the Apex Technical Authority generating metadata for a website.

WEBSITE NAME: {tool_name}

TASK: Generate professional, SEO-optimized metadata for this website. Remember: "Everything, everywhere, all at once."
The project is part of the "Armstrong" initiative.

CONTEXT (Jan 2026):
- All websites are frontend-only (client-side processing)
- Users value privacy (files never leave device)
- Target: High traffic, monetizable utility websites
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
# WEBSITE LOGIC GENERATION PROMPT (2026 UI STANDARDS)
# =============================================================================

WEBSITE_LOGIC_PROMPT = """You are the Apex Technical Authority (Jan 2026 Standards).

TASK: Write production-ready JavaScript for website: "{title}"

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

OUTPUT FORMAT:
Return A SINGLE `index.html` file containing ALL HTML, CSS (in <style>), and JavaScript (in <script>).
NO external files. NO JSON. Enclose in ```html``` block."""


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

WEBSITE: {tool_name}
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

def get_website_metadata_prompt(tool_name: str) -> str:
    """Generate prompt for website metadata generation."""
    return WEBSITE_METADATA_PROMPT.format(tool_name=tool_name)


def get_website_logic_prompt(title: str, description: str, features: list,
                          research_context: str = "", tool_name: str = "") -> str:
    """Generate prompt for website JavaScript logic with research context and category-specific info."""

    # Detect category and get config
    category = detect_category(tool_name) if tool_name else "utility"
    config = get_category_config(category)

    # Build category-specific context
    category_context = f"""
DETECTED CATEGORY: {category.upper()}
RECOMMENDED LIBRARIES: {', '.join(config['libraries']) if config['libraries'] else 'None required'}
UI ELEMENTS FOR THIS CATEGORY: {config['ui_elements']}
FILE TYPES: {config['file_types']}"""

    full_research = f"{research_context}\n{category_context}" if research_context else category_context

    return WEBSITE_LOGIC_PROMPT.format(
        title=title,
        description=description,
        features=", ".join(features),
        research_context=full_research
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
