"""
Repository Factory - Creates new private GitHub repositories.

Features:
- Private repository creation
- AGENTS.md-compliant structure (Dec 2025)
- APEX Naming convention enforcement
- Jules session integration
"""

import logging
import re

import requests

from src.core.config import Settings

logger = logging.getLogger("RepositoryFactory")


class RepositoryFactory:
    """
    Creates new private GitHub repositories for trending ideas.

    All repos are created as PRIVATE by default for manual review.
    Follows AGENTS.md Dec 2025 naming and structure conventions.
    """

    def __init__(self, config: Settings):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {config.GH_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        self.base_url = "https://api.github.com"

    def create_repository(
        self,
        name: str,
        description: str,
        topics: list[str] | None = None,
        is_private: bool = True
    ) -> dict | None:
        """
        Create a new GitHub repository.

        Args:
            name: Repository name (will be normalized to APEX convention)
            description: Repository description (max 300 chars)
            topics: Optional list of topics
            is_private: Create as private (default: True)

        Returns:
            Repository data dict or None if failed
        """
        # Normalize name to APEX convention
        repo_name = self._normalize_repo_name(name)

        # Truncate description to GitHub limit (350 chars)
        if description and len(description) > 350:
            description = description[:347] + "..."

        data = {
            "name": repo_name,
            "description": description,
            "private": is_private,
            "auto_init": True,  # Create with README
            "has_issues": True,
            "has_projects": True,
            "has_wiki": False,
        }

        try:
            response = self.session.post(
                f"{self.base_url}/user/repos",
                json=data,
                timeout=30
            )

            if response.status_code == 201:
                repo_data = response.json()
                logger.info(f"✅ Created repository: {repo_name} (private={is_private})")

                # Add topics if provided
                if topics:
                    self._set_topics(repo_name, topics)

                return repo_data

            elif response.status_code == 422:
                # Repo already exists
                logger.warning(f"⚠️ Repository {repo_name} already exists")
                return None

            else:
                logger.error(f"❌ Failed to create {repo_name}: {response.status_code}")
                logger.error(f"   Response: {response.text[:200]}")
                return None

        except requests.RequestException as e:
            logger.error(f"❌ Request error creating {repo_name}: {e}")
            return None

    def _normalize_repo_name(self, name: str) -> str:
        """
        Normalize name to valid GitHub repository name following APEX convention.

        APEX Naming Convention (Dec 2025):
        Format: Title-Case-With-Hyphens
        Formula: <Product>-<Function>-<Platform>-<Type>

        Rules:
        - Can only contain alphanumeric, hyphens
        - Cannot start with hyphen
        - Max 100 characters
        - 3-10 words
        """
        # Replace spaces and underscores with hyphens
        normalized = name.replace(" ", "-").replace("_", "-")

        # Remove invalid characters (keep only alphanumeric and hyphens)
        normalized = re.sub(r"[^a-zA-Z0-9\-]", "", normalized)

        # Remove consecutive hyphens
        normalized = re.sub(r"-+", "-", normalized)

        # Remove leading/trailing hyphens
        normalized = normalized.strip("-")

        # Title case each word
        words = normalized.split("-")
        normalized = "-".join(w.capitalize() for w in words if w)

        # Limit length to 100 characters
        if len(normalized) > 100:
            normalized = normalized[:100].rsplit("-", 1)[0]

        return normalized

    def _set_topics(self, repo_name: str, topics: list[str]) -> None:
        """Set repository topics (lowercase-with-hyphens format)."""
        # Normalize topics (lowercase, alphanumeric + hyphens only)
        normalized_topics = []
        for topic in topics[:20]:  # Max 20 topics
            t = topic.lower().replace(" ", "-")
            t = re.sub(r"[^a-z0-9\-]", "", t)
            if t and len(t) >= 1:
                normalized_topics.append(t)

        try:
            self.session.put(
                f"{self.base_url}/repos/{self.config.GH_USERNAME}/{repo_name}/topics",
                json={"names": normalized_topics},
                timeout=30
            )
            logger.info(f"   🏷️ Set topics: {normalized_topics[:5]}...")
        except requests.RequestException as e:
            logger.warning(f"   ⚠️ Failed to set topics: {e}")

    def generate_short_name(self, idea: str) -> str:
        """
        Generate a SHORT, descriptive repository name.

        New Naming Convention (Jan 2026):
        - Maximum 2-3 words
        - Lowercase with hyphens
        - Immediately clear purpose
        - SEO-friendly and searchable

        Examples:
        - "PDF Compressor Tool" -> "pdf-compress"
        - "PNG to JPG Converter" -> "png-jpg"
        - "Image Optimization Utility" -> "image-shrink"
        - "YouTube Video Downloader" -> "yt-download"
        - "QR Code Generator" -> "qr-gen"
        - "Password Generator Tool" -> "pass-gen"
        - "JSON Formatter" -> "json-fmt"
        - "Markdown Editor" -> "md-editor"
        """
        # Common abbreviations for shorter names
        abbreviations = {
            "compressor": "compress",
            "compression": "compress",
            "converter": "convert",
            "conversion": "convert",
            "downloader": "download",
            "generator": "gen",
            "optimizer": "optim",
            "optimization": "optim",
            "formatter": "fmt",
            "editor": "edit",
            "viewer": "view",
            "reader": "read",
            "writer": "write",
            "analyzer": "analyze",
            "extractor": "extract",
            "validator": "validate",
            "builder": "build",
            "creator": "create",
            "manager": "mgr",
            "tracker": "track",
            "scanner": "scan",
            "resizer": "resize",
            "cropper": "crop",
            "merger": "merge",
            "splitter": "split",
            "youtube": "yt",
            "instagram": "ig",
            "twitter": "tw",
            "facebook": "fb",
            "linkedin": "li",
            "tiktok": "tt",
            "javascript": "js",
            "typescript": "ts",
            "python": "py",
            "password": "pass",
            "markdown": "md",
            "application": "app",
            "utility": "",
            "tool": "",
            "online": "",
            "free": "",
            "best": "",
            "simple": "",
            "easy": "",
            "quick": "",
            "fast": "",
            "super": "",
            "ultimate": "",
            "advanced": "",
            "modern": "",
            "smart": "",
            "professional": "",
            "premium": "",
        }

        # Clean and lowercase
        clean = idea.lower().strip()

        # Remove common noise words
        noise_words = ["the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "with", "by", "from", "as"]
        words = clean.replace("-", " ").replace("_", " ").split()
        words = [w for w in words if w not in noise_words]

        # Apply abbreviations
        abbreviated = []
        for word in words:
            if word in abbreviations:
                abbrev = abbreviations[word]
                if abbrev:  # Skip empty abbreviations (noise removal)
                    abbreviated.append(abbrev)
            else:
                # Keep alphanumeric only
                clean_word = re.sub(r"[^a-z0-9]", "", word)
                if clean_word:
                    abbreviated.append(clean_word)

        # Take first 3 words max
        short_words = abbreviated[:3]

        # If result is too long, shorten further
        result = "-".join(short_words)

        # Limit total length to 30 chars
        if len(result) > 30:
            result = result[:30].rsplit("-", 1)[0]

        # Ensure not empty
        if not result:
            result = "tool"

        return result

    def _normalize_to_short_name(self, name: str) -> str:
        """
        Normalize to GitHub-compatible short name.
        Lowercase, hyphens, alphanumeric only.
        """
        # Lowercase and replace spaces/underscores
        normalized = name.lower().replace(" ", "-").replace("_", "-")

        # Remove invalid characters
        normalized = re.sub(r"[^a-z0-9\-]", "", normalized)

        # Remove consecutive hyphens
        normalized = re.sub(r"-+", "-", normalized)

        # Remove leading/trailing hyphens
        normalized = normalized.strip("-")

        return normalized


    def generate_creation_prompt(
        self,
        idea: str,
        description: str,
        category: str = "web_app"
    ) -> str:
        """
        Generate Jules prompt for new repository creation.

        Returns AGENTS.md Dec 2025 compliant prompt for full project generation.
        """
        # Load AGENTS.md content
        agents_md = self._load_agents_md()

        return f"""
# NEW REPOSITORY CREATION TASK

## Project Idea
**Name:** {idea}
**Description:** {description}
**Category:** {category}

## YOUR MISSION
You are a Senior FAANG Engineer. Build a COMPLETE, PRODUCTION-READY {category} project.

## CRITICAL REQUIREMENTS

### 1. FRONTEND-ONLY ARCHITECTURE (MANDATORY)
Constraint: ALL repositories MUST be frontend-only. NO backend servers/APIs.
Rationale: Limited deployment resources. Run entirely in browser.

**Implementation Rules:**
- ✅ Direct REST Calls: All AI/external services via fetch/axios. NO SDKs.
- ✅ User-Provided Keys: Users enter API keys in UI. NEVER hardcode.
- ✅ Client-Side Processing: Logic runs in browser. Use Web Workers.
- ✅ Static Hosting: GitHub Pages, Vercel, Netlify, Cloudflare Pages.
- ❌ NO Express/Flask/Django servers
- ❌ NO backend API routes
- ❌ NO database connections

### 2. AI ORCHESTRATION (Dec 2025 PARADIGM)
Protocol: Raw REST APIs only. Exponential backoff (start 1s, max 32s).
Fallback Logic: Cerebras -> Gemini -> Groq -> Mistral -> NVIDIA -> Cloudflare.

**Provider 1: Cerebras Inference (Primary)**
- Base URL: https://api.cerebras.ai/v1
- Endpoint: POST /chat/completions
- Models: qwen-3-235b-a22b-instruct-2507, gpt-oss-120b, zai-glm-4.6, llama-3.3-70b

**Provider 2: Google Gemini API (Backup)**
- Base URL: https://generativelanguage.googleapis.com/v1beta
- Models: gemma-3-27b-instruct, gemma-3-12b-instruct

**Provider 3: Resilience Layer**
- Groq: https://api.groq.com/openai/v1
- Mistral: https://api.mistral.ai/v1
- NVIDIA NIM: https://api.nvidia.com/nim
- Cloudflare Workers AI: 100k req/day

### 3. PROJECT STRUCTURE
Create the following:
```
src/
├── index.html
├── main.ts
├── styles/
├── components/
└── api/
    ├── cerebras.ts
    ├── gemini.ts
    ├── groq.ts
    └── fallback.ts
tests/
.github/
├── workflows/ci.yml
├── ISSUE_TEMPLATE/
│   └── bug_report.md
└── PULL_REQUEST_TEMPLATE.md
```

### 3.5. CENTRAL HUB INTEGRATION (MANDATORY)
ALL repositories MUST load shared resources from the central hub at chirag127.github.io.
This allows changing analytics/profile/monetization once and updating all sites.

**In every index.html <head>:**
```html
<!-- Centralized Analytics (10 trackers) - DO NOT duplicate -->
<script src="https://chirag127.github.io/shared/analytics.js" defer></script>
```

**Before </body>:**
```html
<!-- Centralized Monetization (A-Ads, BMC) -->
<script src="https://chirag127.github.io/shared/monetization.js" defer></script>

<!-- Load shared header/footer from hub -->
<script>
  async function loadShared() {{
    try {{
      const h = await fetch('https://chirag127.github.io/shared/header.html').then(r => r.text());
      document.getElementById('central-header').innerHTML = h;
      const f = await fetch('https://chirag127.github.io/shared/footer.html').then(r => r.text());
      document.getElementById('central-footer').innerHTML = f;
    }} catch (e) {{ console.warn('Shared load failed'); }}
  }}
  loadShared();
</script>
```

**NEVER duplicate these in individual projects:**
- Analytics tracking codes (GA4, Yandex, Clarity, Mixpanel, etc.)
- Profile/Author information
- Monetization widgets (A-Ads, BMC button)
- Footer with social links


### 4. MANDATORY FILES (Generate ALL 10)
1. README.md - Hero-tier with badges, quickstart
2. .github/badges.yml - Shield.io configurations
3. LICENSE - CC BY-NC 4.0
4. .gitignore - Comprehensive
5. .github/workflows/ci.yml - Full CI/CD
6. CONTRIBUTING.md - Contribution guidelines
7. .github/ISSUE_TEMPLATE/bug_report.md
8. .github/PULL_REQUEST_TEMPLATE.md
9. SECURITY.md - Security policy
10. AGENTS.md - System prompt (customized)

### 5. TECH STACK (Late 2025)
- TypeScript 6.x with strict mode
- Vite 7 (Rolldown) for bundling
- Tailwind v4 for styling
- Signals for state management
- Biome for linting
- Vitest for testing

### 6. UI/UX (2026 Standard)
- Spatial Glass effects
- Bento Grid layouts
- Depth Stacking
- Spring animations (kinetic physics)
- Adaptive: Morph based on input (Touch/Mouse)

### 7. QUALITY STANDARDS
- SOLID, GRASP, Clean Architecture principles
- 100% working code (no placeholders)
- Error handling with try-catch
- Loading states and error boundaries
- Responsive design

---

# FULL AGENTS.MD SPECIFICATION

{agents_md[:8000]}

---

Execute now. Generate ALL files. Create a COMPLETE working project.
"""

    def _load_agents_md(self) -> str:
        """Load AGENTS.md content."""
        try:
            agents_path = self.config.AGENTS_MD_PATH
            with open(agents_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "# AGENTS.md not found"

    def check_repo_exists(self, name: str) -> bool:
        """Check if repository already exists."""
        repo_name = self._normalize_repo_name(name)
        try:
            response = self.session.get(
                f"{self.base_url}/repos/{self.config.GH_USERNAME}/{repo_name}",
                timeout=10
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def generate_apex_name(self, idea: str, category: str) -> str:
        """
        Generate an APEX-compliant name from an idea.

        Formula: <Product>-<Function>-<Platform>-<Type>
        Format: Title-Case-With-Hyphens
        """
        # Clean the idea
        clean_idea = idea.replace("_", " ").replace("-", " ")
        words = clean_idea.split()

        # Capitalize each word
        title_words = [w.capitalize() for w in words if w]

        # Add category suffix if not present
        category_map = {
            # Web Applications
            "web_app": "Web-App",
            "webapp": "Web-App",
            "react_app": "React-Web-App",
            "vue_app": "Vue-Web-App",
            "nextjs_app": "Next-Web-App",
            "angular_app": "Angular-Web-App",
            "svelte_app": "Svelte-Web-App",
            "frontend": "Web-App",
            "spa": "Single-Page-Web-App",
            "pwa": "Progressive-Web-App",
            "dashboard": "Dashboard-Web-App",
            "landing_page": "Landing-Page-Web-App",
            "portfolio": "Portfolio-Web-App",
            "ecommerce": "Ecommerce-Web-App",

            # Browser Extensions
            "chrome_extension": "Browser-Extension",
            "browser_extension": "Browser-Extension",
            "firefox_extension": "Browser-Extension",
            "edge_extension": "Browser-Extension",
            "safari_extension": "Browser-Extension",
            "extension": "Browser-Extension",
            "addon": "Browser-Extension",
            "tampermonkey": "Userscript",
            "userscript": "Userscript",

            # Mobile Applications
            "mobile_app": "Mobile-App",
            "android_app": "Android-Mobile-App",
            "ios_app": "iOS-Mobile-App",
            "react_native_app": "React-Native-Mobile-App",
            "flutter_app": "Flutter-Mobile-App",
            "expo_app": "Expo-Mobile-App",
            "cross_platform_mobile": "Cross-Platform-Mobile-App",

            # Desktop Applications
            "desktop_app": "Desktop-App",
            "electron_app": "Electron-Desktop-App",
            "tauri_app": "Tauri-Desktop-App",
            "macos_app": "MacOS-Desktop-App",
            "windows_app": "Windows-Desktop-App",
            "linux_app": "Linux-Desktop-App",
            "cross_platform_desktop": "Cross-Platform-Desktop-App",

            # CLI Tools
            "cli_tool": "CLI-Tool",
            "cli": "CLI-Tool",
            "terminal_tool": "Terminal-CLI-Tool",
            "python_cli": "Python-CLI-Tool",
            "node_cli": "Node-CLI-Tool",
            "rust_cli": "Rust-CLI-Tool",
            "go_cli": "Go-CLI-Tool",
            "shell_script": "Shell-Script",
            "bash_script": "Bash-Script",

            # Libraries & Packages
            "library": "Library",
            "lib": "Library",
            "package": "Package",
            "sdk": "SDK",
            "framework": "Framework",
            "python_lib": "Python-Library",
            "npm_package": "NPM-Package",
            "typescript_lib": "TypeScript-Library",
            "rust_crate": "Rust-Crate",
            "go_module": "Go-Module",

            # AI/ML Tools
            "ai_ml": "AI-ML-Tool",
            "ai_tool": "AI-Tool",
            "ml_tool": "ML-Tool",
            "ai_assistant": "AI-Assistant",
            "llm_tool": "LLM-Tool",
            "nlp_tool": "NLP-Tool",
            "computer_vision": "Computer-Vision-Tool",
            "data_processing": "Data-Processing-Tool",
            "model_training": "Model-Training-Tool",

            # Developer Tools
            "devtools": "Developer-Tool",
            "dev_tool": "Developer-Tool",
            "developer_tool": "Developer-Tool",
            "debugging_tool": "Debugging-Tool",
            "testing_tool": "Testing-Tool",
            "linter": "Linting-Tool",
            "formatter": "Code-Formatter",
            "build_tool": "Build-Tool",
            "code_generator": "Code-Generator",
            "scaffolding": "Scaffolding-Tool",

            # Automation Tools
            "automation": "Automation-Tool",
            "automation_tool": "Automation-Tool",
            "workflow": "Workflow-Automation-Tool",
            "scraper": "Web-Scraper",
            "web_scraper": "Web-Scraping-Tool",
            "bot": "Bot-Automation-Tool",
            "github_action": "GitHub-Action",
            "ci_cd": "CI-CD-Tool",
            "task_runner": "Task-Runner",

            # API & Backend (frontend-only wrappers)
            "api_wrapper": "API-Wrapper",
            "api_client": "API-Client",
            "rest_client": "REST-API-Client",
            "graphql_client": "GraphQL-Client",

            # Data & Analytics
            "data_viz": "Data-Visualization-Tool",
            "analytics": "Analytics-Dashboard",
            "reporting": "Reporting-Tool",
            "monitoring": "Monitoring-Tool",

            # Content & Documentation
            "blog": "Blog-Web-App",
            "cms": "Content-Management-Web-App",
            "docs": "Documentation-Site",
            "wiki": "Wiki-Web-App",
            "static_site": "Static-Site-Generator",

            # Games & Creative
            "game": "Game",
            "web_game": "Web-Game",
            "canvas_app": "Canvas-Web-App",
            "creative_tool": "Creative-Tool",

            # Utilities & Misc
            "utility": "Utility-Tool",
            "converter": "Converter-Tool",
            "generator": "Generator-Tool",
            "template": "Template",
            "boilerplate": "Boilerplate",
            "starter_kit": "Starter-Kit",
            "awesome_list": "Awesome-List",
            "filter_list": "Filter-List",
            "config": "Configuration",
        }

        suffix = category_map.get(category, "Tool")

        # Check if suffix-like words already present
        last_word = title_words[-1].lower() if title_words else ""
        if last_word not in ["app", "tool", "extension", "library", "cli"]:
            title_words.append(suffix)

        # Join with hyphens
        apex_name = "-".join(title_words)

        # Normalize and limit length
        return self._normalize_repo_name(apex_name)
