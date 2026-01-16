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
        # 1. Find JavaScript libraries
        logger.info(f"  📚 Searching libraries for: {topic}")
        # WebSearchClient.search returns list of SearchResult objects
        lib_results = search_client.search(f"best javascript libraries for {topic}", limit=5)
        if lib_results:
            research['libraries'] = [
                {'title': r.title, 'url': r.url, 'content': r.description[:200]}
                for r in lib_results
            ]
            logger.info(f"  ✅ Found {len(research['libraries'])} libraries")
        else:
            logger.warning(f"  ⚠️ No library results")

        # 2. Search for FEATURES from competitors
        logger.info(f"  ⭐ Searching features for: {topic}")
        feature_results = search_client.search(f"best {topic} tool features list", limit=5)
        if feature_results:
            research['features'] = [
                {'title': r.title, 'content': r.description[:300]}
                for r in feature_results
            ]
            logger.info(f"  ✅ Found {len(research['features'])} feature sources")
        else:
            logger.warning(f"  ⚠️ No feature results")

        # 3. How to build tutorials
        logger.info(f"  📖 Searching tutorials for: {topic}")
        how_to = search_client.search(f"how to build {topic} with javascript tutorial", limit=5)
        if how_to:
            research['best_practices'] = [
                {'title': r.title, 'url': r.url, 'content': r.description[:200]}
                for r in how_to
            ]
            logger.info(f"  ✅ Found {len(research['best_practices'])} tutorials")
        else:
            logger.warning(f"  ⚠️ No tutorial results")

        # 4. Existing examples
        logger.info(f"  🔎 Searching examples for: {topic}")
        examples = search_client.search(f"{topic} javascript github example", limit=3)
        if examples:
            research['examples'] = [
                {'title': r.title, 'url': r.url}
                for r in examples
            ]
            logger.info(f"  ✅ Found {len(research['examples'])} examples")

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
    """
    logger.info("  ✨ Optimizing Instruction Sets...")

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
4. Critical Constraints (No Headers, Single File, Config Injection).

Your output should be the EXACT PROMPT string I will paste to the coding AI.
Start with "Role: Expert..." and end with "...implementation."
"""

    result = ai.generate(
        prompt=meta_prompt,
        max_tokens=2000,
        min_model_size=70 # Use a smart model for planning
    )

    if result.success:
        logger.info("  ✨ Prompt Optimized.")
        return result.content
    else:
        logger.warning(f"  ⚠️ Prompt Optimization Failed: {result.error}")
        return "" # Fallback to default


def generate_single_html(tool: dict, ai: UnifiedAIClient, search_client: WebSearchClient = None) -> str:
    """
    Generate a SINGLE-FILE tool (HTML+CSS+JS) using the Generative UI Engine.
    Uses AGENTS.md as the system prompt (Apex Technical Authority).
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

    # 2. PROMPT OPTIMIZATION (New Step)
    optimized_instructions = optimize_prompt(tool, research_context, agents_context, ai)

    # 3. Construct The Final Prompt
    if optimized_instructions:
        # Use the optimized instructions as the core
        prompt = f"""
SYSTEM INSTRUCTION: IMPLEMENT THE FOLLOWING SPECIFICATION EXACTLY.

{optimized_instructions}

CRITICAL OVERRIDE:
- OUTPUT: A SINGLE `index.html` file containing ALL HTML, CSS, and JavaScript.
- UNIVERSAL ARCHITECTURE:
  - MUST include in <head>: <script src="https://chirag127.github.io/universal/config.js"></script>
  - MUST include in <head>: <script src="https://chirag127.github.io/universal/core.js"></script>
  - DO NOT generate <header> or <footer>.
  - Wrap content in <main>.
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
3. LIBRARY SELECTION (THE MENU):
   - Consult "12. APEX APPROVED CLIENT-SIDE ENGINES" in the System Context.
   - For PDF tools, you MUST use `PDF-lib` or `pdf-merger-js`.
   - For Video tools, you MUST use `FFmpeg.wasm`.
   - LOAD LIBRARIES VIA CDN (cdnjs/unpkg).
4. CONFIGURATION: Use `window.SITE_CONFIG` for any external service keys.
5. AESTHETICS: **Apex 2026 Spatial-Adaptive**.
   - "Spatial Glass" look (backdrop-filter: blur).
   - "Bento Grid" layouts.
6. LOGIC: Robust, error-handled JavaScript (IIFE).
7. FORMAT: Return ONLY the HTML code block within ```html flags.
"""

    logger.info(f"  🧠 Generative UI Engine engaged for {tool['name']}...")

    # 3. Generate Content (Using Large Model)
    result = ai.generate(
        prompt=prompt,
        system_prompt=agents_context,
        max_tokens=20000, # Large buffer for full file
        min_model_size=70,
        temperature=0.7
    )

    if not result.success:
        logger.error(f"AI Generation Failed: {result.error}")
        return f"<h1>Generation Failed</h1><p>{result.error}</p>"

    # 4. Extract Code
    content = result.content
    if "```html" in content:
        content = content.split("```html")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()

    logger.info(f"  ✅ Generated {len(content)} bytes of HTML")
    return content


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
        "README.md": f'''# {tool["title"]}

{tool["description"]}

## Live Demo

**[{CENTRAL_HUB}/{tool["name"]}/]({CENTRAL_HUB}/{tool["name"]}/)**

## Features

{chr(10).join(f"- {f}" for f in tool["features"])}

## Privacy

All processing happens in your browser. Your files never leave your device.

## Author

**Chirag Singhal** - [GitHub](https://github.com/chirag127) | [Support](https://buymeacoffee.com/chirag127)
''',
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
