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
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent))

from apex_optimizer.ai.unified_client import UnifiedAIClient
from apex_optimizer.prompts import get_tool_metadata_prompt
from apex_optimizer.clients.searxng import SearXNGClient

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

ROOT = Path(__file__).parent
TOOLS_FILE = ROOT / "ar.txt"
STATE_FILE = ROOT / "state" / "tools_generated.json"
TEMP_DIR = ROOT / ".temp"
TEMPLATE_FILE = ROOT / "shared" / "tool-template.html"

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

def research_tool(name: str, search_client: SearXNGClient) -> dict:
    """
    Research libraries, features, and best practices for a tool using SearXNG.

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

    try:
        # 1. Find JavaScript libraries
        logger.info(f"  📚 Searching libraries for: {topic}")
        lib_results = search_client.find_libraries(topic, max_results=8)
        if lib_results:
            research['libraries'] = [
                {'title': r.get('title', ''), 'url': r.get('url', ''), 'content': r.get('content', '')[:200]}
                for r in lib_results[:5]
            ]
            logger.info(f"  ✅ Found {len(research['libraries'])} libraries")
        else:
            logger.warning(f"  ⚠️ No library results")

        # 2. Search for FEATURES from competitors
        logger.info(f"  ⭐ Searching features for: {topic}")
        feature_results = search_client.search(
            f"best {topic} tool features what can it do",
            categories=['general'],
            max_results=10
        )
        if feature_results:
            research['features'] = [
                {'title': r.get('title', ''), 'content': r.get('content', '')[:300]}
                for r in feature_results[:5]
            ]
            logger.info(f"  ✅ Found {len(research['features'])} feature sources")
        else:
            logger.warning(f"  ⚠️ No feature results")

        # 3. How to build tutorials
        logger.info(f"  📖 Searching tutorials for: {topic}")
        how_to = search_client.research_how_to_build(topic, max_results=8)
        if how_to:
            research['best_practices'] = [
                {'title': r.get('title', ''), 'url': r.get('url', ''), 'content': r.get('content', '')[:200]}
                for r in how_to[:5]
            ]
            logger.info(f"  ✅ Found {len(research['best_practices'])} tutorials")
        else:
            logger.warning(f"  ⚠️ No tutorial results")

        # 4. Existing examples
        logger.info(f"  🔎 Searching examples for: {topic}")
        examples = search_client.search(
            f"{topic} javascript github example",
            categories=['it'],
            max_results=5
        )
        if examples:
            research['examples'] = [
                {'title': r.get('title', ''), 'url': r.get('url', '')}
                for r in examples[:3]
            ]
            logger.info(f"  ✅ Found {len(research['examples'])} examples")

        research['search_successful'] = bool(lib_results or how_to or examples or feature_results)

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
# GENERATE SINGLE HTML FILE
# =============================================================================

def generate_single_html(tool: dict, ai: UnifiedAIClient, search_client: SearXNGClient = None) -> str:
    """Generate complete single-file HTML using template and AI with web research."""

    name = tool["name"]
    title = tool["title"]
    desc = tool["description"]
    features = tool["features"]
    keywords = tool["keywords"]
    url = f"{CENTRAL_HUB}/{name}/"

    # 0. Research best practices via web search
    research_context = ""
    if search_client:
        research = research_tool(name, search_client)
        research_context = format_research_context(research)
        logger.info(f"  📋 Research context generated: {len(research_context)} chars")

    # 1. Load Template
    if not TEMPLATE_FILE.exists():
        logger.error(f"Template file not found at {TEMPLATE_FILE}")
        return f"<h1>Error: Template not found at {TEMPLATE_FILE}</h1>"

    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    # 2. AI Prompt for Tool Logic (Enhanced with Web Research)
    prompt = f"""You are an Expert Frontend Developer (Jan 2026 Standards).

TASK: Write production-ready JavaScript for: "{title}"

DESCRIPTION: {desc}
FEATURES: {', '.join(features)}

{research_context}

HTML ELEMENTS (Already exist in template):
- <input type="file" id="fileInput"> (Hidden file input)
- <label id="dropZone"> (Drag-drop area, triggers fileInput)
- <button id="actionBtn"> (Main action button - disabled by default)
- <div id="statusArea"> (Progress, options, file list display)
- <div id="resultsContent"> (Output display)
- <div id="results" class="hidden"> (Results container)

REQUIREMENTS (CRITICAL):
1. ALL PROCESSING MUST BE CLIENT-SIDE (no fetch to external APIs unless research suggests specific library CDNs)
2. Use EVENT DELEGATION on document.addEventListener('DOMContentLoaded', ...)
3. Handle drag-drop on dropZone (dragover, dragleave, drop events)
4. Show file names in statusArea when files are selected
5. Enable actionBtn only when valid files are selected
6. Show progress percentage during processing
7. Display downloadable results in resultsContent
8. Use CSS variables: var(--primary), var(--bg-card), var(--success), var(--text-main)
9. Include necessary library CDN in a comment at top if needed (pdf-lib, jszip, etc.)
10. Clean error handling with try/catch

UI/UX (2026 Standards):
- Kinetic feedback on button clicks (scale transform)
- Smooth transitions (0.3s ease)
- Progress bars with gradient background
- File list with remove buttons

OUTPUT FORMAT (JSON only, no markdown):
{{
  "js": "/* Complete JavaScript code with all event handlers */",
  "css": "/* Optional additional CSS for custom elements */"
}}"""

    print(f"  Generating logic for {name}...")
    # Use 70B+ models for complex tool logic generation
    result = ai.generate_json(prompt=prompt, max_tokens=8000, min_model_size=70)

    js_code = ""
    css_code = ""

    if result.success and result.json_content:
        js_code = result.json_content.get("js", "// No JS generated")
        css_code = result.json_content.get("css", "")
        print("  + AI Logic Generated")

        # Clean up markdown artifacts
        if "```" in js_code:
            js_code = js_code.replace("```javascript", "").replace("```", "")

        # CRITICAL: Escape </script> to prevent premature script tag closure
        # This is a common issue when AI generates comments mentioning script tags
        js_code = js_code.replace("</script>", "<\\/script>")
        js_code = js_code.replace("</Script>", "<\\/Script>")
        js_code = js_code.replace("</SCRIPT>", "<\\/SCRIPT>")

        # Also escape in CSS if present
        if css_code:
            css_code = css_code.replace("</style>", "<\\/style>")
    else:
        print(f"  x AI Generation Failed: {result.error}")
        js_code = "console.error('AI Logic Generation Failed'); alert('Logic generation failed');"

    # 3. Inject Content into Template
    html = template.replace("{{TOOL_TITLE}}", title)
    html = html.replace("{{TOOL_DESCRIPTION}}", desc)
    html = html.replace("{{TOOL_KEYWORDS}}", ", ".join(keywords))
    html = html.replace("{{REPO_NAME}}", name)

    # Format hints
    formats = "Files"
    if "pdf" in name: formats = "PDF"
    elif "image" in name: formats = "Images (PNG, JPG, WEBP)"
    elif "video" in name: formats = "Video (MP4, WEBM)"

    html = html.replace("{{SUPPORTED_FORMATS}}", formats)
    html = html.replace("{{FILE_ACCEPT}}", "*/*")
    html = html.replace("{{TOOL_SCRIPT}}", js_code)
    html = html.replace("{{TOOL_CSS}}", f"<style>{css_code}</style>" if css_code else "")

    return html


# =============================================================================
# MAIN GENERATION FLOW
# =============================================================================

def generate_tool(tool: dict, ai: UnifiedAIClient, state: dict, search_client: SearXNGClient = None) -> bool:
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

    # Initialize SearXNG client for web research
    search_client = SearXNGClient()

    # Test SearXNG availability
    if search_client.is_available():
        logger.info("🔍 SearXNG search: AVAILABLE")
    else:
        logger.warning("⚠️ SearXNG search: UNAVAILABLE (will use AI only)")
        search_client = None

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
