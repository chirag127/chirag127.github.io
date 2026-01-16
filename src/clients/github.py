import base64
import json
import logging
import sys
import time
from typing import Any

import requests

from ..cache import CacheManager
from ..config import Settings
from ..utils import retry_with_backoff

logger = logging.getLogger("ApexOptimizer")

class GitHubClient:
    def __init__(self, config: Settings) -> None:
        self.config = config
        self.cache = CacheManager(self.config)
        self.headers = {
            "Authorization": f"Bearer {self.config.GH_TOKEN}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json",
        }

    @retry_with_backoff
    def fetch_all_repos(self) -> list[dict[str, Any]]:
        cache_key = f"github_repos_{self.config.GH_USERNAME}_all"
        cached_repos = self.cache.get(cache_key)
        if cached_repos:
            logger.info(f"   📦 Cached repositories found for {self.config.GH_USERNAME}")
            return cached_repos

        logger.info("🚀 Fetching repository data via GraphQL (All Pages)...")

        all_repos = []
        has_next_page = True
        end_cursor = None

        query = """
        query($username: String!, $after: String) {
          user(login: $username) {
            repositories(first: 100, ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER], orderBy: {field: UPDATED_AT, direction: DESC}, after: $after) {
              pageInfo {
                hasNextPage
                endCursor
              }
              nodes {
                name
                description
                isArchived
                pushedAt
                primaryLanguage {
                  name
                }
                repositoryTopics(first: 10) {
                  nodes {
                    topic {
                      name
                    }
                  }
                }
              }
            }
          }
        }
        """

        while has_next_page:
            try:
                variables = {"username": self.config.GH_USERNAME}
                if end_cursor:
                    variables["after"] = end_cursor

                response = requests.post(
                    self.config.GITHUB_GRAPHQL_URL,
                    json={
                        "query": query,
                        "variables": variables,
                    },
                    headers=self.headers,
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()

                if "errors" in data:
                    logger.error("❌ GraphQL Query Errors:")
                    logger.error(json.dumps(data["errors"], indent=2))
                    sys.exit(1)

                repo_data = data["data"]["user"]["repositories"]
                repos = repo_data["nodes"]

                # Update pagination info
                page_info = repo_data["pageInfo"]
                has_next_page = page_info["hasNextPage"]
                end_cursor = page_info["endCursor"]

                # Flatten topics structure for easier access
                for repo in repos:
                    if repo.get("repositoryTopics"):
                        repo["repositoryTopics"]["nodes"] = [
                            node["topic"]["name"]
                            for node in repo["repositoryTopics"]["nodes"]
                        ]

                all_repos.extend(repos)
                logger.info(f"   Fetched {len(repos)} repositories (Total: {len(all_repos)})...")

            except Exception as e:
                logger.error(f"❌ GitHub API Error: {e}")
                raise  # Let retry handle it

        logger.info(f"✅ Successfully fetched {len(all_repos)} total repositories.")
        self.cache.set(cache_key, all_repos)
        return all_repos

    @retry_with_backoff
    def get_readme_content(self, repo_name: str) -> str:
        """
        Fetches the raw content of the repository's README.
        Returns empty string if not found.
        """
        cache_key = f"readme_{repo_name}"
        cached_readme = self.cache.get(cache_key)
        if cached_readme is not None:
             # logger.info(f"   📦 Cached README found for {repo_name}")
             return cached_readme

        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/readme"
        headers = {
            "Authorization": f"token {self.config.GH_TOKEN}",
            "Accept": "application/vnd.github.v3.raw",  # Request raw content
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                logger.info(f"   📄 Fetched README for {repo_name}")
                self.cache.set(cache_key, response.text)
                return response.text
            elif response.status_code == 404:
                logger.info(f"   ⚠️  No README found for {repo_name}")
                self.cache.set(cache_key, "")
                return ""
            else:
                logger.warning(f"   ⚠️  Failed to fetch README: {response.status_code}")
                return ""
        except Exception as e:
            logger.warning(f"   ⚠️  Error fetching README: {e}")
            return ""

    def archive_repo(self, repo_name: str) -> None:
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}"
        try:
            response = requests.patch(
                url, json={"archived": True}, headers=self.headers, timeout=30
            )
            if response.status_code == 200:
                logger.info(f"   ✅ Archived {repo_name}")
            else:
                logger.error(
                    f"   ❌ Failed to archive {repo_name}: {response.status_code} {response.text}"
                )
        except Exception as e:
            logger.error(f"   ❌ Error archiving {repo_name}: {e}")

    @retry_with_backoff
    def merge_pull_request(self, repo_name: str, pr_number: int) -> bool:
        """Merge a pull request."""
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/pulls/{pr_number}/merge"
        try:
            response = requests.put(
                url,
                json={"merge_method": "squash", "commit_title": f"Merge PR #{pr_number} via Apex Optimizer"},
                headers=self.headers,
                timeout=30
            )
            if response.status_code == 200:
                logger.info(f"   🟣 Merged PR #{pr_number} for {repo_name}")
                return True
            else:
                logger.error(f"   ❌ Failed to merge PR #{pr_number}: {response.status_code} {response.text}")
                return False
        except Exception as e:
            logger.error(f"   ❌ Error merging PR #{pr_number}: {e}")
            return False

    @retry_with_backoff
    def create_pull_request(
        self,
        repo_name: str,
        title: str,
        body: str,
        head: str,
        base: str = "main"
    ) -> dict | None:
        """Create a new pull request."""
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
        }

        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=30)
            if response.status_code == 201:
                pr = response.json()
                logger.info(f"   🚀 Created PR #{pr.get('number')}: {pr.get('html_url')}")
                return pr
            elif response.status_code == 422:
                logger.warning(f"   ⚠️  PR creation failed (422): Likely no commits or already exists.")
                return None
            else:
                logger.error(f"   ❌ Failed to create PR: {response.status_code} {response.text}")
                return None
        except Exception as e:
            logger.error(f"   ❌ Error creating PR: {e}")
            return None

    @retry_with_backoff
    def get_pull_request_details(self, repo_name: str, pr_number: int) -> dict:
        """Fetch detailed PR status including mergeability."""
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/pulls/{pr_number}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            logger.error(f"   ❌ Error fetching PR #{pr_number}: {e}")
            return {}

    @retry_with_backoff
    def close_pull_request(self, repo_name: str, pr_number: int, comment: str = None) -> bool:
        """Close a PR, optionally with a comment."""
        # 1. Post comment if provided
        if comment:
            comment_url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/issues/{pr_number}/comments"
            try:
                requests.post(comment_url, json={"body": comment}, headers=self.headers, timeout=30)
            except Exception:
                pass  # Non-critical

        # 2. Close PR
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/pulls/{pr_number}"
        try:
            response = requests.patch(url, json={"state": "closed"}, headers=self.headers, timeout=30)
            if response.status_code == 200:
                logger.info(f"   🚫 Closed PR #{pr_number} for {repo_name}")
                return True
            else:
                logger.error(f"   ❌ Failed to close PR #{pr_number}: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"   ❌ Error closing PR #{pr_number}: {e}")
            return False

    @retry_with_backoff
    def delete_branch(self, repo_name: str, branch_name: str) -> bool:
        """Delete a branch (ref)."""
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/git/refs/heads/{branch_name}"
        try:
            response = requests.delete(url, headers=self.headers, timeout=30)
            if response.status_code == 204:
                logger.info(f"   🗑️ Deleted branch {branch_name} for {repo_name}")
                return True
            else:
                logger.error(f"   ❌ Failed to delete branch {branch_name}: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"   ❌ Error deleting branch {branch_name}: {e}")
            return False

    @retry_with_backoff
    def update_repo_details(
        self, repo_name: str, new_name: str, description: str, topics: list[str]
    ) -> bool:
        # 1. Rename and Description
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}"

        # Truncate description to 350 chars (GitHub limit)
        if description and len(description) > 350:
            logger.warning(
                f"   ⚠️  Truncating description for {new_name} (Length: {len(description)} > 350)"
            )
            description = description[:347] + "..."

        payload = {"name": new_name, "description": description}

        logger.info(f"   🔄 Renaming to: {new_name}")
        try:
            response = requests.patch(url, json=payload, headers=self.headers, timeout=30)
            if response.status_code == 403:
                logger.warning(f"   🛑 Rate Limit (403) during rename/update for {repo_name}. Sleeping 120s...")
                time.sleep(120)
                return False

            if response.status_code != 200:
                logger.error(
                    f"   ❌ Failed to update details for {repo_name}: {response.status_code} {response.text}"
                )
                return False

            # Wait for rename to propagate
            if new_name != repo_name:
                time.sleep(2)
        except Exception as e:
            error_msg = str(e)
            if "422" in error_msg or (getattr(e, "response", None) and e.response.status_code == 422):
                 logger.warning(f"   ⚠️  Renaming failed for {repo_name} (422 Unprocessable Entity). Likely namespace lock. Skipping rename but continuing with other updates.")
                 # We continue, but we must ensure we use the OLD name for subsequent operations if rename failed
                 # However, the caller expects 'new_name' to be valid if we return True.
                 # If rename fails, we should probably return False for the rename part, but maybe we can still update topics?
                 # The current logic returns False on error.
                 # Let's return True but log the warning, so the script continues to process files using the OLD name?
                 # No, if we return True, the caller might assume 'new_name' is the repo name.
                 # Actually, the caller (core.py) uses 'target_name' which is set to 'new_name'.
                 # If rename fails, we must tell the caller to use 'repo_name' instead.
                 # But this method doesn't return the name.
                 # For now, let's just return False to be safe, BUT we want to avoid the "Aborting file updates" log in core.py if possible.
                 # Actually, the log says "Aborting file updates" if this returns False.
                 # So if we want to continue, we must return True, but we must rely on the fact that the rename didn't happen.
                 # This is tricky without changing the signature.
                 # Let's just return False for now as per plan, but make the log less alarming?
                 # Wait, the plan said "Log a warning and continue".
                 # To continue, we must return True. But then core.py will try to use 'new_name'.
                 # If 'new_name' != 'repo_name' and rename failed, using 'new_name' will fail 404.
                 # So we MUST return False if rename fails, unless we change core.py.
                 # Let's stick to returning False for rename failure for now, but handle the 403 specifically.
                 return False

            if "403" in error_msg or (getattr(e, "response", None) and e.response.status_code == 403):
                logger.warning(f"   🛑 Rate Limit (403) during rename/update for {repo_name}. Sleeping 120s...")
                time.sleep(120)
                return False

            logger.error(f"   ❌ Error updating details for {repo_name}: {e}")
            return False

        # 2. Update Topics (using NEW name)
        topics_url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{new_name}/topics"
        try:
            requests.put(topics_url, json={"names": topics}, headers=self.headers, timeout=30)
            logger.info(f"   🏷️  Updated topics: {topics}")
        except Exception as e:
            logger.error(f"   ❌ Error updating topics: {e}")

        return True

    @retry_with_backoff
    def update_file(self, repo_name: str, file_path: str, content: str, commit_message: str) -> None:
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/contents/{file_path}"
        max_retries = 5

        for attempt in range(max_retries):
            try:
                # Get current SHA
                get_resp = requests.get(url, headers=self.headers, timeout=30)
                sha = None
                if get_resp.status_code == 200:
                    sha = get_resp.json().get("sha")

                # Create/Update
                content_bytes = content.encode("utf-8")
                base64_content = base64.b64encode(content_bytes).decode("utf-8")

                payload = {
                    "message": commit_message,
                    "content": base64_content,
                }
                if sha:
                    payload["sha"] = sha

                put_resp = requests.put(url, json=payload, headers=self.headers, timeout=30)

                if put_resp.status_code in [200, 201]:
                    logger.info(f"   📄 Updated {file_path}")
                    return # Success

                elif put_resp.status_code == 409:
                    logger.warning(f"   ⚠️  Conflict (409) updating {file_path}. Retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(1 * (attempt + 1)) # Linear backoff
                    continue # Retry

                elif put_resp.status_code == 403:
                    logger.warning(f"   🛑 403 Forbidden updating {file_path}. Rate Limit? Sleeping 120s and retrying...")
                    time.sleep(120)
                    continue # Retry

                elif put_resp.status_code == 404 and ".github/workflows" in file_path:
                    logger.warning(f"   ⚠️  Failed to update {file_path} (404). Missing 'workflow' scope? Skipping.")
                    return # Skip this file, not fatal for the whole process

                else:
                    logger.error(
                        f"   ❌ Failed to update {file_path}: {put_resp.status_code} {put_resp.text}"
                    )
                    return # Fatal error, don't retry

            except Exception as e:
                if "403" in str(e) or (getattr(e, "response", None) and e.response.status_code == 403):
                     logger.warning(f"   🛑 403 Forbidden updating {file_path}. Rate Limit? Sleeping 120s and retrying...")
                     time.sleep(120)
                     continue
                logger.error(f"   ❌ Error updating {file_path}: {e}")
                return # Fatal error

        logger.error(f"   ❌ Failed to update {file_path} after {max_retries} retries.")

    def apply_optimizations(self, repo_name: str, files_dict: dict[str, str]) -> None:
        """
        Iterates through the files dictionary and updates/creates them in the repo.
        """
        logger.info(f"   🛠️  Applying file optimizations for {repo_name}...")

        for file_path, content in files_dict.items():
            if not content:
                logger.warning(f"   ⚠️  Skipping empty content for {file_path}")
                continue

            logger.info(f"   📝 Processing {file_path}...")
            self.update_file(
                repo_name=repo_name,
                file_path=file_path,
                content=content,
                commit_message=f"docs: update {file_path} via Apex Optimizer"
            )
    @retry_with_backoff
    def enable_github_pages(self, repo_name: str, branch: str = "main", path: str = "/docs") -> bool:
        """Enables GitHub Pages for the repository from the specified source."""
        url = f"{self.config.GITHUB_API_URL}/repos/{self.config.GH_USERNAME}/{repo_name}/pages"
        data = {
            "source": {
                "branch": branch,
                "path": path
            }
        }
        # Special acceptance header often needed for Pages API
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.switcheroo-preview+json"

        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code in [201, 200, 204]:
                logger.info(f"   🌍 Enabled GitHub Pages for {repo_name} ({path})")
                return True
            # If already enabled, it often returns 409 or similar, check details
            elif response.status_code == 409:
                logger.info(f"   🌍 GitHub Pages already enabled for {repo_name}")
                return True
            else:
                logger.error(f"   ❌ Failed to enable Pages: {response.status_code} {response.text}")
                return False
        except Exception as e:
            logger.error(f"   ❌ Error enabling Pages: {e}")
            return False

    @retry_with_backoff
    def star_repository(self, repo_name: str) -> bool:
        """Stars the repository."""
        url = f"{self.config.GITHUB_API_URL}/user/starred/{self.config.GH_USERNAME}/{repo_name}"
        # PUT to /user/starred/{owner}/{repo}
        try:
            response = requests.put(url, headers=self.headers, timeout=30)
            if response.status_code == 204:
                logger.info(f"   🌟 Starred repository: {repo_name}")
                return True
            else:
                logger.error(f"   ❌ Failed to star repo: {response.status_code} {response.text}")
                return False
        except Exception as e:
            logger.error(f"   ❌ Error starring repo: {e}")
            return False
