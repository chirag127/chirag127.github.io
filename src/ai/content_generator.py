"""
Apex Content Generator - Generates production-ready project content.

ARCHITECTURE:
- Web apps → Deploy directly (no separate docs/ site)
- Non-web (extensions, mobile, desktop) → Generate Vite landing page
- ALL projects → Load from central hub chirag127.github.io

CENTRAL HUB (chirag127.github.io/shared/):
- analytics.js - 10 trackers (GA4, Yandex, Clarity, etc.)
- monetization.js - A-Ads, BMC widgets
- profile.json - Author data
- header.html, footer.html - Shared components
"""

import logging
from typing import Any

from src.ai.unified_client import UnifiedAIClient
from src.core.monetization import MONETIZATION

logger = logging.getLogger("ApexContentGenerator")


# =============================================================================
# CENTRAL HUB CONFIGURATION
# =============================================================================

CENTRAL_HUB = "https://chirag127.github.io"
SHARED_ANALYTICS = f"{CENTRAL_HUB}/shared/analytics.js"
SHARED_MONETIZATION = f"{CENTRAL_HUB}/shared/monetization.js"
SHARED_PROFILE = f"{CENTRAL_HUB}/shared/profile.json"


# =============================================================================
# PROJECT CATEGORIES
# =============================================================================

# Web apps - Deploy directly, no separate landing page needed
WEB_CATEGORIES = {
    "web_app", "webapp", "spa", "pwa", "dashboard", "landing_page",
    "portfolio", "frontend", "static_site", "react_app", "vue_app",
    "nextjs_app", "astro_app", "svelte_app", "vite_app",
}

# Non-web - Need a separate landing page built with Vite
NONWEB_CATEGORIES = {
    "chrome_extension", "browser_extension", "firefox_extension",
    "mobile_app", "android_app", "ios_app", "react_native_app",
    "flutter_app", "desktop_app", "electron_app", "tauri_app",
    "cli_tool", "library", "package", "api", "backend",
    "python_package", "npm_package", "rust_crate",
}


class ApexContentGenerator:
    """
    Generates project content with smart deployment strategy.

    - Web projects: Client-side only, load from central hub
    - Non-web projects: Generate Vite landing page via GitHub Actions
    """

    def __init__(self, ai_client: UnifiedAIClient):
        self.ai = ai_client
        self.monetization = MONETIZATION

    def generate_from_repo_name(self, repo_name: str) -> dict[str, str]:
        """
        Generate all project content from just the repository name.

        This is the simplified entry point that derives everything automatically:
        1. Uses AI to infer title, description, features, keywords, category from name
        2. Generates complete project files based on inferred metadata

        Args:
            repo_name: The repository name (e.g., "pdf-merge", "image-resize")

        Returns:
            Dict of filepath -> content
        """
        from src.ai.prompts import get_repo_name_only_prompt

        logger.info(f"🧠 Generating from repo name only: {repo_name}")

        # Step 1: Derive metadata from repository name using AI
        prompt = get_repo_name_only_prompt(repo_name)
        result = self.ai.generate_json(
            prompt=prompt,
            system_prompt="You are the Apex Technical Authority. Output only valid JSON.",
            max_tokens=2000,
            min_model_size=32,  # Use 32B+ for better inference
        )

        if result.success and result.json_content:
            metadata = result.json_content
            title = metadata.get("title", repo_name.replace("-", " ").title())
            description = metadata.get("description", f"A tool for {repo_name.replace('-', ' ')}")
            category = metadata.get("category", "utility")
            features = metadata.get("features", ["Fast", "Free", "Privacy-focused"])
            keywords = metadata.get("keywords", [repo_name])

            logger.info(f"   📋 Inferred: {title} ({category})")
            logger.info(f"   📝 Features: {features[:3]}...")

            # Step 2: Generate project content using inferred metadata
            return self.generate_project_content(
                idea=title,
                description=description,
                category=category,
                tags=keywords + features[:5],
            )
        else:
            logger.warning(f"⚠️ Metadata inference failed: {result.error}")
            # Fallback: use repo name directly
            title = repo_name.replace("-", " ").title()
            return self.generate_project_content(
                idea=title,
                description=f"A {title.lower()} tool",
                category="utility",
                tags=[repo_name],
            )

    def generate_project_content(
        self,
        idea: str,
        description: str,
        category: str,
        tags: list[str],
    ) -> dict[str, str]:
        """
        Generate file map for a project.

        Returns:
            Dict of filepath -> content
        """
        is_web = category.lower() in WEB_CATEGORIES
        logger.info(f"🧠 Generating content for: {idea} (web={is_web})")

        files = {}

        # 1. Core project files
        files.update(self._generate_core_files(idea, description, category, tags))

        # 2. Deployment workflow (GitHub Actions)
        if is_web:
            # Web app: Deploy the app itself to GitHub Pages
            files[".github/workflows/deploy.yml"] = self._get_webapp_deploy_workflow()
        else:
            # Non-web: Generate Vite landing page and deploy
            files[".github/workflows/deploy.yml"] = self._get_vite_landing_deploy_workflow()
            files.update(self._generate_landing_page_files(idea, description, tags))

        logger.info(f"   📝 Generated {len(files)} files")
        return files

    def _generate_core_files(
        self,
        idea: str,
        description: str,
        category: str,
        tags: list[str],
    ) -> dict[str, str]:
        """Generate core project files using AI."""

        prompt = f"""
Generate core project files for:
PROJECT: {idea}
DESCRIPTION: {description}
CATEGORY: {category}
TAGS: {", ".join(tags[:15])}

REQUIREMENTS:
1. Client-side only (NO backend servers)
2. Use modern tech (TypeScript, Vite, React if needed)
3. Production-ready, working code

CRITICAL - CENTRAL HUB INTEGRATION:
For ALL HTML files, include these scripts:
- <script src="{SHARED_ANALYTICS}" defer></script>
- <script src="{SHARED_MONETIZATION}" defer></script>

DO NOT include any analytics codes directly - they load from central hub.

FILE MAP TO GENERATE:
- README.md (with badges, features, usage)
- package.json or pyproject.toml
- .gitignore
- src/ folder with actual code
- LICENSE (MIT)

OUTPUT: Pure JSON object with file paths as keys and content as values.
"""

        result = self.ai.generate_json(
            prompt=prompt,
            system_prompt="You are a senior engineer generating production code.",
            max_tokens=16000,
            min_model_size=32,
        )

        if result.success and result.json_content:
            return result.json_content

        logger.warning(f"⚠️ AI generation failed: {result.error}")
        return self._get_fallback_core_files(idea, description)

    def _generate_landing_page_files(
        self,
        idea: str,
        description: str,
        tags: list[str],
    ) -> dict[str, str]:
        """Generate Vite landing page for non-web projects."""

        # Generate a minimal Vite React landing page
        return {
            "landing/package.json": f'''{{
  "name": "{idea.lower().replace(" ", "-")}-landing",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }},
  "dependencies": {{
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }},
  "devDependencies": {{
    "@vitejs/plugin-react": "^4.3.4",
    "vite": "^6.1.0"
  }}
}}''',

            "landing/vite.config.js": f'''import {{ defineConfig }} from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({{
  plugins: [react()],
  base: '/{idea.lower().replace(" ", "-")}/',
  build: {{
    outDir: 'dist',
  }},
}})
''',

            "landing/index.html": f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{idea} - Free Tool by Chirag Singhal</title>
  <meta name="description" content="{description[:160]}">
  <script src="{SHARED_ANALYTICS}" defer></script>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
  <script src="{SHARED_MONETIZATION}" defer></script>
</body>
</html>
''',

            "landing/src/main.jsx": '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
''',

            "landing/src/App.jsx": f'''import React from 'react'

export default function App() {{
  return (
    <div className="app">
      <header className="hero">
        <h1>{idea}</h1>
        <p>{description}</p>
        <div className="buttons">
          <a href="https://github.com/chirag127/{idea.lower().replace(" ", "-")}" className="btn-primary">
            GitHub
          </a>
          <a href="https://buymeacoffee.com/chirag127" className="btn-secondary">
            ☕ Support
          </a>
        </div>
      </header>

      <section className="features">
        <h2>Features</h2>
        <div className="grid">
          <div className="card">
            <h3>🚀 Fast</h3>
            <p>Optimized for performance</p>
          </div>
          <div className="card">
            <h3>🔒 Private</h3>
            <p>Your data stays local</p>
          </div>
          <div className="card">
            <h3>🆓 Free</h3>
            <p>Open source and free forever</p>
          </div>
        </div>
      </section>

      <footer>
        <p>© 2026 Chirag Singhal | <a href="https://github.com/chirag127">GitHub</a></p>
      </footer>
    </div>
  )
}}
''',

            "landing/src/index.css": '''* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --bg: #0f172a; --text: #f8fafc; --accent: #0ea5e9; }
body { font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; }
.app { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.hero { text-align: center; padding: 4rem 0; }
.hero h1 { font-size: 3rem; background: linear-gradient(135deg, #0ea5e9, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero p { margin: 1rem 0 2rem; color: #94a3b8; font-size: 1.2rem; }
.buttons { display: flex; gap: 1rem; justify-content: center; }
.btn-primary, .btn-secondary { padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; }
.btn-primary { background: linear-gradient(135deg, #0ea5e9, #6366f1); color: white; }
.btn-secondary { background: rgba(255,255,255,0.1); color: white; border: 1px solid rgba(255,255,255,0.2); }
.features { margin: 4rem 0; }
.features h2 { text-align: center; margin-bottom: 2rem; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
.card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 1.5rem; }
.card h3 { margin-bottom: 0.5rem; }
.card p { color: #94a3b8; }
footer { text-align: center; padding: 2rem 0; color: #64748b; }
footer a { color: var(--accent); text-decoration: none; }
''',
        }

    def _get_webapp_deploy_workflow(self) -> str:
        """GitHub Actions workflow for web app deployment."""
        return f'''name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
'''

    def _get_vite_landing_deploy_workflow(self) -> str:
        """GitHub Actions workflow for Vite landing page deployment."""
        return f'''name: Deploy Landing Page

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        working-directory: ./landing
        run: npm install

      - name: Build
        working-directory: ./landing
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './landing/dist'

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{{{ steps.deployment.outputs.page_url }}}}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
'''

    def _get_fallback_core_files(self, idea: str, description: str) -> dict[str, str]:
        """Fallback files if AI generation fails."""
        repo_name = idea.lower().replace(" ", "-")

        return {
            "README.md": f'''# {idea}

{description}

## Features
- 🚀 Fast and lightweight
- 🔒 Privacy-focused
- 🆓 Free and open source

## Installation
```bash
npm install
npm run dev
```

## Author
**Chirag Singhal** - Software Engineer

[![GitHub](https://img.shields.io/github/followers/chirag127?style=social)](https://github.com/chirag127)
[![Buy Me A Coffee](https://img.shields.io/badge/-Buy%20Me%20A%20Coffee-orange?logo=buy-me-a-coffee)](https://buymeacoffee.com/chirag127)

## License
MIT © 2026 Chirag Singhal
''',
            ".gitignore": '''node_modules/
dist/
.env
.env.local
*.log
.DS_Store
''',
            "LICENSE": f'''MIT License

Copyright (c) 2026 Chirag Singhal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
''',
        }
