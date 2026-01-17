#!/usr/bin/env python3
"""
Generate Projects - Tool Website Generator

Creates single-file HTML tools (inline CSS + JS):
- All code in one index.html
- No build step, no separate files
- Direct GitHub Pages deployment
- Central hub analytics integration
- AI-generated metadata (title, description, keywords, features)

Usage:
  python generate_projects.py                    # Generate next tool
  python generate_projects.py --tool pdf-merger  # Generate specific
  python generate_projects.py --status           # Show progress
"""

import json
import logging
import os
import shutil
import subprocess
import sys
import time
import argparse
import asyncio
from pathlib import Path
from typing import Dict, Any, List

import requests

# Setup paths
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
sys.path.append(str(ROOT_DIR))

# Update imports for new structure
from src.ai.unified_client import UnifiedAIClient
from src.clients import WebSearchClient
# src.prompts is now... wait, prompts.py is still in src/ ?
# User list showed src\prompts.py. I didn't move it yet.
from src.ai.prompts import (
    get_tool_metadata_prompt,
    get_tool_logic_prompt,
    detect_category,
    TOOL_CATEGORIES,
    CATEGORY_CONFIGS
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('ToolGenerator')

# =============================================================================
# CONFIGURATION
# =============================================================================

GH_TOKEN = os.getenv("GH_TOKEN")
GH_USERNAME = "chirag127"
CENTRAL_HUB = "https://chirag127.github.io"

# Use ROOT_DIR defined at top of file
TOOLS_FILE = ROOT_DIR / "config" / "ar.txt"
STATE_FILE = ROOT_DIR / "state" / "tools_generated.json"
TEMP_DIR = ROOT_DIR / ".temp"
AGENTS_FILE = ROOT_DIR / "docs" / "AGENTS.md"

STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


# =============================================================================
# STATE MANAGEMENT
# =============================================================================

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except:
            pass
    return {"generated": [], "failed": [], "metadata_cache": {}}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


# =============================================================================
# AI-POWERED METADATA GENERATION
# =============================================================================

def generate_tool_metadata(name: str, ai: UnifiedAIClient, state: dict) -> dict:
    """Generate tool metadata using AI, with caching."""

    # Check cache first
    if name in state.get("metadata_cache", {}):
        print(f"  Using cached metadata for {name}")
        return state["metadata_cache"][name]

    print(f"  Generating metadata for {name}...")
    prompt = get_tool_metadata_prompt(name)

    result = ai.generate_json(prompt=prompt, max_tokens=1000, min_model_size=8)

    if result.success and result.json_content:
        metadata = {
            "title": result.json_content.get("title", name.replace("-", " ").title()),
            "description": result.json_content.get("description", f"Free online {name} tool."),
            "features": result.json_content.get("features", ["Fast", "Free", "Secure", "Private", "Mobile"]),
            "keywords": result.json_content.get("keywords", [name.replace("-", " ")]),
            "category": result.json_content.get("category", "Utilities"),
        }
        print(f"  + Metadata generated: {metadata['title']}")

        # Cache it
        if "metadata_cache" not in state:
            state["metadata_cache"] = {}
        state["metadata_cache"][name] = metadata
        save_state(state)

        return metadata
    else:
        print(f"  x Metadata generation failed: {result.error}")
        # Fallback to simple generation
        title = name.replace("-", " ").title()
        return {
            "title": title,
            "description": f"Free online {title.lower()} tool. Fast and secure.",
            "features": ["Client-side", "Fast", "Free", "No signup", "Mobile ready"],
            "keywords": [name.replace("-", " "), f"online {name}", f"free {name}"],
            "category": "Utilities",
        }


# =============================================================================
# PARSE TOOLS FROM ar.txt
# =============================================================================

def parse_tools() -> list[dict]:
    if not TOOLS_FILE.exists():
        print(f"Error: {TOOLS_FILE} not found")
        return []

    tools = []
    category = ""

    for line in TOOLS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            if "---" in line:
                category = line.replace("#", "").replace("-", "").strip()
            continue

        name = line.split("#")[0].strip()
        if name:
            tools.append({"name": name, "category": category})

    return tools


# =============================================================================
# GITHUB API
# =============================================================================

def gh_api(method: str, endpoint: str, data: dict = None):
    url = f"https://api.github.com{endpoint}"
    headers = {"Authorization": f"Bearer {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}

    if method == "GET":
        return requests.get(url, headers=headers, timeout=60)
    elif method == "POST":
        return requests.post(url, headers=headers, json=data, timeout=60)
    elif method == "PUT":
        return requests.put(url, headers=headers, json=data, timeout=120)


def create_repo(name: str, desc: str) -> bool:
    print(f"  Creating repo: {name}")
    r = gh_api("POST", "/user/repos", {
        "name": name,
        "description": desc[:300],
        "private": False,
        "auto_init": False,
    })
    if r.status_code == 201:
        print("  + Created")
        return True
    elif r.status_code == 422:
        print("  + Exists")
        return True
    print(f"  x Failed: {r.status_code}")
    return False


def enable_pages(name: str):
    print("  Enabling Pages...")
    r = gh_api("POST", f"/repos/{GH_USERNAME}/{name}/pages", {
        "source": {"branch": "main", "path": "/"}
    })
    if r.status_code in [201, 204, 409]:
        print("  + Pages enabled")


def set_github_topics(name: str, topics: list[str]):
    """Set repository topics (tags) via GitHub API."""
    if not topics:
        return

    # Clean topics: lowercase, alphanumeric + hyphens only, max 20 topics
    clean_topics = []
    for topic in topics[:20]:
        clean = topic.lower().replace(" ", "-").replace("_", "-")
        clean = "".join(c for c in clean if c.isalnum() or c == "-")
        if clean and len(clean) <= 50:
            clean_topics.append(clean)

    if not clean_topics:
        return

    logger.info(f"  🏷️ Setting topics: {', '.join(clean_topics[:5])}...")

    # Use special Accept header for topics API
    url = f"https://api.github.com/repos/{GH_USERNAME}/{name}/topics"
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    try:
        r = requests.put(url, headers=headers, json={"names": clean_topics}, timeout=30)
        if r.status_code in [200, 204]:
            logger.info(f"  ✅ Topics set: {len(clean_topics)}")
        else:
            logger.warning(f"  ⚠️ Topics API: {r.status_code}")
    except Exception as e:
        logger.error(f"  ❌ Topics error: {e}")


def git_push(name: str, files: dict[str, str]) -> bool:
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    repo_url = f"https://{GH_TOKEN}@github.com/{GH_USERNAME}/{name}.git"

    try:
        subprocess.run(["git", "init"], cwd=TEMP_DIR, capture_output=True, check=True)
        subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=TEMP_DIR, capture_output=True)
        subprocess.run(["git", "config", "user.email", "whyiswhen@gmail.com"], cwd=TEMP_DIR, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Chirag Singhal"], cwd=TEMP_DIR, capture_output=True)
        subprocess.run(["git", "branch", "-M", "main"], cwd=TEMP_DIR, capture_output=True)

        for path, content in files.items():
            file_path = TEMP_DIR / path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            print(f"  + {path}")

        subprocess.run(["git", "add", "-A"], cwd=TEMP_DIR, capture_output=True, check=True)
        subprocess.run(["git", "commit", "-m", "feat: initial release"], cwd=TEMP_DIR, capture_output=True, check=True)

        result = subprocess.run(
            ["git", "push", "-u", "--force", "origin", "main"],
            cwd=TEMP_DIR, capture_output=True, text=True
        )

        if result.returncode == 0:
            print("  + Pushed")
            return True
        return False

    except Exception as e:
        print(f"  x Git error: {e}")
        return False
    finally:
        if TEMP_DIR.exists():
            shutil.rmtree(TEMP_DIR, ignore_errors=True)


# =============================================================================
# WEB SEARCH RESEARCH (SearXNG Integration)
# =============================================================================

def research_tool(name: str, search_client: WebSearchClient) -> dict:
    """
    Research libraries, features, and best practices for a tool using WebSearchClient.

    Returns context for AI prompt including:
    - Recommended libraries
    - Implementation best practices
    - Feature ideas from competitors
    - Existing examples
    """
    logger.info(f"🔍 Researching: {name}")

    # Extract the main functionality from name
    topic = name.replace('-tool', '').replace('-', ' ')

    research = {
        'libraries': [],
        'best_practices': [],
        'features': [],
        'examples': [],
        'search_successful': False
    }

    if not search_client:
        return research

    try:
        # 1. Start with Implementation Resources (Free/APIs)
        logger.info(f"  📚 Searching free implementation resources for: {topic}")
        # Strictly search for free resources/APIs as requested
        lib_results = search_client.search(f"how to implement {topic} javascript free open source library api", limit=3)
        if lib_results:
            research['libraries'] = [
                {'title': r.title, 'url': r.url, 'content': r.description[:200]}
                for r in lib_results
            ]
            logger.info(f"  ✅ Found {len(research['libraries'])} libraries")
        else:
            logger.warning(f"  ⚠️ No library results")

        # 2. Search for Advanced Core Extensions
        logger.info(f"  ⭐ Searching advanced core extensions for: {topic}")
        feature_results = search_client.search(f"advanced {topic} algorithms implementation javascript free", limit=3)
        if feature_results:
            research['features'] = [
                {'title': r.title, 'content': r.description[:300]}
                for r in feature_results
            ]
            logger.info(f"  ✅ Found {len(research['features'])} feature sources")
        else:
            logger.warning(f"  ⚠️ No feature results")

        research['search_successful'] = True

    except Exception as e:
        logger.error(f"  ❌ Research failed: {e}")

    return research


def format_research_context(research: dict) -> str:
    """Format research results into context for AI prompt."""
    if not research.get('search_successful'):
        return "No web research available - use general best practices."

    context_parts = []

    # Include discovered features first (most important)
    if research.get('features'):
        feature_text = "\n".join([f"  - {f['content'][:150]}..." for f in research['features'][:3] if f.get('content')])
        if feature_text:
            context_parts.append(f"COMPETITOR FEATURES (implement these):\n{feature_text}")

    if research.get('libraries'):
        libs = "\n".join([f"  - {l['title']}: {l['url']}" for l in research['libraries'][:3]])
        context_parts.append(f"RECOMMENDED LIBRARIES:\n{libs}")

    if research.get('best_practices'):
        practices = "\n".join([f"  - {p['title']}" for p in research['best_practices'][:3]])
        context_parts.append(f"IMPLEMENTATION GUIDES:\n{practices}")

    return "\n\n".join(context_parts) if context_parts else "Use common JavaScript libraries."


# =============================================================================
# PROMPT OPTIMIZATION (THE "PROMPTING THE PROMPTER" LAYER)
# =============================================================================

def optimize_prompt(tool: dict, research_context: str, agents_context: str, ai: UnifiedAIClient) -> str:
    """
    Step 2 in the Pipeline: Ask a 'smart' model to write the perfect system instructions
    for the 'coding' model.

    Uses TIER 4 model (not largest) to reserve largest models for main generation.
    """
    logger.info("  ✨ Optimizing Instruction Sets (Tier 4 model)...")

    meta_prompt = f"""
ROLE: Chief AI Prompt Engineer (World Class).
CONTEXT: You are orchestrating the creation of a high-end web tool: "{tool['name']}".
INPUT:
- Tool Metadata: {json.dumps(tool, indent=2)}
- Research: {research_context[:4000]}
- System Architecture: {agents_context[:4000]} ... (truncated)

TASK:
Write a STACK-RANKED, PERFECTIONIST CODING PROMPT for an AI Developer.
The output prompt must encompass:
1. Exact Library choices from the System Architecture (e.g. PDF-lib for PDFs).
2. UI/UX Mandates (Apex 2026 Spatial Glass).
3. Step-by-Step implementation logic (IIFE, Error handling, DOM structure).
4. Critical Constraints (No Headers, Single File, Config Injection, INLINE CSS/JS).
5. CORE EXTENSION ONLY: Advanced features must be extensions of the main purpose.
6. STRICTLY FREE: Use only free APIs/Libraries. No paid services.

MANDATORY INCLUSIONS (THE AI DEVELOPER **MUST** IMPLEMENT THESE):
7. CRITICAL CSS: The <main> element MUST have `padding-top: 80px;` because the Universal Engine injects a fixed header. Without this, content is hidden behind the header.
8. JAVASCRIPT QUALITY (ZERO RUNTIME ERRORS):
   - Validate all inputs: check if value is array before .map(), .filter(), .forEach()
   - Check element existence: `if (element) {{ element.doSomething() }}`
   - Use defensive defaults: `const arr = input || [];`
   - Wrap ALL async operations in try-catch blocks
   - Show user-friendly errors in the UI, not just console.log

Your output should be the EXACT PROMPT string I will paste to the coding AI.
Start with "Role: Expert..." and end with "...implementation."
"""

    # Use tier 4 (4th largest model) to reserve largest for main generation
    result = ai.generate_with_tier(
        prompt=meta_prompt,
        max_tokens=2000,
        start_tier=4  # Use 4th largest model (e.g., Mistral Large 123B)
    )

    if result.success:
        logger.info(f"  ✨ Prompt Optimized using {result.model_used}")
        return result.content
    else:
        logger.warning(f"  ⚠️ Prompt Optimization Failed: {result.error}")
        return "" # Fallback to default


def generate_single_html(tool: dict, ai: UnifiedAIClient, search_client: WebSearchClient = None) -> str:
    """
    Generate a SINGLE-FILE tool (HTML+CSS+JS) using the Generative UI Engine.
    Uses AGENTS.md as the system prompt (Apex Technical Authority).

    Uses TIER 1 (largest available model) for maximum quality single-file generation.
    Timeout is 900s (15 min) for 671B models.
    """
    start_time = time.time()

    # 0. Load Agents Context (The "Brain")
    if not AGENTS_FILE.exists():
        logger.error(f"AGENTS.md not found at {AGENTS_FILE}")
        return "<h1>Error: System Brain Missing (AGENTS.md)</h1>"

    agents_context = AGENTS_FILE.read_text(encoding="utf-8")

    # 1. Research
    research_context = ""
    # WebSearchClient does not have is_available() method - it always tries its best
    if search_client:
        logger.info("  🔍 Researching tool requirements...")
        try:
            research_results = research_tool(tool['name'], search_client)
            research_context = format_research_context(research_results)
            logger.info(f"  📋 Research context generated: {len(research_context)} chars")
        except Exception as e:
            logger.warning(f"  ⚠️ Research failed: {e}")

    # 2. PROMPT OPTIMIZATION (Uses Tier 4 model to save largest for generation)
    optimized_instructions = optimize_prompt(tool, research_context, agents_context, ai)

    # 3. Build the COMPLETE SINGLE-FILE prompt
    logger.info(f"  🚀 SINGLE-FILE Generation for {tool['name']} (Tier 1 - Largest Model)...")

    if optimized_instructions:
        prompt = f"""
SYSTEM INSTRUCTION: IMPLEMENT THE FOLLOWING SPECIFICATION EXACTLY.

{optimized_instructions}

CRITICAL OVERRIDE:
- OUTPUT: A SINGLE `index.html` file containing ALL HTML, CSS, and JavaScript.
- STYLE/SCRIPT ENFORCEMENT:
  - CSS MUST be inside <style> tags in the <head>.
  - JavaScript MUST be inside <script> tags at the end of <body>.
  - NO external .css or .js files (except the Universal Config/Core scripts below).
- UNIVERSAL ARCHITECTURE:
  - MUST include in <head>: <script src="https://chirag127.github.io/universal/config.js"></script>
  - MUST include in <head>: <script src="https://chirag127.github.io/universal/core.js"></script>
  - DO NOT generate <header> or <footer> tags (the Universal Engine injects them).
  - Wrap ALL content in <main> tag.
- CRITICAL CSS FIX (HEADER OVERLAP PREVENTION):
  - The Universal Engine injects a FIXED header at the top.
  - You MUST add `padding-top: 80px;` (or `margin-top: 80px;`) to the <main> element.
  - Example: `main {{ padding-top: 80px; }}`
  - Without this, your content WILL be hidden behind the fixed header.
- JAVASCRIPT QUALITY REQUIREMENTS:
  - ABSOLUTELY NO RUNTIME ERRORS. Test every code path mentally.
  - Always validate input types: check if value is array before calling .map(), .filter(), .forEach().
  - Always check if elements exist before accessing properties: `if (element) {{ ... }}`
  - Use defensive coding: `const range = Array.isArray(input) ? input : [input];`
  - Wrap all async operations in try-catch blocks.
  - Use `console.error()` for debugging, show user-friendly error messages in UI.
- FORMAT: Return ONLY the HTML code block within ```html flags.
"""
    else:
        # Fallback to standard prompt
        prompt = f"""
TASK: GENERATE THE COMPLETE SOURCE CODE FOR: "{tool.get('title', tool['name'])}"
DESCRIPTION: {tool.get('description', '')}
Features: {json.dumps(tool.get('features', []), indent=2)}

{research_context}

REQUIREMENTS:
1. OUTPUT: A SINGLE `index.html` file containing ALL HTML, CSS, and JavaScript.
2. UNIVERSAL ARCHITECTURE (CRITICAL):
   - MUST include in <head>: <script src="https://chirag127.github.io/universal/config.js"></script>
   - MUST include in <head>: <script src="https://chirag127.github.io/universal/core.js"></script>
   - DO NOT generate <header> or <footer> tags (The Universal Engine injects them).
   - ALL content must be wrapped in <main> tag.
3. CRITICAL CSS FIX (HEADER OVERLAP PREVENTION):
   - The Universal Engine injects a FIXED header at the top (height ~70px).
   - You MUST add CSS: `main {{ padding-top: 80px; }}`
   - Without this, your content WILL be hidden behind the fixed header.
4. LIBRARY SELECTION (THE MENU):
   - Consult "12. APEX APPROVED CLIENT-SIDE ENGINES" in the System Context.
   - For PDF tools, you MUST use `PDF-lib` or `pdf-merger-js`.
   - For Video tools, you MUST use `FFmpeg.wasm`.
   - LOAD LIBRARIES VIA CDN (cdnjs/unpkg).
5. JAVASCRIPT QUALITY (ZERO ERRORS TOLERANCE):
   - ABSOLUTELY NO RUNTIME ERRORS. Think through every code path.
   - Validate types before array methods: `if (Array.isArray(x)) x.map(...)`
   - Check elements exist: `if (element) element.style.display = 'none';`
   - Wrap async code in try-catch: `try {{ await fetch(...) }} catch (e) {{ showError(e) }}`
   - Use defensive defaults: `const arr = input || [];`
   - Show user-friendly errors in the UI, not just console.
6. AESTHETICS: **Apex 2026 Spatial-Adaptive**.
   - "Spatial Glass" look (backdrop-filter: blur).
   - "Bento Grid" layouts.
7. FORMAT: Return ONLY the HTML code block within ```html flags.
"""

    # 4. Generate using TIER 1 (largest model) for best quality
    result = ai.generate(
        prompt=prompt,
        system_prompt=agents_context,
        max_tokens=32000,  # Large buffer for complete single file
        min_model_size=200,  # Use 200B+ models (God-class preferred)
        temperature=0.7
    )

    if not result.success:
        logger.error(f"AI Generation Failed: {result.error}")
        return f"<h1>Generation Failed</h1><p>{result.error}</p>"

    # 5. Extract Code
    content = result.content
    if "```html" in content:
        content = content.split("```html")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()

    elapsed = time.time() - start_time
    logger.info(f"  ✅ Generated {len(content)} bytes of HTML in {elapsed:.1f}s using {result.model_used}")
    return content


# =============================================================================
# COMPREHENSIVE README GENERATOR
# =============================================================================

def generate_comprehensive_readme(tool: dict) -> str:
    """
    Generate a comprehensive, professional README.md for a tool repository.

    Includes: Badges, Live Demo, Features, How it Works, Tech Stack,
    Installation, Usage, Privacy, Contributing, License, Author sections.
    """
    name = tool["name"]
    title = tool.get("title", name)
    description = tool.get("description", "")
    features = tool.get("features", [])
    keywords = tool.get("keywords", [])
    category = tool.get("category", "Tool")

    # Generate feature list
    feature_list = "\n".join(f"- ✅ {f}" for f in features) if features else "- ✅ Easy to use interface"

    # Generate keywords/tags for SEO
    keyword_badges = " ".join(f"`{k}`" for k in keywords[:10]) if keywords else ""

    readme = f'''# {title}

<p align="center">
  <a href="{CENTRAL_HUB}/{name}/">
    <img src="https://img.shields.io/badge/Try%20Live%20Demo-blue?style=for-the-badge&logo=googlechrome&logoColor=white" alt="Live Demo">
  </a>
  <a href="https://github.com/chirag127/{name}/stargazers">
    <img src="https://img.shields.io/github/stars/chirag127/{name}?style=for-the-badge&logo=github" alt="Stars">
  </a>
  <a href="https://github.com/chirag127/{name}/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  </a>
</p>

<p align="center">
  <strong>{description}</strong>
</p>

---

## 🚀 Live Demo

**👉 [Try {title} Now]({CENTRAL_HUB}/{name}/) 👈**

No installation required. Works directly in your browser.

---

## ✨ Features

{feature_list}

---

## 🔧 How It Works

1. **Open the Tool** - Visit the live demo link above
2. **Upload/Input** - Drag & drop files or enter your data
3. **Process** - All processing happens locally in your browser
4. **Download** - Get your results instantly

> 💡 **No server uploads!** Your files never leave your device.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure & Semantics |
| **CSS3** | Styling & Animations |
| **JavaScript** | Client-side Logic |
| **WebAssembly** | Heavy Processing (when needed) |
| **[Universal Engine](https://github.com/chirag127/chirag127.github.io)** | Shared Components |

---

## 📦 Installation

### Option 1: Use Online (Recommended)
Just visit: [{CENTRAL_HUB}/{name}/]({CENTRAL_HUB}/{name}/)

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/chirag127/{name}.git
cd {name}

# Serve locally (Python)
python -m http.server 8000

# Or use any static file server
npx serve .
```
Open `http://localhost:8000` in your browser.

---

## 📖 Usage

```
1. Open the tool in your browser
2. Follow the on-screen instructions
3. Download your processed files
```

---

## 🔒 Privacy & Security

| Aspect | Details |
|--------|---------|
| **Data Processing** | 100% client-side (in your browser) |
| **File Storage** | Files are NEVER uploaded to any server |
| **Cookies** | Only essential cookies for analytics |
| **Tracking** | Privacy-friendly analytics (Plausible/Umami) |

**Your data stays on YOUR device. Always.**

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

```
MIT License

Copyright (c) 2026 Chirag Singhal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files.
```

---

## 👤 Author

<p align="center">
  <a href="https://github.com/chirag127">
    <img src="https://img.shields.io/badge/GitHub-chirag127-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
  <a href="https://buymeacoffee.com/chirag127">
    <img src="https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Support-FFDD00?style=for-the-badge&logo=buymeacoffee&logoColor=black" alt="Buy Me A Coffee">
  </a>
</p>

---

## 🏷️ Tags

{keyword_badges}

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/chirag127">Chirag Singhal</a>
</p>

<p align="center">
  Part of the <a href="{CENTRAL_HUB}">Chirag Hub</a> - 450+ Free Online Tools
</p>
'''

    return readme


# =============================================================================
# MAIN GENERATION FLOW
# =============================================================================

def generate_tool(tool: dict, ai: UnifiedAIClient, state: dict, search_client: WebSearchClient = None) -> bool:
    """Generate a tool with AI and optional web research."""
    logger.info(f"\n{'='*50}")
    logger.info(f"Generating: {tool['name']}")
    logger.info(f"{'='*50}")

    # Generate metadata first
    metadata = generate_tool_metadata(tool["name"], ai, state)
    tool.update(metadata)

    if not create_repo(tool["name"], tool["description"]):
        return False

    # Generate HTML with web research
    html_content = generate_single_html(tool, ai, search_client)

    files = {
        "index.html": html_content,
        "README.md": generate_comprehensive_readme(tool),
    }

    logger.info(f"  Writing {len(files)} files...")
    if not git_push(tool["name"], files):
        return False

    time.sleep(2)
    enable_pages(tool["name"])

    # Set GitHub topics from keywords
    topics = tool.get("keywords", []) + [tool.get("category", "").lower()]
    set_github_topics(tool["name"], topics)

    if tool["name"] not in state["generated"]:
        state["generated"].append(tool["name"])
    save_state(state)

    logger.info(f"\n✅ Complete: {CENTRAL_HUB}/{tool['name']}/")
    return True


def show_status():
    """Show generation progress status."""
    tools = parse_tools()
    state = load_state()
    done = len(state["generated"])
    cached = len(state.get("metadata_cache", {}))
    logger.info(f"\n{'='*50}")
    logger.info(f"Progress: {done}/{len(tools)} ({done/len(tools)*100:.0f}%)")
    logger.info(f"Remaining: {len(tools) - done}")
    logger.info(f"Cached Metadata: {cached}")
    logger.info(f"{'='*50}")


def main():
    """Main entry point for tool generation."""
    if not GH_TOKEN:
        logger.error("Error: GH_TOKEN not set")
        sys.exit(1)

    args = sys.argv[1:]
    state = load_state()

    # Initialize AI client
    ai = UnifiedAIClient()

    # Initialize Web Search client
    search_client = WebSearchClient()
    logger.info("🔍 Web Search Client: INITIALIZED")

    if "--status" in args:
        show_status()
        return

    tools = parse_tools()

    if "--tool" in args:
        idx = args.index("--tool")
        if idx + 1 < len(args):
            name = args[idx + 1]
            tool = next((t for t in tools if t["name"] == name), None)
            if tool:
                generate_tool(tool, ai, state, search_client)
            else:
                logger.error(f"Tool not found: {name}")
        return

    if "--all" in args:
        remaining = [t for t in tools if t["name"] not in state["generated"]]
        for tool in remaining:
            generate_tool(tool, ai, state, search_client)
            time.sleep(5)
        return

    # Default: generate next tool
    for tool in tools:
        if tool["name"] not in state["generated"]:
            generate_tool(tool, ai, state, search_client)
            return

    logger.info("All tools generated!")


if __name__ == "__main__":
    main()
