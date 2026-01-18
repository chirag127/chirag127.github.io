#!/usr/bin/env python3
"""
Generate Projects - Website Generator

Creates single-file HTML tools (inline CSS + JS):
- All code in one index.html
- No build step, no separate files
- Direct GitHub Pages deployment
- Central hub analytics integration
- AI-generated metadata (title, description, keywords, features)

Usage:
  python generate_projects.py                    # Generate next website
  python generate_projects.py --website pdf-merger  # Generate specific website
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
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, Any, List

import requests

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Setup paths
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
sys.path.append(str(ROOT_DIR))

# Update imports for new structure
from src.ai.unified_client import UnifiedAIClient
from src.clients import WebSearchClient
from src.core.config import Settings
from src.ai.prompts import (
    get_website_metadata_prompt,
    get_website_logic_prompt,
    detect_category,
    WEBSITE_CATEGORIES,
    CATEGORY_CONFIGS
)
from src.core.seo_schema import generate_software_schema

# Polymorphs generation support
try:
    from polymorphs_tools import (
        PolymorphsToolGenerator,
        get_sidebar_models_from_chain,
        generate_sidebar_html,
        inject_sidebar_into_html
    )
    POLYMORPHS_AVAILABLE = True
except ImportError:
    POLYMORPHS_AVAILABLE = False

# Multi-platform deployment
try:
    sys.path.append(str(SCRIPT_DIR))
    from multi_platform_deploy import deploy_to_all_platforms
    MULTI_DEPLOY_AVAILABLE = True
except ImportError:
    MULTI_DEPLOY_AVAILABLE = False

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
CENTRAL_HUB = Settings.SITE_BASE_URL

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
    prompt = get_website_metadata_prompt(name)

    result = ai.generate_json(prompt=prompt, max_tokens=1000, start_tier=3)

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
# WEB SEARCH RESEARCH
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
        # 1. Start with Implementation Resources (Free/APIs) - Get more results
        logger.info(f"  📚 Searching free implementation resources for: {topic}")
        # Search for more comprehensive results
        lib_results = search_client.search(f"how to implement {topic} javascript free open source library api", limit=10)
        if lib_results:
            research['libraries'] = [
                {'title': r.title, 'url': r.url, 'content': r.description[:200]}
                for r in lib_results
            ]
            logger.info(f"  ✅ Found {len(research['libraries'])} libraries")
        else:
            logger.warning(f"  ⚠️ No library results")

        # 2. Search for Advanced Core Extensions - Get more results
        logger.info(f"  ⭐ Searching advanced core extensions for: {topic}")
        feature_results = search_client.search(f"advanced {topic} algorithms implementation javascript free", limit=10)
        if feature_results:
            research['features'] = [
                {'title': r.title, 'content': r.description[:300]}
                for r in feature_results
            ]
            logger.info(f"  ✅ Found {len(research['features'])} feature sources")
        else:
            logger.warning(f"  ⚠️ No feature results")

        # 3. Search for Best Practices and Examples - Additional search
        logger.info(f"  🔧 Searching best practices for: {topic}")
        practice_results = search_client.search(f"{topic} best practices examples tutorial javascript", limit=8)
        if practice_results:
            research['best_practices'] = [
                {'title': r.title, 'content': r.description[:250]}
                for r in practice_results
            ]
            logger.info(f"  ✅ Found {len(research['best_practices'])} practice sources")
        else:
            logger.warning(f"  ⚠️ No practice results")

        # 4. Search for Existing Tools and Competitors - Market research
        logger.info(f"  🏆 Searching competitor analysis for: {topic}")
        competitor_results = search_client.search(f"online {topic} tool free website", limit=5)
        if competitor_results:
            research['examples'] = [
                {'title': r.title, 'url': r.url, 'content': r.description[:200]}
                for r in competitor_results
            ]
            logger.info(f"  ✅ Found {len(research['examples'])} competitor examples")
        else:
            logger.warning(f"  ⚠️ No competitor results")

        research['search_successful'] = True

    except Exception as e:
        logger.error(f"  ❌ Research failed: {e}")
        # Continue with empty research - the system will use fallback prompts

    return research


def format_research_context(research: dict) -> str:
    """Format research results into context for AI prompt."""
    if not research.get('search_successful'):
        return "No web research available - use general best practices."

    context_parts = []

    # Include discovered features first (most important)
    if research.get('features'):
        feature_text = "\n".join([f"  - {f['content'][:150]}..." for f in research['features'][:5] if f.get('content')])
        if feature_text:
            context_parts.append(f"COMPETITOR FEATURES (implement these):\n{feature_text}")

    if research.get('libraries'):
        libs = "\n".join([f"  - {l['title']}: {l['url']}" for l in research['libraries'][:5]])
        context_parts.append(f"RECOMMENDED LIBRARIES:\n{libs}")

    if research.get('best_practices'):
        practices = "\n".join([f"  - {p['title']}: {p['content'][:100]}..." for p in research['best_practices'][:5]])
        context_parts.append(f"IMPLEMENTATION GUIDES:\n{practices}")

    if research.get('examples'):
        examples = "\n".join([f"  - {e['title']}: {e['url']}" for e in research['examples'][:3]])
        context_parts.append(f"COMPETITOR EXAMPLES:\n{examples}")

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
9. PDF-LIB/WORKER SAFETY (CRITICAL):
   - Never pass complex objects (like PDFDocument) to Web Workers.
   - ONLY pass Serializable data (Uint8Array, ArrayBuffer, Strings, JSON).
   - When using `postMessage(data, [transferables])`, `transferables` MUST be an array of ArrayBuffer, MessagePort, or ImageBitmap.
   - If in doubt, omit the 2nd `transferables` argument: `postMessage(data)`.

Your output should be the EXACT PROMPT string I will paste to the coding AI.
Start with "Role: Expert..." and end with "...implementation."
"""

    # Use tier 4 (smaller models) to reserve largest for main generation
    result = ai.generate_with_tier(
        prompt=meta_prompt,
        max_tokens=2000,
        start_tier=4  # Use Tier 4+ models (100B-200B range) to save largest for main generation
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
  - MUST include in <head>: <script src="{CENTRAL_HUB}/universal/config.js"></script>
  - MUST include in <head>: <script src="{CENTRAL_HUB}/universal/core.js"></script>
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
- PDF/WORKER SAFETY:
  - DO NOT pass non-transferable types (like Objects/Functions) in the transfer list of `postMessage`.
  - CORRECT: `worker.postMessage({{ pdfData: arrayBuffer }}, [arrayBuffer])`
  - INCORRECT: `worker.postMessage(complextObject, [complexObject])` -> This causes CRASH.
  - If using PDF-lib, serialize to Uint8Array before sending to worker.
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
   - MUST include in <head>: <script src="{CENTRAL_HUB}/universal/config.js"></script>
   - MUST include in <head>: <script src="{CENTRAL_HUB}/universal/core.js"></script>
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
        min_model_size=400,  # Use 400B+ models (Tier 1 - largest available)
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
    category = tool.get("category", "Website")

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
# CONCURRENT POLYMORPHS GENERATION WITH FALLBACK STRATEGY
# =============================================================================

def generate_polymorphs_concurrent(tool: dict, ai: UnifiedAIClient, sidebar_models: list, main_html: str, max_workers: int = 8) -> dict:
    """
    Generate polymorphs for all sidebar models CONCURRENTLY with intelligent fallback.

    Strategy:
    1. Generate all polymorphs concurrently using ThreadPoolExecutor
    2. If a model fails, use the largest successful model as fallback
    3. Track which models succeeded/failed for transparency
    4. Return all files for the project repository

    Args:
        tool: Tool metadata dict
        ai: UnifiedAIClient instance
        sidebar_models: List of models to generate with
        main_html: Main HTML content as fallback
        max_workers: Maximum concurrent API calls

    Returns:
        dict: {
            "files": {"polymorphs/model-slug.html": content, ...},
            "successful_models": [model1, model2, ...],
            "failed_models": [model3, model4, ...],
            "fallback_used": "largest-model-name"
        }
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import time

    logger.info(f"  🚀 Starting concurrent generation with {max_workers} workers...")

    results = {
        "files": {},
        "successful_models": [],
        "failed_models": [],
        "fallback_used": None
    }

    # Find largest model for fallback
    largest_model = max(sidebar_models, key=lambda m: m.size_billions)

    def generate_single_polymorph(model_info):
        """Worker function to generate one polymorph."""
        idx, model = model_info
        slug = f"{model.name.lower().replace(' ', '-').replace('.', '-')}"

        try:
            logger.info(f"  [{idx}/{len(sidebar_models)}] Generating with {model.name} ({model.size_billions}B)...")

            # Generate with specific model
            result = ai._call_model(
                model=model,
                prompt=get_website_logic_prompt(tool["name"]) + f"\n\nTool metadata: {json.dumps(tool, indent=2)}",
                system_prompt="",
                max_tokens=32000,
                temperature=0.7,
                json_mode=False
            )

            if result.success:
                content = result.content

                # Extract HTML from markdown if needed
                if "```html" in content:
                    content = content.split("```html")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()

                # Inject enhancements using universal system
                enhanced_content = inject_all_enhancements(
                    content,
                    generate_software_schema(tool["name"], tool.get("title", tool["name"]), tool.get("description", ""), tool.get("keywords", []), CENTRAL_HUB),
                    generate_universal_integration(tool["name"])
                )

                logger.info(f"  ✅ [{idx}] Success: {model.name}")
                return model, slug, enhanced_content, True
            else:
                logger.warning(f"  ⚠️ [{idx}] Failed: {model.name} - {result.error}")
                return model, slug, None, False

        except Exception as e:
            logger.error(f"  ❌ [{idx}] Error: {model.name} - {e}")
            return model, slug, None, False

    # Execute concurrent generation
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = {
            executor.submit(generate_single_polymorph, (i, model)): model
            for i, model in enumerate(sidebar_models, 1)
        }

        # Collect results as they complete
        for future in as_completed(futures):
            model, slug, content, success = future.result()

            if success and content:
                results["files"][f"polymorphs/{slug}.html"] = content
                results["successful_models"].append(model)
            else:
                results["failed_models"].append(model)

    # Handle fallbacks for failed models
    if results["failed_models"]:
        logger.info(f"  🔄 Handling {len(results['failed_models'])} failed models with fallback strategy...")

        # Find the largest successful model for fallback
        fallback_content = main_html
        if results["successful_models"]:
            fallback_model = max(results["successful_models"], key=lambda m: m.size_billions)
            fallback_slug = f"{fallback_model.name.lower().replace(' ', '-').replace('.', '-')}"
            if f"polymorphs/{fallback_slug}.html" in results["files"]:
                fallback_content = results["files"][f"polymorphs/{fallback_slug}.html"]
                results["fallback_used"] = fallback_model.name

        # Create fallback files for failed models
        for failed_model in results["failed_models"]:
            failed_slug = f"{failed_model.name.lower().replace(' ', '-').replace('.', '-')}"

            # Add fallback indicator to content
            fallback_indicator = f"""
<!-- POLYMORPH FALLBACK NOTICE -->
<div id="polymorph-fallback-notice" style="
    position: fixed; top: 70px; right: 20px; z-index: 9999;
    background: rgba(255, 193, 7, 0.9); color: #000;
    padding: 10px 15px; border-radius: 8px; font-size: 0.8rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
">
    ⚠️ This polymorph uses fallback content from {results.get("fallback_used", "main")} model
    <button onclick="this.parentElement.remove()" style="margin-left: 10px; background: none; border: none; font-size: 1.2rem; cursor: pointer;">×</button>
</div>
"""

            fallback_with_notice = fallback_content.replace("</body>", f"{fallback_indicator}\n</body>")
            results["files"][f"polymorphs/{failed_slug}.html"] = fallback_with_notice

    elapsed = time.time() - start_time
    logger.info(f"  ⚡ Concurrent generation completed in {elapsed:.1f}s")
    logger.info(f"  ✅ Successful: {len(results['successful_models'])}")
    logger.info(f"  ⚠️ Failed (using fallback): {len(results['failed_models'])}")

    return results


def create_polymorphs_hub_structure(project_name: str, successful_models: list, failed_models: list) -> dict:
    """
    Create polymorphs hub structure files for the main hub repository.

    Creates /projects/{project-name}/polymorphs/ directory structure as requested.
    """
    hub_files = {}

    # Create polymorphs index for this project
    polymorphs_index = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name.title()} Polymorphs - AI Model Variants</title>
    <style>
        body {{ font-family: Inter, system-ui, sans-serif; background: #0a0a0a; color: #fff; margin: 0; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 40px; }}
        .models-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .model-card {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; }}
        .model-card.failed {{ opacity: 0.6; border-color: rgba(255,193,7,0.5); }}
        .model-name {{ font-size: 1.2rem; font-weight: 600; margin-bottom: 10px; }}
        .model-meta {{ font-size: 0.9rem; color: rgba(255,255,255,0.7); margin-bottom: 15px; }}
        .model-link {{ display: inline-block; background: #6366f1; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; }}
        .model-link:hover {{ background: #5855eb; }}
        .fallback-notice {{ background: rgba(255,193,7,0.1); border: 1px solid rgba(255,193,7,0.3); border-radius: 8px; padding: 15px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔮 {project_name.title()} Polymorphs</h1>
            <p>AI-generated variants using different models</p>
        </div>

        {f'<div class="fallback-notice">⚠️ Some models failed and are using fallback content from the largest successful model.</div>' if failed_models else ''}

        <div class="models-grid">
"""

    # Add successful models
    for model in successful_models:
        slug = f"{model.name.lower().replace(' ', '-').replace('.', '-')}"
        polymorphs_index += f"""
            <div class="model-card">
                <div class="model-name">{model.name}</div>
                <div class="model-meta">{model.size_billions}B parameters • {model.provider}</div>
                <a href="https://chirag127.github.io/{project_name}/polymorphs/{slug}.html" class="model-link">View Variant</a>
            </div>
"""

    # Add failed models with fallback notice
    for model in failed_models:
        slug = f"{model.name.lower().replace(' ', '-').replace('.', '-')}"
        polymorphs_index += f"""
            <div class="model-card failed">
                <div class="model-name">{model.name} (Fallback)</div>
                <div class="model-meta">{model.size_billions}B parameters • {model.provider} • Using fallback content</div>
                <a href="https://chirag127.github.io/{project_name}/polymorphs/{slug}.html" class="model-link">View Variant</a>
            </div>
"""

    polymorphs_index += """
        </div>
    </div>
</body>
</html>
"""

    hub_files[f"projects/{project_name}/polymorphs/index.html"] = polymorphs_index

    return hub_files


# =============================================================================
# GROWTHBOOK A/B TESTING INTEGRATION
# =============================================================================

def generate_universal_integration(project_name: str) -> str:
    """
    Generate integration script that uses the existing universal config system.

    This replaces the duplicate tracking functions and properly integrates with:
    - universal/config/tracking/* (existing analytics)
    - universal/config/engagement/ab_testing.js (existing GrowthBook config)
    - universal/config/* (all other modules)
    """
    return f"""
<!-- Universal Config Integration -->
<script src="/universal/config.js" type="module"></script>
<script src="/universal/core.js" type="module"></script>

<!-- GrowthBook Auto-Loading Script (Proper Implementation) -->
<script async
  data-client-key="sdk-BamkgvyjaSFKa0m6"
  src="https://cdn.jsdelivr.net/npm/@growthbook/growthbook/dist/bundles/auto.min.js">
</script>

<script type="module">
import {{ SITE_CONFIG, priorities }} from '/universal/config/index.js';

// Initialize Universal System for {project_name}
console.log('[Universal] Initializing for {project_name}');

// Project-specific configuration
const projectConfig = {{
    name: '{project_name}',
    type: 'tool',
    timestamp: new Date().toISOString(),

    // Enhanced user attributes for targeting
    userAttributes: {{
        id: localStorage.getItem('visitor_id') || 'anonymous_' + Math.random().toString(36).substr(2, 9),
        url: window.location.pathname,
        project: '{project_name}',
        device: /Mobile|Android|iPhone|iPad/.test(navigator.userAgent) ? 'mobile' : 'desktop',
        browser: navigator.userAgent.includes('Chrome') ? 'chrome' :
                navigator.userAgent.includes('Firefox') ? 'firefox' :
                navigator.userAgent.includes('Safari') ? 'safari' : 'other',
        screen_resolution: `${{screen.width}}x${{screen.height}}`,
        viewport_size: `${{window.innerWidth}}x${{window.innerHeight}}`,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        language: navigator.language
    }}
}};

// Store visitor ID for consistency
if (!localStorage.getItem('visitor_id')) {{
    localStorage.setItem('visitor_id', projectConfig.userAttributes.id);
}}

// Initialize all tracking systems using existing config
async function initializeTracking() {{
    const {{ tracking }} = SITE_CONFIG;

    // Initialize GA4 if enabled
    if (tracking.analytics_general.ga4.enabled) {{
        const ga4Config = tracking.analytics_general.ga4;

        // Load GA4 script
        const script = document.createElement('script');
        script.async = true;
        script.src = `https://www.googletagmanager.com/gtag/js?id=${{ga4Config.id}}`;
        document.head.appendChild(script);

        // Initialize gtag
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        window.gtag = gtag;
        gtag('js', new Date());
        gtag('config', ga4Config.id, {{
            custom_map: {{
                'custom_parameter_1': 'project_name',
                'custom_parameter_2': 'tool_category'
            }},
            project_name: '{project_name}',
            tool_category: 'utility'
        }});

        console.log('[Universal] GA4 initialized');
    }}

    // Initialize Clarity if enabled
    if (tracking.analytics_heatmaps.clarity.enabled) {{
        const clarityConfig = tracking.analytics_heatmaps.clarity;

        (function(c,l,a,r,i,t,y){{
            c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
            t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
            y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
        }})(window, document, "clarity", "script", clarityConfig.id);

        clarity('set', 'project', '{project_name}');
        console.log('[Universal] Clarity initialized');
    }}

    // Initialize Mixpanel if enabled
    if (tracking.analytics_general.mixpanel.enabled) {{
        const mixpanelConfig = tracking.analytics_general.mixpanel;

        (function(f,b){{if(!b.__SV){{var e,g,i,h;window.mixpanel=b;b._i=[];b.init=function(e,f,c){{function g(a,d){{var b=d.split(".");2==b.length&&(a=a[b[0]],d=b[1]);a[d]=function(){{a.push([d].concat(Array.prototype.slice.call(arguments,0)))}}}}var a=b;"undefined"!==typeof c?a=b[c]=[]:c="mixpanel";a.people=a.people||[];a.toString=function(a){{var d="mixpanel";"mixpanel"!==c&&(d+="."+c);a||(d+=" (stub)");return d}};a.people.toString=function(){{return a.toString(1)+".people (stub)"}};i="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");for(h=0;h<i.length;h++)g(a,i[h]);var j="set set_once union unset remove delete".split(" ");a.get_group=function(){{function b(c){{d[c]=function(){{call2_args=arguments;call2=[c].concat(Array.prototype.slice.call(call2_args,0));a.push([e,call2])}}}}for(var d={{}},e=["get_group"].concat(Array.prototype.slice.call(arguments,0)),c=0;c<j.length;c++)b(j[c]);return d}};b._i.push([e,f,c])}};b.__SV=1.7}})(document,window.mixpanel||[]);

        mixpanel.init(mixpanelConfig.token, {{
            debug: false,
            track_pageview: true,
            persistence: 'localStorage'
        }});

        mixpanel.track('Tool Loaded', {{
            'Tool Name': '{project_name}',
            'Category': 'utility',
            'URL': window.location.href
        }});

        console.log('[Universal] Mixpanel initialized');
    }}

    // Initialize other analytics platforms using existing config...
}}

// Initialize A/B Testing using existing GrowthBook config
async function initializeABTesting() {{
    const {{ engagement }} = SITE_CONFIG;
    const gbConfig = engagement.ab_testing.growthbook;

    if (!gbConfig.enabled) return;

    // Load GrowthBook SDK
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/@growthbook/growthbook@latest/dist/bundles/auto.min.js';
    document.head.appendChild(script);

    script.onload = async () => {{
        // Initialize GrowthBook with existing config
        const growthbook = new GrowthBook({{
            apiHost: gbConfig.apiHost,
            clientKey: gbConfig.clientKey,
            enableDevMode: gbConfig.enableDevMode,
            trackingCallback: (experiment, result) => {{
                // Use universal tracking function
                trackUniversalEvent('ab_test_view', {{
                    experiment_id: experiment.key,
                    variant_id: result.variationId,
                    project: '{project_name}'
                }});
            }}
        }});

        await growthbook.init({{ streaming: true }});
        growthbook.setAttributes(projectConfig.userAttributes);

        // Run comprehensive A/B tests
        runUniversalABTests(growthbook);

        console.log('[Universal] GrowthBook initialized');
    }};
}}

// Universal event tracking function that sends to all enabled platforms
function trackUniversalEvent(eventName, properties = {{}}) {{
    const eventData = {{
        ...properties,
        project: '{project_name}',
        timestamp: new Date().toISOString(),
        url: window.location.href
    }};

    // Track to GA4 if available
    if (typeof gtag !== 'undefined') {{
        gtag('event', eventName, eventData);
    }}

    // Track to Clarity if available
    if (typeof clarity !== 'undefined') {{
        clarity('event', eventName, eventData);
    }}

    // Track to Mixpanel if available
    if (typeof mixpanel !== 'undefined') {{
        mixpanel.track(eventName, eventData);
    }}

    console.log('[Universal Event]', eventName, eventData);
}}

// A/B testing using existing config
function runUniversalABTests(growthbook) {{
    // Button color test
    const buttonColorTest = growthbook.getFeatureValue('button_color_test', 'default');
    if (buttonColorTest !== 'default') {{
        document.querySelectorAll('button, .btn, input[type="submit"], [role="button"]').forEach(btn => {{
            switch(buttonColorTest) {{
                case 'variant_a':
                    btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                    btn.style.boxShadow = '0 8px 32px rgba(102, 126, 234, 0.4)';
                    break;
                case 'variant_b':
                    btn.style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
                    btn.style.boxShadow = '0 8px 32px rgba(240, 147, 251, 0.4)';
                    break;
                case 'variant_c':
                    btn.style.background = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
                    btn.style.boxShadow = '0 8px 32px rgba(79, 172, 254, 0.4)';
                    break;
            }}
        }});
    }}

    // Layout test
    const layoutTest = growthbook.getFeatureValue('layout_test', 'default');
    if (layoutTest === 'compact') {{
        document.body.style.fontSize = '0.9rem';
        document.body.style.lineHeight = '1.4';
    }} else if (layoutTest === 'spacious') {{
        document.body.style.fontSize = '1.1rem';
        document.body.style.lineHeight = '1.8';
    }}

    // CTA text test
    const ctaTest = growthbook.getFeatureValue('cta_text_test', 'default');
    if (ctaTest !== 'default') {{
        document.querySelectorAll('[data-cta], .cta, button').forEach(el => {{
            const originalText = el.textContent.trim();
            switch(ctaTest) {{
                case 'urgent':
                    el.textContent = originalText.replace(/Get|Start|Try|Download|Use/, 'Get Instant');
                    break;
                case 'benefit':
                    el.textContent = originalText.replace(/Get|Start|Try|Download|Use/, 'Unlock Free');
                    break;
            }}
        }});
    }}
}}

// Auto-track interactions using universal system
function setupUniversalTracking() {{
    // Track clicks
    document.addEventListener('click', (e) => {{
        const element = e.target;

        if (element.matches('button, .btn, input[type="submit"], [role="button"]')) {{
            trackUniversalEvent('button_click', {{
                element_text: element.textContent.trim().substring(0, 50),
                element_type: element.tagName.toLowerCase()
            }});
        }}

        if (element.matches('a[href*="download"], [data-download]')) {{
            trackUniversalEvent('download_click', {{
                element_text: element.textContent.trim(),
                href: element.href || 'none'
            }});
        }}
    }});

    // Track file uploads
    document.addEventListener('change', (e) => {{
        if (e.target.type === 'file' && e.target.files.length > 0) {{
            trackUniversalEvent('file_upload', {{
                file_count: e.target.files.length,
                file_types: Array.from(e.target.files).map(f => f.type).join(',')
            }});
        }}
    }});

    // Track engagement metrics
    let timeOnPage = 0;
    setInterval(() => {{
        timeOnPage += 15;
        if (timeOnPage === 30) trackUniversalEvent('engaged_30s');
        if (timeOnPage === 60) trackUniversalEvent('engaged_60s');
        if (timeOnPage === 120) trackUniversalEvent('engaged_2min');
    }}, 15000);

    // Track scroll depth
    let maxScroll = 0;
    window.addEventListener('scroll', () => {{
        const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
        if (scrollPercent > maxScroll) {{
            maxScroll = scrollPercent;
            if (maxScroll >= 25 && maxScroll < 50) trackUniversalEvent('scroll_25');
            if (maxScroll >= 50 && maxScroll < 75) trackUniversalEvent('scroll_50');
            if (maxScroll >= 75 && maxScroll < 90) trackUniversalEvent('scroll_75');
            if (maxScroll >= 90) trackUniversalEvent('scroll_90');
        }}
    }});
}}

// Initialize everything using the universal config system
document.addEventListener('DOMContentLoaded', async () => {{
    console.log('[Universal] Starting initialization for {project_name}');

    // Initialize in priority order
    await initializeTracking();
    await initializeABTesting();
    setupUniversalTracking();

    console.log('[Universal] All systems initialized for {project_name}');
}});
</script>
"""
    """
    Generate comprehensive GrowthBook A/B testing integration script.

    Features:
    - Automatic A/B testing for all elements
    - Conversion tracking (clicks, engagement, time on page)
    - Multi-armed bandit optimization
    - Client-side only (no backend required)
    """
    return f"""
<!-- GrowthBook A/B Testing Integration -->
<script src="https://cdn.jsdelivr.net/npm/@growthbook/growthbook@latest/dist/bundles/auto.min.js"></script>
<script>
// Initialize GrowthBook with comprehensive tracking
const growthbook = new GrowthBook({{
    apiHost: "https://cdn.growthbook.io",
    clientKey: "sdk-BamkgvyjaSFKa0m6",
    enableDevMode: true,
    trackingCallback: (experiment, result) => {{
        // Track to all analytics platforms
        if (typeof gtag !== 'undefined') {{
            gtag('event', 'ab_test_view', {{
                experiment_id: experiment.key,
                variant_id: result.variationId,
                project: '{project_name}'
            }});
        }}

        if (typeof clarity !== 'undefined') {{
            clarity('set', 'ab_test', `${{experiment.key}}_${{result.variationId}}`);
        }}

        console.log('[A/B Test]', experiment.key, 'variant:', result.variationId);
    }}
}});

// Wait for features to be available
growthbook.init({{ streaming: true }}).then(() => {{
    console.log('[GrowthBook] Initialized for {project_name}');

    // Set user attributes for targeting
    growthbook.setAttributes({{
        id: localStorage.getItem('visitor_id') || 'anonymous_' + Math.random().toString(36).substr(2, 9),
        url: window.location.pathname,
        project: '{project_name}',
        device: /Mobile|Android|iPhone|iPad/.test(navigator.userAgent) ? 'mobile' : 'desktop',
        browser: navigator.userAgent.includes('Chrome') ? 'chrome' :
                navigator.userAgent.includes('Firefox') ? 'firefox' :
                navigator.userAgent.includes('Safari') ? 'safari' : 'other'
    }});

    // A/B test everything automatically
    runComprehensiveABTests();
}});

function runComprehensiveABTests() {{
    // Test 1: Button colors and styles
    const buttonColorTest = growthbook.getFeatureValue('button_color_test', 'default');
    if (buttonColorTest !== 'default') {{
        document.querySelectorAll('button, .btn, input[type="submit"]').forEach(btn => {{
            switch(buttonColorTest) {{
                case 'variant_a':
                    btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                    break;
                case 'variant_b':
                    btn.style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
                    break;
                case 'variant_c':
                    btn.style.background = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
                    break;
            }}
        }});
    }}

    // Test 2: Layout variations
    const layoutTest = growthbook.getFeatureValue('layout_test', 'default');
    if (layoutTest === 'compact') {{
        document.body.style.fontSize = '0.9rem';
        document.body.style.lineHeight = '1.4';
    }} else if (layoutTest === 'spacious') {{
        document.body.style.fontSize = '1.1rem';
        document.body.style.lineHeight = '1.8';
    }}

    // Test 3: Call-to-action text
    const ctaTest = growthbook.getFeatureValue('cta_text_test', 'default');
    if (ctaTest !== 'default') {{
        document.querySelectorAll('[data-cta]').forEach(el => {{
            switch(ctaTest) {{
                case 'urgent':
                    el.textContent = el.textContent.replace(/Get|Start|Try/, 'Get Instant');
                    break;
                case 'benefit':
                    el.textContent = el.textContent.replace(/Get|Start|Try/, 'Unlock Free');
                    break;
            }}
        }});
    }}

    // Test 4: Color scheme variations
    const colorSchemeTest = growthbook.getFeatureValue('color_scheme_test', 'default');
    if (colorSchemeTest !== 'default') {{
        const root = document.documentElement;
        switch(colorSchemeTest) {{
            case 'warm':
                root.style.setProperty('--primary-color', '#ff6b6b');
                root.style.setProperty('--secondary-color', '#feca57');
                break;
            case 'cool':
                root.style.setProperty('--primary-color', '#3742fa');
                root.style.setProperty('--secondary-color', '#2ed573');
                break;
            case 'monochrome':
                root.style.setProperty('--primary-color', '#2f3542');
                root.style.setProperty('--secondary-color', '#57606f');
                break;
        }}
    }}
}}

// Conversion tracking
function trackConversion(event, value = 1) {{
    growthbook.track(event, {{ value, project: '{project_name}' }});

    // Also track to other analytics
    if (typeof gtag !== 'undefined') {{
        gtag('event', 'conversion', {{
            event_category: 'ab_test',
            event_label: event,
            value: value,
            project: '{project_name}'
        }});
    }}
}}

// Auto-track common conversions
document.addEventListener('click', (e) => {{
    if (e.target.matches('button, .btn, input[type="submit"], a[href*="download"]')) {{
        trackConversion('button_click');
    }}
    if (e.target.matches('a[href^="mailto:"], a[href^="tel:"]')) {{
        trackConversion('contact_click');
    }}
}});

// Track time on page
let timeOnPage = 0;
setInterval(() => {{
    timeOnPage += 10;
    if (timeOnPage === 30) trackConversion('engaged_30s');
    if (timeOnPage === 60) trackConversion('engaged_60s');
    if (timeOnPage === 120) trackConversion('engaged_2min');
}}, 10000);

// Track scroll depth
let maxScroll = 0;
window.addEventListener('scroll', () => {{
    const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
    if (scrollPercent > maxScroll) {{
        maxScroll = scrollPercent;
        if (maxScroll >= 25 && maxScroll < 50) trackConversion('scroll_25');
        if (maxScroll >= 50 && maxScroll < 75) trackConversion('scroll_50');
        if (maxScroll >= 75 && maxScroll < 90) trackConversion('scroll_75');
        if (maxScroll >= 90) trackConversion('scroll_90');
    }}
}});
</script>
"""


# =============================================================================
# COMPREHENSIVE TRACKING INTEGRATION
# =============================================================================

def generate_comprehensive_tracking(tool: dict) -> str:
    """
    Generate comprehensive tracking integration for all analytics platforms.

    Includes:
    - Google Analytics 4 (GA4)
    - Microsoft Clarity
    - Mixpanel
    - Amplitude
    - PostHog
    - Heap Analytics
    - Custom event tracking
    """
    project_name = tool["name"]
    title = tool.get("title", project_name)
    category = tool.get("category", "Utilities")

    return f"""
<!-- Comprehensive Analytics & Tracking Integration -->

<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){{dataLayer.push(arguments);}}
gtag('js', new Date());
gtag('config', 'G-XXXXXXXXXX', {{
    custom_map: {{
        'custom_parameter_1': 'project_name',
        'custom_parameter_2': 'tool_category'
    }},
    project_name: '{project_name}',
    tool_category: '{category}'
}});

// Enhanced ecommerce tracking for tool usage
gtag('event', 'page_view', {{
    page_title: '{title}',
    page_location: window.location.href,
    content_group1: '{category}',
    content_group2: '{project_name}'
}});
</script>

<!-- Microsoft Clarity -->
<script type="text/javascript">
(function(c,l,a,r,i,t,y){{
    c[a]=c[a]||function(){{(c[a].q=c[a].q||[]).push(arguments)}};
    t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
    y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
}})(window, document, "clarity", "script", "XXXXXXXXX");

clarity('set', 'project', '{project_name}');
clarity('set', 'category', '{category}');
</script>

<!-- Mixpanel -->
<script type="text/javascript">
(function(f,b){{if(!b.__SV){{var e,g,i,h;window.mixpanel=b;b._i=[];b.init=function(e,f,c){{function g(a,d){{var b=d.split(".");2==b.length&&(a=a[b[0]],d=b[1]);a[d]=function(){{a.push([d].concat(Array.prototype.slice.call(arguments,0)))}}}}var a=b;"undefined"!==typeof c?a=b[c]=[]:c="mixpanel";a.people=a.people||[];a.toString=function(a){{var d="mixpanel";"mixpanel"!==c&&(d+="."+c);a||(d+=" (stub)");return d}};a.people.toString=function(){{return a.toString(1)+".people (stub)"}};i="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");for(h=0;h<i.length;h++)g(a,i[h]);var j="set set_once union unset remove delete".split(" ");a.get_group=function(){{function b(c){{d[c]=function(){{call2_args=arguments;call2=[c].concat(Array.prototype.slice.call(call2_args,0));a.push([e,call2])}}}}for(var d={{}},e=["get_group"].concat(Array.prototype.slice.call(arguments,0)),c=0;c<j.length;c++)b(j[c]);return d}};b._i.push([e,f,c])}};b.__SV=1.7}})(document,window.mixpanel||[]);

mixpanel.init('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', {{
    debug: false,
    track_pageview: true,
    persistence: 'localStorage'
}});

mixpanel.track('Tool Loaded', {{
    'Tool Name': '{project_name}',
    'Tool Title': '{title}',
    'Category': '{category}',
    'URL': window.location.href
}});
</script>

<!-- PostHog -->
<script>
!function(t,e){{var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){{function g(t,e){{var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]);t[e]=function(){{t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){{var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e}},u.people.toString=function(){{return u.toString(1)+".people (stub)"}},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])}},e.__SV=1)}}(document,window.posthog||[]);
posthog.init('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX', {{api_host: 'https://app.posthog.com'}});

posthog.capture('tool_loaded', {{
    tool_name: '{project_name}',
    tool_title: '{title}',
    category: '{category}'
}});
</script>

<!-- Custom Event Tracking System -->
<script>
// Unified event tracking function
function trackEvent(eventName, properties = {{}}) {{
    const eventData = {{
        ...properties,
        project: '{project_name}',
        category: '{category}',
        timestamp: new Date().toISOString(),
        url: window.location.href,
        user_agent: navigator.userAgent,
        screen_resolution: `${{screen.width}}x${{screen.height}}`,
        viewport_size: `${{window.innerWidth}}x${{window.innerHeight}}`
    }};

    // Track to all platforms
    if (typeof gtag !== 'undefined') {{
        gtag('event', eventName, eventData);
    }}

    if (typeof clarity !== 'undefined') {{
        clarity('event', eventName, eventData);
    }}

    if (typeof mixpanel !== 'undefined') {{
        mixpanel.track(eventName, eventData);
    }}

    if (typeof posthog !== 'undefined') {{
        posthog.capture(eventName, eventData);
    }}

    console.log('[Analytics]', eventName, eventData);
}}

// Auto-track common interactions
document.addEventListener('DOMContentLoaded', function() {{
    // Track file uploads
    document.querySelectorAll('input[type="file"]').forEach(input => {{
        input.addEventListener('change', (e) => {{
            if (e.target.files.length > 0) {{
                trackEvent('file_uploaded', {{
                    file_count: e.target.files.length,
                    file_types: Array.from(e.target.files).map(f => f.type).join(',')
                }});
            }}
        }});
    }});

    // Track downloads
    document.querySelectorAll('a[download], button[data-download]').forEach(el => {{
        el.addEventListener('click', () => {{
            trackEvent('file_downloaded', {{
                element_type: el.tagName.toLowerCase(),
                element_text: el.textContent.trim()
            }});
        }});
    }});

    // Track form submissions
    document.querySelectorAll('form').forEach(form => {{
        form.addEventListener('submit', (e) => {{
            trackEvent('form_submitted', {{
                form_id: form.id || 'unnamed',
                form_action: form.action || 'none'
            }});
        }});
    }});

    // Track tool usage (processing buttons)
    document.querySelectorAll('button[data-action], .process-btn, .convert-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
            trackEvent('tool_used', {{
                action: btn.dataset.action || btn.textContent.trim(),
                button_text: btn.textContent.trim()
            }});
        }});
    }});

    // Track errors
    window.addEventListener('error', (e) => {{
        trackEvent('javascript_error', {{
            error_message: e.message,
            error_filename: e.filename,
            error_line: e.lineno,
            error_column: e.colno
        }});
    }});

    // Track performance metrics
    window.addEventListener('load', () => {{
        setTimeout(() => {{
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {{
                trackEvent('page_performance', {{
                    load_time: Math.round(perfData.loadEventEnd - perfData.fetchStart),
                    dom_content_loaded: Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart),
                    first_paint: Math.round(performance.getEntriesByType('paint')[0]?.startTime || 0)
                }});
            }}
        }}, 1000);
    }});
}});

// Track engagement metrics
let engagementStartTime = Date.now();
let isEngaged = true;

// Track when user becomes inactive
document.addEventListener('visibilitychange', () => {{
    if (document.hidden) {{
        if (isEngaged) {{
            const engagementTime = Date.now() - engagementStartTime;
            trackEvent('engagement_session', {{
                duration_seconds: Math.round(engagementTime / 1000),
                session_type: 'active'
            }});
            isEngaged = false;
        }}
    }} else {{
        engagementStartTime = Date.now();
        isEngaged = true;
    }}
}});

// Track before page unload
window.addEventListener('beforeunload', () => {{
    if (isEngaged) {{
        const engagementTime = Date.now() - engagementStartTime;
        trackEvent('engagement_session', {{
            duration_seconds: Math.round(engagementTime / 1000),
            session_type: 'final'
        }});
    }}
}});
</script>
"""


# =============================================================================
# ENHANCED HTML INJECTION SYSTEM
# =============================================================================

def inject_all_enhancements(html_content: str, schema_html: str, universal_script: str) -> str:
    """
    Inject all enhancements into HTML content using the universal config system.

    Order:
    1. Schema and meta tags in <head>
    2. Universal config integration (replaces separate tracking/AB testing)
    3. Service Worker registration before </body>
    """
    enhanced_html = html_content

    # 1. Inject schema and manifest in <head>
    if "</head>" in enhanced_html:
        head_injection = f"{schema_html}\n<link rel=\"manifest\" href=\"manifest.json\">\n"
        enhanced_html = enhanced_html.replace("</head>", f"{head_injection}</head>")

    # 2. Inject Universal integration and SW registration before </body>
    sw_script = f"""
<script>
if ('serviceWorker' in navigator) {{
  window.addEventListener('load', () => {{
    navigator.serviceWorker.register('{CENTRAL_HUB}/sw.js', {{ scope: '/' }})
      .then(reg => console.log('[PWA] ServiceWorker registered'))
      .catch(err => console.log('[PWA] ServiceWorker failed', err));
  }});
}}
</script>
"""

    if "</body>" in enhanced_html:
        body_injection = f"{universal_script}\n{sw_script}\n"
        enhanced_html = enhanced_html.replace("</body>", f"{body_injection}</body>")

    return enhanced_html


def generate_pwa_manifest(tool: dict) -> str:
    """Generate PWA manifest with enhanced metadata."""
    manifest = {
        "name": tool.get("title", tool["name"]),
        "short_name": tool["name"],
        "description": tool.get("description", ""),
        "start_url": "./index.html",
        "display": "standalone",
        "background_color": "#0a0a0a",
        "theme_color": "#007bff",
        "categories": [tool.get("category", "utilities").lower()],
        "icons": [
            {
                "src": f"{CENTRAL_HUB}/universal/icons/icon-192.png",
                "sizes": "192x192",
                "type": "image/png"
            },
            {
                "src": f"{CENTRAL_HUB}/universal/icons/icon-512.png",
                "sizes": "512x512",
                "type": "image/png"
            }
        ],
        "shortcuts": [
            {
                "name": f"Open {tool.get('title', tool['name'])}",
                "short_name": "Open Tool",
                "description": f"Quick access to {tool.get('title', tool['name'])}",
                "url": "./index.html",
                "icons": [{"src": f"{CENTRAL_HUB}/universal/icons/icon-192.png", "sizes": "192x192"}]
            }
        ]
    }

    return json.dumps(manifest, indent=2)


# =============================================================================
# MAIN GENERATION FLOW
# =============================================================================

def generate_tool_concurrent(tool: dict, ai: UnifiedAIClient, state: dict, search_client: WebSearchClient = None, multiverse: bool = False) -> bool:
    """Generate a tool with AI using concurrent polymorphs generation and comprehensive A/B testing.

    Args:
        tool: Tool metadata dict
        ai: UnifiedAIClient instance
        state: State dict for caching
        search_client: Optional WebSearchClient for research
        multiverse: If True, generate multiverse variants concurrently
    """
    logger.info(f"\n{'='*50}")
    logger.info(f"Generating: {tool['name']} (CONCURRENT + A/B TESTING)")
    if multiverse:
        logger.info("POLYMORPHS MODE ENABLED - CONCURRENT GENERATION")
    logger.info(f"{'='*50}")

    # Generate metadata first
    metadata = generate_tool_metadata(tool["name"], ai, state)
    tool.update(metadata)

    if not create_repo(tool["name"], tool["description"]):
        return False

    # Get all sidebar models for concurrent generation
    sidebar_models = []
    if multiverse and POLYMORPHS_AVAILABLE:
        try:
            from src.ai.models import get_sidebar_enabled_models
            sidebar_models = get_sidebar_enabled_models()
            logger.info(f"  🔮 Found {len(sidebar_models)} sidebar models for concurrent generation")
        except ImportError:
            logger.warning("  ⚠️ Could not import sidebar models, falling back to single generation")

    # Generate main HTML with largest model (fallback for failed polymorphs)
    logger.info("  🚀 Generating main HTML with largest model...")
    main_html_content = generate_single_html(tool, ai, search_client)

    # Enhanced Universal Integration (replaces separate GrowthBook + tracking)
    universal_script = generate_universal_integration(tool["name"])

    # Generate SEO Schema
    schema_html = generate_software_schema(
        name=tool["name"],
        title=tool.get("title", tool["name"]),
        description=tool.get("description", ""),
        keywords=tool.get("keywords", []),
        base_url=CENTRAL_HUB
    )

    # Inject all enhancements into main HTML using universal system
    enhanced_html = inject_all_enhancements(
        main_html_content,
        schema_html,
        universal_script
    )

    files = {
        "index.html": enhanced_html,
        "README.md": generate_comprehensive_readme(tool),
        "manifest.json": generate_pwa_manifest(tool)
    }

    # CONCURRENT POLYMORPHS GENERATION
    if multiverse and sidebar_models:
        logger.info(f"\n  🔮 CONCURRENT Polymorphs Generation ({len(sidebar_models)} models)...")

        # Generate polymorphs concurrently with fallback strategy
        polymorphs_results = generate_polymorphs_concurrent(
            tool=tool,
            ai=ai,
            sidebar_models=sidebar_models,
            main_html=enhanced_html,
            max_workers=8  # Concurrent API calls
        )

        # Add successful polymorphs to files
        files.update(polymorphs_results["files"])

        # Create polymorphs directory structure in main hub repo
        polymorphs_hub_files = create_polymorphs_hub_structure(
            tool["name"],
            polymorphs_results["successful_models"],
            polymorphs_results["failed_models"]
        )
        files.update(polymorphs_hub_files)

        logger.info(f"  ✅ Generated {len(polymorphs_results['files'])} polymorphs")
        logger.info(f"  ⚠️ Failed: {len(polymorphs_results['failed_models'])} (using fallback)")

    logger.info(f"  📝 Writing {len(files)} files...")
    if not git_push(tool["name"], files):
        return False

    time.sleep(2)
    enable_pages(tool["name"])

    # Deploy to other platforms if enabled
    if MULTI_DEPLOY_AVAILABLE:
        logger.info("\n  🌐 Multi-Platform Deployment...")
        try:
            deploy_to_all_platforms(TEMP_DIR, tool["name"])
        except Exception as e:
            logger.error(f"  ❌ Multi-platform deploy failed: {e}")

    # Set GitHub topics from keywords
    topics = tool.get("keywords", []) + [tool.get("category", "").lower()]
    set_github_topics(tool["name"], topics)

    if tool["name"] not in state["generated"]:
        state["generated"].append(tool["name"])
    save_state(state)

    logger.info(f"\n✅ Complete: {CENTRAL_HUB}/{tool['name']}/")
    return True


# Keep original function for backward compatibility
def generate_tool(tool: dict, ai: UnifiedAIClient, state: dict, search_client: WebSearchClient = None, multiverse: bool = False) -> bool:
    """Legacy function - redirects to concurrent version."""
    return generate_tool_concurrent(tool, ai, state, search_client, multiverse)


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
    """Main entry point for tool generation with enhanced concurrent polymorphs and A/B testing."""
    if not GH_TOKEN:
        logger.error("Error: GH_TOKEN not set")
        sys.exit(1)

    args = sys.argv[1:]
    state = load_state()

    # Enhanced polymorphs mode (Enabled by default with concurrency)
    multiverse_mode = True
    concurrent_workers = 8  # Default concurrent API calls

    if "--no-multiverse" in args:
        multiverse_mode = False

    if "--workers" in args:
        idx = args.index("--workers")
        if idx + 1 < len(args):
            try:
                concurrent_workers = int(args[idx + 1])
                logger.info(f"🚀 Using {concurrent_workers} concurrent workers")
            except ValueError:
                logger.warning("Invalid workers value, using default: 8")

    if multiverse_mode:
        if POLYMORPHS_AVAILABLE:
            logger.info("🔮 ENHANCED POLYMORPHS MODE: Concurrent generation with A/B testing enabled")
            logger.info(f"⚡ Concurrent workers: {concurrent_workers}")
        else:
            logger.warning("⚠️ Polymorphs module not available, falling back to standard mode")
            multiverse_mode = False

    # Initialize AI client
    ai = UnifiedAIClient()

    # Initialize Web Search client
    search_client = WebSearchClient()
    logger.info("🔍 Web Search Client: INITIALIZED")

    if "--status" in args:
        show_status()
        return

    tools = parse_tools()

    if "--website" in args:
        idx = args.index("--website")
        if idx + 1 < len(args):
            name = args[idx + 1]
            tool = next((t for t in tools if t["name"] == name), None)
            if tool:
                logger.info(f"🎯 Generating single project: {name}")
                generate_tool_concurrent(tool, ai, state, search_client, multiverse=multiverse_mode)
            else:
                logger.error(f"Tool not found: {name}")
        return

    if "--all" in args:
        remaining = [t for t in tools if t["name"] not in state["generated"]]
        logger.info(f"🚀 Generating ALL remaining projects ({len(remaining)}) with concurrent polymorphs")

        for i, tool in enumerate(remaining, 1):
            logger.info(f"\n{'='*60}")
            logger.info(f"BATCH PROGRESS: {i}/{len(remaining)}")
            logger.info(f"{'='*60}")

            generate_tool_concurrent(tool, ai, state, search_client, multiverse=multiverse_mode)

            # Brief pause between projects to avoid rate limits
            if i < len(remaining):
                logger.info("⏳ Brief pause between projects...")
                time.sleep(5)

        logger.info(f"\n🎉 BATCH COMPLETE: Generated {len(remaining)} projects with polymorphs!")
        return

    # Default: generate next tool with enhanced features
    for tool in tools:
        if tool["name"] not in state["generated"]:
            logger.info("🚀 Generating next project with enhanced concurrent polymorphs...")
            generate_tool_concurrent(tool, ai, state, search_client, multiverse=multiverse_mode)
            return

    logger.info("✅ All tools generated!")


if __name__ == "__main__":
    main()
