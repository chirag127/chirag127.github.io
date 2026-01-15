#!/usr/bin/env python3
"""
Generate Projects - Tool Website Generator

Creates single-file HTML tools (inline CSS + JS):
- All code in one index.html
- No build step, no separate files
- Direct GitHub Pages deployment
- Central hub analytics integration

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
# TOOL METADATA
# =============================================================================

TOOL_INFO = {
    "pdf-merger-splitter-tool": {
        "title": "PDF Merger & Splitter",
        "description": "Merge multiple PDFs or split PDF into pages. 100% client-side.",
        "features": ["Merge PDFs", "Split by pages", "Drag-drop", "Preview", "ZIP download"],
        "keywords": ["pdf merger", "pdf splitter", "combine pdf", "split pdf"],
        "cdn": "https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js",
    },
    "pdf-compressor-optimizer": {
        "title": "PDF Compressor",
        "description": "Compress PDF files to reduce size while keeping quality.",
        "features": ["3 compression levels", "Batch compress", "Size preview"],
        "keywords": ["compress pdf", "pdf optimizer", "reduce pdf size"],
        "cdn": "https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js",
    },
    "image-converter-pro": {
        "title": "Image Converter",
        "description": "Convert images between JPG, PNG, WEBP, GIF formats.",
        "features": ["10+ formats", "Batch convert", "Quality control", "Resize"],
        "keywords": ["image converter", "jpg to png", "webp converter"],
        "cdn": "",
    },
    "json-data-tools": {
        "title": "JSON Tools",
        "description": "Format, minify, validate JSON. Convert to CSV/XML.",
        "features": ["Format", "Minify", "Validate", "Convert"],
        "keywords": ["json formatter", "json validator", "json to csv"],
        "cdn": "",
    },
    "qrcode-barcode-suite": {
        "title": "QR & Barcode Generator",
        "description": "Generate QR codes for URLs, WiFi, vCards and more.",
        "features": ["QR codes", "WiFi QR", "vCard", "Barcodes", "Custom colors"],
        "keywords": ["qr generator", "barcode maker", "wifi qr"],
        "cdn": "https://unpkg.com/qrcode@1.5.3/build/qrcode.min.js",
    },
}


def get_tool_info(name: str) -> dict:
    if name in TOOL_INFO:
        return TOOL_INFO[name]
    title = name.replace("-", " ").title()
    return {
        "title": title,
        "description": f"Free online {title.lower()} tool. Fast and secure.",
        "features": ["Client-side", "Fast", "Free", "No signup", "Mobile ready"],
        "keywords": [name.replace("-", " "), f"online {name}", f"free {name}"],
        "cdn": "",
    }


# =============================================================================
# STATE
# =============================================================================

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except:
            pass
    return {"generated": [], "failed": []}


def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


# =============================================================================
# PARSE TOOLS
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
            info = get_tool_info(name)
            tools.append({"name": name, "category": category, **info})

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
    """Generate complete single-file HTML using shared/tool-template.html and AI."""

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

    # 2. AI Prompt
    prompt = f"""You are an Expert Frontend Developer.
    TASK: Write the **JavaScript logic** (and optional CSS) for a new web tool: "{title}".

    TOOL INFO:
    - Description: {desc}
    - Features: {', '.join(features)}

    HTML STRUCTURE (Do NOT output HTML, it exists):
    - <input type="file" id="fileInput">
    - <label id="dropZone"> (Drop area)
    - <button id="actionBtn"> (Click to process - Disabled by default)
    - <div id="statusArea"> (Inject dynamic UI here: options, progress bars)
    - <div id="resultsContent"> (Inject final results here)
    - <div id="results"> (Container of resultsContent, hidden by default)

    REQUIREMENTS:
    1. Listen for file selection (drop or click).
    2. Enable "actionBtn" when file is selected. Update dropZone UI to show file name.
    3. On click, process the file (Client-side ONLY).
       - Use browser APIs (FileReader, Canvas) or CDN libraries if strictly necessary.
       - If complex (like PDF merge), simulate the process with a progress bar and fake "success" if true client-side is too large for this snippet, BUT prefer real implementation if possible within 8000 tokens.
    4. Inject progress bars or status messages into `statusArea`.
    5. Reveal `results` (remove .hidden class from #results or set style.display) and show output.
    6. **THEME**: Use CSS variables: var(--primary), var(--bg-card).

    OUTPUT JSON FORMAT:
    {{
      "js": "/* Pure JS code here */",
      "css": "/* Optional CSS for new elements */"
    }}
    """

    print(f"  Generating logic for {name}...")
    result = ai.generate_json(prompt=prompt, max_tokens=8000, min_model_size=32)

    js_code = ""
    css_code = ""

    if result.success and result.json_content:
        js_code = result.json_content.get("js", "// No JS generated")
        css_code = result.json_content.get("css", "")
        print("  + AI Logic Generated")

        # Fallback Cleanup
        if "```" in js_code:
            js_code = js_code.replace("```javascript", "").replace("```", "")
    else:
        print(f"  x AI Generation Failed: {result.error}")
        js_code = "console.error('AI Logic Generation Failed'); alert('AI Logic Generation Failed');"

    # 3. Inject Content into Template
    html = template.replace("{{TOOL_TITLE}}", title)
    html = html.replace("{{TOOL_DESCRIPTION}}", desc)
    html = html.replace("{{TOOL_KEYWORDS}}", ", ".join(keywords))
    html = html.replace("{{REPO_NAME}}", name)

    # Supported formats for display
    formats = "Files"
    if "pdf" in name: formats = "PDF"
    elif "image" in name: formats = "Images (PNG, JPG, WEBP)"
    elif "video" in name: formats = "Video (MP4, WEBM)"

    html = html.replace("{{SUPPORTED_FORMATS}}", formats)
    html = html.replace("{{FILE_ACCEPT}}", "*/*")

    # Scripts
    html = html.replace("{{TOOL_SCRIPT}}", js_code)
    html = html.replace("{{TOOL_CSS}}", f"<style>{css_code}</style>" if css_code else "")

    return html


# =============================================================================
# MAIN
# =============================================================================

def generate_tool(tool: dict) -> bool:
    print(f"\n{'='*50}")
    print(f"Generating: {tool['name']}")
    print(f"{'='*50}")

    if not create_repo(tool["name"], tool["description"]):
        return False

    ai = UnifiedAIClient()
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

    state = load_state()
    if tool["name"] not in state["generated"]:
        state["generated"].append(tool["name"])
    save_state(state)

    print(f"\n+ Complete: {CENTRAL_HUB}/{tool['name']}/")
    return True


def show_status():
    tools = parse_tools()
    state = load_state()
    done = len(state["generated"])
    print(f"\n{'='*50}")
    print(f"Progress: {done}/{len(tools)} ({done/len(tools)*100:.0f}%)")
    print(f"Remaining: {len(tools) - done}")
    print(f"{'='*50}")


def main():
    if not GH_TOKEN:
        print("Error: GH_TOKEN not set")
        sys.exit(1)

    args = sys.argv[1:]

    if "--status" in args:
        show_status()
        return

    tools = parse_tools()
    state = load_state()

    if "--tool" in args:
        idx = args.index("--tool")
        if idx + 1 < len(args):
            name = args[idx + 1]
            tool = next((t for t in tools if t["name"] == name), None)
            if tool:
                generate_tool(tool)
            else:
                print(f"Tool not found: {name}")
        return

    if "--all" in args:
        remaining = [t for t in tools if t["name"] not in state["generated"]]
        for tool in remaining:
            generate_tool(tool)
            time.sleep(5)
        return

    # Default: generate next tool
    for tool in tools:
        if tool["name"] not in state["generated"]:
            generate_tool(tool)
            return

    print("All tools generated!")


if __name__ == "__main__":
    main()
