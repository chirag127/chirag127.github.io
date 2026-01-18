"""
Apex Optimizer - Core Automation Engine

Orchestrates:
1. Repository optimization (existing repos)
2. Tool generation (from ar.txt approved list)
3. GitHub Pages deployment
4. Central hub resource integration

Architecture:
- All AI calls via UnifiedAIClient (6 providers, auto-fallback)
- All analytics/monetization from chirag127.github.io central hub
- Client-side only projects (no backend)
- React + Vite for tools, auto-deploy via GitHub Actions
"""

import concurrent.futures
import logging
import os
import sys
from pathlib import Path
from typing import Any

from .cache import CacheManager
from src.ai.unified_client import UnifiedAIClient
from src.clients.github import GitHubClient
from .config import Settings

# =============================================================================
# LOGGING
# =============================================================================

class UnbufferedFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.flush()


formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

log_file_path = Path(__file__).parent.parent / "apex_optimizer.log"
file_handler = UnbufferedFileHandler(str(log_file_path), encoding="utf-8")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO, handlers=[stream_handler, file_handler])
logger = logging.getLogger("ApexOptimizer")


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception


# =============================================================================
# CENTRAL HUB CONFIGURATION
# =============================================================================

CENTRAL_HUB = Settings.SITE_BASE_URL
SHARED_ANALYTICS = f"{CENTRAL_HUB}/shared/analytics.js"
SHARED_MONETIZATION = f"{CENTRAL_HUB}/shared/monetization.js"


# =============================================================================
# APEX OPTIMIZER
# =============================================================================

class ApexOptimizer:
    """
    Core automation engine for repository management.

    Features:
    - Optimize existing repositories (README, docs, SEO)
    - Generate new tools from approved list (ar.txt)
    - Ensure central hub integration
    - Auto-deploy to GitHub Pages
    """

    def __init__(self) -> None:
        self.config = Settings()
        self.ai = UnifiedAIClient()  # 6 AI providers with auto-fallback
        self.github = GitHubClient(self.config)
        self.cache = CacheManager(self.config)

        logger.info("ApexOptimizer initialized")
        logger.info(f"  AI Providers: {len(self.ai.providers)} available")
        logger.info(f"  Central Hub: {CENTRAL_HUB}")

    def optimize_repository(self, repo: dict[str, Any]) -> bool:
        """
        Optimize an existing repository.

        Actions:
        - Update README with better formatting
        - Add missing files (LICENSE, CONTRIBUTING, etc.)
        - Ensure GitHub Pages deployment workflow
        - Add central hub analytics/monetization
        """
        name = repo["name"]

        try:
            # Skip archived/processed repos
            if repo.get("isArchived"):
                logger.info(f"  Skip {name} (archived)")
                return False

            cache_key = f"optimized:{name}"
            if self.cache.exists(cache_key):
                logger.info(f"  Skip {name} (cached)")
                return False

            logger.info(f"Optimizing: {name}")

            # Get current state
            readme = self.github.get_readme_content(name) or ""

            # Generate optimization strategy
            result = self.ai.generate_json(
                prompt=f"""Analyze this repository and suggest optimizations:

Repository: {name}
Description: {repo.get('description', 'No description')}
Stars: {repo.get('stargazers', {}).get('totalCount', 0)}
Language: {repo.get('primaryLanguage', {}).get('name', 'Unknown')}

Current README (first 2000 chars):
{readme[:2000]}

Provide JSON with:
- action: "UPDATE" | "SKIP" | "ARCHIVE"
- reason: Why this action
- readme_improvements: List of improvements needed
- missing_files: List of files to add
- needs_pages: Boolean - does it need GitHub Pages?
- is_web_project: Boolean - is this a web app/site?
""",
                system_prompt="You are a repository optimization expert. Be concise.",
                max_tokens=2048,
            )

            if not result.success or not result.json_content:
                logger.warning(f"  Strategy failed for {name}")
                return False

            strategy = result.json_content
            action = strategy.get("action", "SKIP")

            if action == "SKIP":
                logger.info(f"  No changes needed for {name}")
                self.cache.set(cache_key, {"status": "skipped"})
                return True

            if action == "UPDATE":
                # Update README if improvements needed
                if strategy.get("readme_improvements"):
                    self._update_readme(name, readme, strategy["readme_improvements"])

                # Add missing files
                for file_path in strategy.get("missing_files", []):
                    self._add_missing_file(name, file_path)

                # Ensure GitHub Pages workflow if web project
                if strategy.get("needs_pages") or strategy.get("is_web_project"):
                    self._ensure_pages_workflow(name)

            self.cache.set(cache_key, {"status": "completed", "action": action})
            logger.info(f"  Completed: {name}")
            return True

        except Exception as e:
            logger.error(f"  Error optimizing {name}: {e}")
            return False

    def _update_readme(self, repo_name: str, current: str, improvements: list) -> bool:
        """Update README with improvements."""
        result = self.ai.generate(
            prompt=f"""Improve this README based on suggestions:

Current README:
{current[:3000]}

Improvements needed:
{chr(10).join(f"- {i}" for i in improvements)}

Requirements:
- Keep existing content structure
- Add badges if missing
- Add "Made by Chirag Singhal" footer
- Link to {CENTRAL_HUB}

Output the complete improved README.
""",
            max_tokens=4096,
        )

        if result.success and result.content:
            return self.github.update_file(
                repo_name=repo_name,
                file_path="README.md",
                content=result.content,
                commit_message="docs: improve README"
            )
        return False

    def _add_missing_file(self, repo_name: str, file_path: str) -> bool:
        """Generate and add a missing file."""
        result = self.ai.generate(
            prompt=f"""Generate the content for: {file_path}

For repository: {repo_name}
Author: Chirag Singhal (github.com/chirag127)

If it's an HTML file, include:
<script src="{SHARED_ANALYTICS}" defer></script>
<script src="{SHARED_MONETIZATION}" defer></script>
""",
            max_tokens=2048,
        )

        if result.success and result.content:
            return self.github.update_file(
                repo_name=repo_name,
                file_path=file_path,
                content=result.content,
                commit_message=f"feat: add {file_path}"
            )
        return False

    def _ensure_pages_workflow(self, repo_name: str) -> bool:
        """Ensure GitHub Pages deployment workflow exists."""
        workflow = """name: Deploy to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - id: deployment
        uses: actions/deploy-pages@v4
"""
        return self.github.update_file(
            repo_name=repo_name,
            file_path=".github/workflows/deploy.yml",
            content=workflow,
            commit_message="ci: add GitHub Pages deployment"
        )

    def run(self) -> None:
        """Run the optimization cycle on all repositories."""
        try:
            repos = self.github.fetch_all_repos()

            logger.info(f"\nStarting Apex Optimization on {len(repos)} repositories...")
            logger.info(f"Concurrency: {self.config.MAX_WORKERS} workers\n")

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.MAX_WORKERS) as executor:
                futures = [executor.submit(self.optimize_repository, repo) for repo in repos]
                concurrent.futures.wait(futures)

            logger.info("\nOptimization cycle complete.")

        except KeyboardInterrupt:
            logger.info("\nInterrupted by user.")
            raise
        except Exception as e:
            logger.error(f"\nFatal error: {e}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Entry point for apex optimizer."""
    optimizer = ApexOptimizer()
    optimizer.run()


if __name__ == "__main__":
    main()
