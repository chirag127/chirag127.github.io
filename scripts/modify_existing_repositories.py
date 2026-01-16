#!/usr/bin/env python3
"""
Modify Existing Repositories

Purpose:
- Optimize README files
- Archive dead/empty repositories
- Make repositories public/private
- Delete spam/useless repositories
- Update metadata and topics

Runs daily via GitHub Actions.
"""

import logging
import os
import sys
from pathlib import Path

import requests

# Add Root to Path
sys.path.append(str(Path(__file__).parent.parent))

from src.ai.unified_client import UnifiedAIClient
from src.core.config import Settings


# =============================================================================
# CONFIGURATION
# =============================================================================

GH_TOKEN = os.getenv("GH_TOKEN")
GH_USERNAME = "chirag127"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("ModifyRepos")


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
    elif method == "PATCH":
        return requests.patch(url, headers=headers, json=data, timeout=60)
    elif method == "DELETE":
        return requests.delete(url, headers=headers, timeout=60)


def get_all_repos() -> list[dict]:
    """Fetch all user repositories."""
    repos = []
    page = 1

    while True:
        r = gh_api("GET", f"/users/{GH_USERNAME}/repos?per_page=100&page={page}")
        if r.status_code != 200:
            break

        data = r.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    logger.info(f"Found {len(repos)} repositories")
    return repos


def get_repo_details(name: str) -> dict:
    """Get detailed repo info."""
    r = gh_api("GET", f"/repos/{GH_USERNAME}/{name}")
    return r.json() if r.status_code == 200 else {}


def is_repo_empty(name: str) -> bool:
    """Check if repo has no commits."""
    r = gh_api("GET", f"/repos/{GH_USERNAME}/{name}/commits?per_page=1")
    return r.status_code == 409 or not r.json()


def archive_repo(name: str) -> bool:
    """Archive a repository."""
    logger.info(f"  Archiving: {name}")
    r = gh_api("PATCH", f"/repos/{GH_USERNAME}/{name}", {"archived": True})
    return r.status_code == 200


def delete_repo(name: str) -> bool:
    """Delete a repository (careful!)."""
    logger.info(f"  Deleting: {name}")
    r = gh_api("DELETE", f"/repos/{GH_USERNAME}/{name}")
    return r.status_code == 204


def make_public(name: str) -> bool:
    """Make repository public."""
    logger.info(f"  Making public: {name}")
    r = gh_api("PATCH", f"/repos/{GH_USERNAME}/{name}", {"private": False})
    return r.status_code == 200


def make_private(name: str) -> bool:
    """Make repository private."""
    logger.info(f"  Making private: {name}")
    r = gh_api("PATCH", f"/repos/{GH_USERNAME}/{name}", {"private": True})
    return r.status_code == 200


def update_repo_metadata(name: str, description: str = None, topics: list[str] = None) -> bool:
    """Update repo description and topics."""
    data = {}
    if description:
        data["description"] = description[:350]

    if data:
        r = gh_api("PATCH", f"/repos/{GH_USERNAME}/{name}", data)
        if r.status_code != 200:
            return False

    if topics:
        requests.put(
            f"https://api.github.com/repos/{GH_USERNAME}/{name}/topics",
            headers={
                "Authorization": f"Bearer {GH_TOKEN}",
                "Accept": "application/vnd.github.mercy-preview+json"
            },
            json={"names": [t.lower()[:35] for t in topics[:20]]},
            timeout=30
        )

    return True


# =============================================================================
# OPTIMIZATION LOGIC
# =============================================================================

def analyze_repo(repo: dict, ai: UnifiedAIClient) -> dict:
    """Use AI to analyze repository and suggest actions."""

    name = repo["name"]
    desc = repo.get("description", "") or ""
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    updated = repo.get("updated_at", "")
    archived = repo.get("archived", False)
    private = repo.get("private", False)

    if archived:
        return {"action": "SKIP", "reason": "Already archived"}

    # Check if empty
    if is_repo_empty(name):
        return {"action": "DELETE", "reason": "Empty repository with no commits"}

    # AI analysis
    prompt = f"""Analyze this GitHub repository:

Name: {name}
Description: {desc}
Stars: {stars}
Forks: {forks}
Last Updated: {updated}
Private: {private}

Suggest ONE action:
1. KEEP - Repository is valuable, keep as is
2. OPTIMIZE - Update description/topics for better SEO
3. ARCHIVE - Old/abandoned project, should be archived
4. DELETE - Spam/test/worthless repo, should be deleted
5. MAKE_PUBLIC - Should be made public for visibility

Return JSON:
{{"action": "KEEP|OPTIMIZE|ARCHIVE|DELETE|MAKE_PUBLIC", "reason": "why", "new_description": "if OPTIMIZE", "topics": ["if", "optimize"]}}
"""

    result = ai.generate_json(prompt=prompt, max_tokens=500)

    if result.success and result.json_content:
        return result.json_content

    # Default: keep
    return {"action": "KEEP", "reason": "AI analysis failed, keeping safe"}


def process_repo(repo: dict, ai: UnifiedAIClient) -> bool:
    """Process a single repository."""
    name = repo["name"]
    logger.info(f"\nAnalyzing: {name}")

    analysis = analyze_repo(repo, ai)
    action = analysis.get("action", "KEEP")
    reason = analysis.get("reason", "")

    logger.info(f"  Action: {action}")
    logger.info(f"  Reason: {reason}")

    if action == "KEEP":
        return True

    elif action == "OPTIMIZE":
        new_desc = analysis.get("new_description")
        topics = analysis.get("topics", [])
        return update_repo_metadata(name, new_desc, topics)

    elif action == "ARCHIVE":
        return archive_repo(name)

    elif action == "DELETE":
        # Be careful - only delete if truly worthless
        if repo.get("stargazers_count", 0) == 0 and repo.get("forks_count", 0) == 0:
            return delete_repo(name)
        else:
            logger.info("  Skipping delete - has stars/forks")
            return archive_repo(name)

    elif action == "MAKE_PUBLIC":
        return make_public(name)

    return True


# =============================================================================
# MAIN
# =============================================================================

def main():
    if not GH_TOKEN:
        logger.error("GH_TOKEN not set")
        sys.exit(1)

    logger.info("="*50)
    logger.info("Modify Existing Repositories")
    logger.info("="*50)

    repos = get_all_repos()
    ai = UnifiedAIClient()

    # Process only non-archived repos
    active_repos = [r for r in repos if not r.get("archived", False)]
    logger.info(f"Processing {len(active_repos)} active repositories...")

    processed = 0
    max_per_run = 10  # Limit per run to avoid rate limits

    for repo in active_repos[:max_per_run]:
        try:
            process_repo(repo, ai)
            processed += 1
        except Exception as e:
            logger.error(f"Error processing {repo['name']}: {e}")

    logger.info(f"\nProcessed {processed} repositories")
    logger.info("Done!")


if __name__ == "__main__":
    main()
