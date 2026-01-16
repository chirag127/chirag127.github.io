#!/usr/bin/env python3
"""
Delete Empty Private Repositories (Optimized)

Finds and deletes private repos that only contain README.md.
Features:
- Infinite Pagination (Handles >1000 repos)
- Immediate Deletion (Persists progress)
- Error Resilience (Retries on network failure)

Usage:
  python delete_empty_repos.py --dry-run  # Preview
  python delete_empty_repos.py --confirm  # Execute
"""

import logging
import os
import sys
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

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

def gh_api(method: str, endpoint: str, data: dict = None, retries=3) -> requests.Response:
    """Make authenticated GitHub API request with retries."""
    url = f"https://api.github.com{endpoint}"
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    for attempt in range(retries):
        try:
            if method == "GET":
                r = requests.get(url, headers=headers, timeout=30)
            elif method == "DELETE":
                r = requests.delete(url, headers=headers, timeout=30)
            elif method == "POST":
                r = requests.post(url, headers=headers, json=data, timeout=30)
            return r
        except requests.RequestException as e:
            logger.warning(f"   ⚠️ Network error ({e}). Retrying {attempt+1}/{retries}...")
            time.sleep(2 * (attempt + 1))

    return None

def get_repo_contents(repo_name: str) -> list[dict]:
    """Get root-level contents of a repo."""
    r = gh_api("GET", f"/repos/{GH_USERNAME}/{repo_name}/contents")
    if r and r.status_code == 200:
        return r.json()
    return []

def is_empty_repo(repo: dict) -> bool:
    """Check if repo only has README.md."""
    if not repo.get("private"):
        return False

    try:
        contents = get_repo_contents(repo["name"])

        # If folder is empty
        if isinstance(contents, list) and len(contents) == 0:
            return True

        # If only README exists
        if isinstance(contents, list) and len(contents) == 1:
            file_name = contents[0].get("name", "").lower()
            if file_name in ["readme.md", "readme", "readme.txt"]:
                return True

    except Exception as e:
        logger.error(f"   ❌ Error checking contents: {e}")

    return False

def delete_repo(repo_name: str) -> bool:
    """Delete a repository."""
    r = gh_api("DELETE", f"/repos/{GH_USERNAME}/{repo_name}")
    return r and r.status_code == 204

def process_repos(dry_run: bool):
    page = 1
    total_checked = 0
    total_deleted = 0

    while True:
        logger.info(f"📦 Fetching page {page}...")
        r = gh_api("GET", f"/user/repos?per_page=100&page={page}&type=all")

        if not r or r.status_code != 200:
            logger.error(f"❌ Failed to fetch page {page}")
            break

        data = r.json()
        if not data:
            logger.info("✅ No more repositories found.")
            break

        logger.info(f"   Found {len(data)} repos on page {page}")

        for repo in data:
            total_checked += 1
            name = repo["name"]

            # Skip non-private immediately to save API calls
            if not repo.get("private"):
                continue

            logger.info(f"   [{total_checked}] Checking: {name}")

            if is_empty_repo(repo):
                if dry_run:
                    logger.info(f"      🗑️ [DRY RUN] Would delete: {name}")
                else:
                    if delete_repo(name):
                        logger.info(f"      ✅ DELETED: {name}")
                        total_deleted += 1
                    else:
                        logger.error(f"      ❌ FAILED DELETE: {name}")

        page += 1

    logger.info("-" * 40)
    logger.info(f"🎉 Complete. Deleted {total_deleted} repositories.")

def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args or "--confirm" not in args

    if dry_run:
        logger.info("🔍 DRY RUN MODE - Use --confirm to delete")
    else:
        logger.warning("⚠️ DELETION MODE ENABLED - Deleting immediately")
        time.sleep(3) # Give user a moment to cancel

    process_repos(dry_run)

if __name__ == "__main__":
    main()
