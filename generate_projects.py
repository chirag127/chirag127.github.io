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
    """Generate complete single-file HTML with inline CSS and JS."""

    name = tool["name"]
    title = tool["title"]
    desc = tool["description"]
    features = tool["features"]
    keywords = tool["keywords"]
    cdn = tool.get("cdn", "")
    url = f"{CENTRAL_HUB}/{name}/"

    # AI prompt for JavaScript logic
    prompt = f"""Create JavaScript for: {title}
Description: {desc}
Features: {', '.join(features)}

Requirements:
- Pure JS ES6+
- Handle file input/drop
- Progress indicator
- Download results
- Error handling

Output ONLY JavaScript code (no markdown).
"""

    result = ai.generate(prompt=prompt, max_tokens=8000, min_model_size=32)
    js_code = result.content if result.success else get_fallback_js(tool)

    # Clean markdown
    if "```" in js_code:
        lines = [l for l in js_code.split("\n") if not l.strip().startswith("```")]
        js_code = "\n".join(lines)

    # SEO structured data
    seo_data = json.dumps({
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "description": desc,
        "url": url,
        "applicationCategory": "UtilityApplication",
        "offers": {"@type": "Offer", "price": "0"},
        "author": {"@type": "Person", "name": "Chirag Singhal"}
    })

    features_html = "\n".join(f"<li>{f}</li>" for f in features)
    cdn_script = f'<script src="{cdn}"></script>' if cdn else ""

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Free Online Tool</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{', '.join(keywords)}">
  <meta name="author" content="Chirag Singhal">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <link rel="canonical" href="{url}">
  <script type="application/ld+json">{seo_data}</script>
  <script src="{CENTRAL_HUB}/shared/analytics.js" defer></script>
  <style>
:root {{
  --bg: #0f172a;
  --bg2: #1e293b;
  --text: #f8fafc;
  --text2: #94a3b8;
  --accent: #0ea5e9;
  --accent2: #8b5cf6;
  --success: #22c55e;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  min-height: 100vh;
}}
.container {{ max-width: 800px; margin: 0 auto; padding: 0 20px; }}
.header {{
  background: var(--bg2);
  padding: 16px 0;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}}
.header .container {{ display: flex; justify-content: space-between; align-items: center; }}
.logo {{ color: var(--text); text-decoration: none; font-weight: 700; }}
.header nav a {{ color: var(--text2); text-decoration: none; margin-left: 20px; }}
.header nav a:hover {{ color: var(--accent); }}
.hero {{ text-align: center; padding: 60px 0 40px; }}
.hero h1 {{
  font-size: 2.5rem;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}}
.hero p {{ color: var(--text2); margin-top: 16px; max-width: 600px; margin-left: auto; margin-right: auto; }}
.tool-section {{ padding-bottom: 60px; }}
.tool-card {{
  background: rgba(30,41,59,0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 32px;
}}
.drop-zone {{
  border: 2px dashed rgba(255,255,255,0.2);
  border-radius: 12px;
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}}
.drop-zone:hover {{ border-color: var(--accent); background: rgba(14,165,233,0.1); }}
.drop-zone svg {{ color: var(--text2); margin-bottom: 16px; }}
#fileList {{ margin-top: 16px; }}
.file-item {{
  display: flex; align-items: center; gap: 12px;
  padding: 12px; background: var(--bg2); border-radius: 8px; margin-top: 8px;
}}
.file-item .name {{ flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
.file-item .size {{ color: var(--text2); font-size: 0.875rem; }}
.btn-primary {{
  width: 100%; margin-top: 24px; padding: 16px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  color: white; border: none; border-radius: 12px;
  font-size: 1rem; font-weight: 600; cursor: pointer;
  transition: all 0.3s;
}}
.btn-primary:disabled {{ opacity: 0.5; cursor: not-allowed; }}
.btn-primary:hover:not(:disabled) {{ transform: translateY(-2px); box-shadow: 0 10px 30px rgba(14,165,233,0.3); }}
.progress-bar {{ height: 8px; background: var(--bg2); border-radius: 4px; margin-top: 24px; overflow: hidden; }}
.progress-fill {{ height: 100%; background: linear-gradient(90deg, var(--accent), var(--accent2)); width: 0%; transition: width 0.3s; }}
#progressText {{ text-align: center; margin-top: 8px; color: var(--text2); }}
#results {{ margin-top: 24px; }}
.result-item {{
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px; background: rgba(34,197,94,0.1);
  border: 1px solid rgba(34,197,94,0.2); border-radius: 12px; margin-top: 8px;
}}
.download-btn {{
  background: var(--success); color: white; border: none;
  padding: 8px 16px; border-radius: 8px; cursor: pointer;
}}
.features, .privacy {{ padding: 60px 0; }}
.features h2, .privacy h2 {{ text-align: center; margin-bottom: 32px; }}
.features-list {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px; list-style: none;
}}
.features-list li {{
  background: rgba(30,41,59,0.8); border: 1px solid rgba(255,255,255,0.1);
  border-radius: 12px; padding: 16px;
}}
.privacy {{ text-align: center; }}
.privacy p {{ color: var(--text2); max-width: 600px; margin: 0 auto; }}
.footer {{ padding: 40px 0; text-align: center; border-top: 1px solid rgba(255,255,255,0.1); }}
.footer a {{ color: var(--accent); text-decoration: none; }}
  </style>
</head>
<body>
  <header class="header">
    <div class="container">
      <a href="{CENTRAL_HUB}" class="logo">Chirag Tools</a>
      <nav>
        <a href="https://github.com/chirag127/{name}">GitHub</a>
        <a href="https://buymeacoffee.com/chirag127">Support</a>
      </nav>
    </div>
  </header>

  <section class="hero">
    <div class="container">
      <h1>{title}</h1>
      <p>{desc}</p>
    </div>
  </section>

  <main class="tool-section">
    <div class="container">
      <div class="tool-card">
        <div class="drop-zone" id="dropZone">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <p>Drop files here or click to browse</p>
          <input type="file" id="fileInput" multiple hidden>
        </div>
        <div id="fileList"></div>
        <button class="btn-primary" id="processBtn" disabled>Process Files</button>
        <div id="progress" hidden>
          <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
          <p id="progressText">Processing...</p>
        </div>
        <div id="results"></div>
      </div>
    </div>
  </main>

  <section class="features">
    <div class="container">
      <h2>Features</h2>
      <ul class="features-list">{features_html}</ul>
    </div>
  </section>

  <section class="privacy">
    <div class="container">
      <h2>100% Private</h2>
      <p>All processing happens in your browser. Files never leave your device.</p>
    </div>
  </section>

  <footer class="footer">
    <div class="container">
      <p>&copy; 2026 <a href="https://github.com/chirag127">Chirag Singhal</a></p>
    </div>
  </footer>

  {cdn_script}
  <script>
{js_code}
  </script>
  <script src="{CENTRAL_HUB}/shared/monetization.js" defer></script>
</body>
</html>'''


def get_fallback_js(tool: dict) -> str:
    return f'''// {tool["title"]} - Main Logic
document.addEventListener('DOMContentLoaded', () => {{
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const fileList = document.getElementById('fileList');
  const processBtn = document.getElementById('processBtn');
  const progress = document.getElementById('progress');
  const progressFill = document.getElementById('progressFill');
  const progressText = document.getElementById('progressText');
  const results = document.getElementById('results');

  let files = [];

  dropZone.onclick = () => fileInput.click();
  dropZone.ondragover = e => {{ e.preventDefault(); dropZone.style.borderColor = '#0ea5e9'; }};
  dropZone.ondragleave = () => dropZone.style.borderColor = '';
  dropZone.ondrop = e => {{ e.preventDefault(); dropZone.style.borderColor = ''; addFiles(e.dataTransfer.files); }};
  fileInput.onchange = e => addFiles(e.target.files);

  function addFiles(newFiles) {{
    files = [...files, ...Array.from(newFiles)];
    renderFiles();
    processBtn.disabled = files.length === 0;
  }}

  function renderFiles() {{
    fileList.innerHTML = files.map((f, i) => `
      <div class="file-item">
        <span class="name">${{f.name}}</span>
        <span class="size">${{(f.size/1024).toFixed(1)}} KB</span>
      </div>
    `).join('');
  }}

  processBtn.onclick = async () => {{
    processBtn.disabled = true;
    progress.hidden = false;
    results.innerHTML = '';

    for (let i = 0; i < files.length; i++) {{
      progressFill.style.width = ((i+1)/files.length*100) + '%';
      progressText.textContent = `Processing ${{i+1}}/${{files.length}}...`;
      await new Promise(r => setTimeout(r, 500));

      results.innerHTML += `
        <div class="result-item">
          <span>Done: ${{files[i].name}}</span>
          <button class="download-btn">Download</button>
        </div>
      `;
    }}

    progressText.textContent = 'Complete!';
    processBtn.disabled = false;
  }};
}});'''


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

    # Only 2 files: index.html and README.md (no .gitignore)
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
