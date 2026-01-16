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
# GENERATE SINGLE HTML FILE
# =============================================================================

def generate_single_html(tool: dict, ai: UnifiedAIClient) -> str:
    """Generate complete single-file HTML using template and AI."""

    name = tool["name"]
    title = tool["title"]
    desc = tool["description"]
    features = tool["features"]
    keywords = tool["keywords"]
    url = f"{CENTRAL_HUB}/{name}/"

    # 1. Load Template
    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file not found at {TEMPLATE_FILE}")
        return f"<h1>Error: Template not found at {TEMPLATE_FILE}</h1>"

    template = TEMPLATE_FILE.read_text(encoding="utf-8")

    # 2. AI Prompt for Tool Logic
    prompt = f"""You are an Expert Frontend Developer.

TASK: Write JavaScript logic (and optional CSS) for: "{title}"

DESCRIPTION: {desc}
FEATURES: {', '.join(features)}

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
3. Process files CLIENT-SIDE ONLY.
4. Show progress in statusArea.
5. Display results in resultsContent.
6. Use CSS variables: var(--primary), var(--bg-card).

OUTPUT JSON:
{{
  "js": "/* Pure JS code */",
  "css": "/* Optional CSS */"
}}"""

    print(f"  Generating logic for {name}...")
    result = ai.generate_json(prompt=prompt, max_tokens=8000, min_model_size=32)

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

def generate_tool(tool: dict, ai: UnifiedAIClient, state: dict) -> bool:
    print(f"\n{'='*50}")
    print(f"Generating: {tool['name']}")
    print(f"{'='*50}")

    # Generate metadata first
    metadata = generate_tool_metadata(tool["name"], ai, state)
    tool.update(metadata)

    if not create_repo(tool["name"], tool["description"]):
        return False

    html_content = generate_single_html(tool, ai)

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

    print(f"  Writing {len(files)} files...")
    if not git_push(tool["name"], files):
        return False

    time.sleep(2)
    enable_pages(tool["name"])

    if tool["name"] not in state["generated"]:
        state["generated"].append(tool["name"])
    save_state(state)

    print(f"\n+ Complete: {CENTRAL_HUB}/{tool['name']}/")
    return True


def show_status():
    tools = parse_tools()
    state = load_state()
    done = len(state["generated"])
    cached = len(state.get("metadata_cache", {}))
    print(f"\n{'='*50}")
    print(f"Progress: {done}/{len(tools)} ({done/len(tools)*100:.0f}%)")
    print(f"Remaining: {len(tools) - done}")
    print(f"Cached Metadata: {cached}")
    print(f"{'='*50}")


def main():
    if not GH_TOKEN:
        print("Error: GH_TOKEN not set")
        sys.exit(1)

    args = sys.argv[1:]
    state = load_state()
    ai = UnifiedAIClient()

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
                generate_tool(tool, ai, state)
            else:
                print(f"Tool not found: {name}")
        return

    if "--all" in args:
        remaining = [t for t in tools if t["name"] not in state["generated"]]
        for tool in remaining:
            generate_tool(tool, ai, state)
            time.sleep(5)
        return

    # Default: generate next tool
    for tool in tools:
        if tool["name"] not in state["generated"]:
            generate_tool(tool, ai, state)
            return

    print("All tools generated!")


if __name__ == "__main__":
    main()
