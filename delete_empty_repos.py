#!/usr/bin/env python3
"""
Delete Empty Private Repositories

Finds and deletes private repos that only contain README.md.
These are likely incomplete tool repos that were created but never filled.

Usage:
  python delete_empty_repos.py --dry-run  # Preview what would be deleted
  python delete_empty_repos.py --confirm  # Actually delete repos

Safety:
- Only deletes PRIVATE repos
- Only deletes repos with 1 file (README.md)
- Requires explicit --confirm flag
"""

import logging
import os
import sys
from datetime import datetime

import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('RepoCleanup')

GH_TOKEN = os.getenv("GH_TOKEN")
GH_USERNAME = "chirag127"

if not GH_TOKEN:
    logger.error("GH_TOKEN environment variable not set")
    sys.exit(1)


def gh_api(method: str, endpoint: str, data: dict = None) -> requests.Response:
    """Make authenticated GitHub API request."""
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    if method == "GET":
        return requests.get(url, headers=headers, timeout=30)
    elif method == "DELETE":
        return requests.delete(url, headers=headers, timeout=30)
    elif method == "POST":
        return requests.post(url, headers=headers, json=data, timeout=30)


def get_all_repos() -> list[dict]:
    """Fetch all repos with pagination."""
    repos = []
    page = 1

    while True:
        r = gh_api("GET", f"/user/repos?per_page=100&page={page}&type=all")
        if r.status_code != 200:
            logger.error(f"API error: {r.status_code}")
            break

        data = r.json()
        if not data:
            break

        repos.extend(data)
        page += 1

        if page > 10:  # Safety limit
            break

    return repos


def get_repo_contents(repo_name: str) -> list[dict]:
    """Get root-level contents of a repo."""
    r = gh_api("GET", f"/repos/{GH_USERNAME}/{repo_name}/contents")
    if r.status_code == 200:
        return r.json()
    return []


def is_empty_repo(repo: dict) -> bool:
    """Check if repo only has README.md."""
    if not repo.get("private"):
        return False  # Only check private repos

    contents = get_repo_contents(repo["name"])

    if len(contents) == 0:
        return True  # Completely empty

    if len(contents) == 1:
        file_name = contents[0].get("name", "").lower()
        if file_name in ["readme.md", "readme", "readme.txt"]:
            return True

    return False


def delete_repo(repo_name: str) -> bool:
    """Delete a repository."""
    r = gh_api("DELETE", f"/repos/{GH_USERNAME}/{repo_name}")
    return r.status_code == 204


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args or "--confirm" not in args

    if dry_run:
        logger.info("🔍 DRY RUN MODE - No repos will be deleted")
        logger.info("   Use --confirm to actually delete repos")
    else:
        logger.warning("⚠️ DELETE MODE - Repos will be permanently deleted!")

    logger.info("")
    logger.info("📦 Fetching all repositories...")
    repos = get_all_repos()
    logger.info(f"   Found {len(repos)} total repos")

    private_repos = [r for r in repos if r.get("private")]
    logger.info(f"   {len(private_repos)} are private")

    empty_repos = []

    logger.info("")
    logger.info("🔍 Checking for empty repos (only README.md)...")

    for i, repo in enumerate(private_repos):
        name = repo["name"]
        logger.info(f"   [{i+1}/{len(private_repos)}] Checking: {name}")

        if is_empty_repo(repo):
            empty_repos.append(repo)
            logger.info(f"      ❌ EMPTY: {name}")

    logger.info("")
    logger.info(f"📊 Found {len(empty_repos)} empty private repos")

    if not empty_repos:
        logger.info("✅ No empty repos to delete!")
        return

    logger.info("")
    logger.info("Empty repos to delete:")
    for repo in empty_repos:
        created = repo.get("created_at", "")[:10]
        logger.info(f"   - {repo['name']} (created: {created})")

    if dry_run:
        logger.info("")
        logger.info("🛡️ DRY RUN complete. Run with --confirm to delete.")
        return

    # Actually delete
    logger.info("")
    logger.info("🗑️ Deleting repos...")

    deleted = 0
    failed = 0

    for repo in empty_repos:
        name = repo["name"]
        if delete_repo(name):
            logger.info(f"   ✅ Deleted: {name}")
            deleted += 1
        else:
            logger.error(f"   ❌ Failed: {name}")
            failed += 1

    logger.info("")
    logger.info(f"📊 Summary: {deleted} deleted, {failed} failed")


if __name__ == "__main__":
    main()
