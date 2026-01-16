"""
Jules REST API Client for Repository Optimization.

Integrates with Google Jules API to automatically audit and update
GitHub repositories according to AGENTS.md standards.
Features: Auto-approve plans, auto-create PRs, retry on failures.
"""

import json
import logging
import os
import time
from typing import Any

import requests

from src.core.config import Settings

logger = logging.getLogger("JulesOptimizer")


class JulesClient:
    """
    Client for Google Jules REST API.
    Handles authentication, session management, and polling.
    """

    def __init__(self, config: Settings) -> None:
        self.config = config
        self.api_key = config.JULES_API_KEY
        self.base_url = config.JULES_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json"
        })

        if not self.api_key:
            logger.warning("   ⚠️  JULES_API_KEY not set. Jules integration disabled.")

    def _request(
        self, method: str, endpoint: str, data: dict | None = None
    ) -> dict | None:
        """Make a SINGLE request to Jules API - NO RETRIES."""
        url = f"{self.base_url}{endpoint}"

        try:
            if method == "GET":
                response = self.session.get(url, timeout=60)
            elif method == "POST":
                response = self.session.post(url, json=data, timeout=120)
            elif method == "DELETE":
                response = self.session.delete(url, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")

            if response.status_code == 200:
                return response.json() if response.text else {}
            elif response.status_code == 429:
                logger.warning(f"   ⚠️ Rate limited (429). FAIL - no retry.")
                return None
            elif response.status_code >= 500:
                logger.warning(f"   ⚠️ Server error {response.status_code}. FAIL - no retry.")
                return None
            else:
                logger.error(f"   ❌ API Error {response.status_code}: {response.text[:200]}")
                return None

        except requests.exceptions.Timeout:
            logger.warning(f"   ⚠️ Request timeout. FAIL - no retry.")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"   ❌ Request failed: {e}")
            return None


    # =========================================================================
    # Sources API
    # =========================================================================

    def list_sources(self, page_size: int = 100) -> list[dict]:
        """
        List all connected GitHub repositories (sources).
        Handles pagination automatically.
        """
        if not self.api_key:
            return []

        sources = []
        page_token = None

        while True:
            endpoint = f"/sources?pageSize={page_size}"
            if page_token:
                endpoint += f"&pageToken={page_token}"

            response = self._request("GET", endpoint)
            if not response:
                break

            sources.extend(response.get("sources", []))
            page_token = response.get("nextPageToken")

            if not page_token:
                break

        logger.info(f"   📂 Found {len(sources)} connected repositories")
        return sources

    def get_source(self, source_name: str) -> dict | None:
        """Get details for a specific source."""
        if not self.api_key:
            return None
        return self._request("GET", f"/{source_name}")

    # =========================================================================
    # Sessions API
    # =========================================================================

    def create_session(
        self,
        source_name: str,
        prompt: str,
        title: str = "AGENTS.md Compliance Update",
        starting_branch: str = "main",
        auto_create_pr: bool = True,
        require_plan_approval: bool = False
    ) -> dict | None:
        """
        Create a new optimization session for a repository.

        Args:
            source_name: Full source name (e.g., "sources/github-owner-repo")
            prompt: The task description for Jules
            title: Session title (appears in PR)
            starting_branch: Branch to start from (default: main)
            auto_create_pr: Automatically create PR when done
            require_plan_approval: If False, plans are auto-approved
        """
        if not self.api_key:
            return None

        data = {
            "prompt": prompt,
            "title": title,
            "sourceContext": {
                "source": source_name,
                "githubRepoContext": {
                    "startingBranch": starting_branch
                }
            },
            "requirePlanApproval": require_plan_approval
        }

        if auto_create_pr:
            data["automationMode"] = "AUTO_CREATE_PR"

        response = self._request("POST", "/sessions", data)

        if response:
            session_id = response.get("id", response.get("name", ""))
            logger.info(f"   🚀 Created session: {session_id}")

        return response

    def get_session(self, session_id: str) -> dict | None:
        """Get session details and current status."""
        if not self.api_key:
            return None
        return self._request("GET", f"/sessions/{session_id}")

    def list_sessions(self, page_size: int = 30) -> list[dict]:
        """List all sessions."""
        if not self.api_key:
            return []

        response = self._request("GET", f"/sessions?pageSize={page_size}")
        return response.get("sessions", []) if response else []

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if not self.api_key:
            return False
        result = self._request("DELETE", f"/sessions/{session_id}")
        return result is not None

    def approve_plan(self, session_id: str) -> bool:
        """Approve a pending plan (only if requirePlanApproval was True)."""
        if not self.api_key:
            return False
        result = self._request("POST", f"/sessions/{session_id}:approvePlan", {})
        return result is not None

    def send_message(self, session_id: str, message: str) -> bool:
        """Send a follow-up message to an active session."""
        if not self.api_key:
            return False
        result = self._request("POST", f"/sessions/{session_id}:sendMessage", {
            "prompt": message
        })
        return result is not None

    # =========================================================================
    # Activities API
    # =========================================================================

    def list_activities(self, session_id: str, page_size: int = 50) -> list[dict]:
        """List all activities for a session."""
        if not self.api_key:
            return []

        response = self._request(
            "GET",
            f"/sessions/{session_id}/activities?pageSize={page_size}"
        )
        return response.get("activities", []) if response else []

    # =========================================================================
    # Polling & Completion (NO SLEEP - Fast polling)
    # =========================================================================

    def wait_for_completion(
        self,
        session_id: str,
        poll_interval: int = 1,  # Reduced from 30 - poll fast
        max_wait: int = 3600  # 1 hour max
    ) -> dict | None:
        """
        Poll a session until it completes or fails.
        NO SLEEP - polls as fast as possible.

        Returns:
            Final session state, or None if timeout/error
        """
        if not self.api_key:
            return None

        start_time = time.time()
        terminal_states = {"COMPLETED", "FAILED"}

        while (time.time() - start_time) < max_wait:
            session = self.get_session(session_id)
            if not session:
                logger.error(f"   ❌ Failed to fetch session {session_id}")
                return None

            state = session.get("state", "UNKNOWN")
            title = session.get("title", "Untitled")

            if state in terminal_states:
                if state == "COMPLETED":
                    outputs = session.get("outputs", [])
                    pr_url = None
                    for output in outputs:
                        if "pullRequest" in output:
                            pr_url = output["pullRequest"].get("url")
                            break

                    if pr_url:
                        logger.info(f"   ✅ {title}: COMPLETED → PR: {pr_url}")
                    else:
                        logger.info(f"   ✅ {title}: COMPLETED (no PR)")
                else:
                    logger.warning(f"   ❌ {title}: FAILED")

                return session

            elif state == "AWAITING_PLAN_APPROVAL":
                logger.info(f"   📋 Auto-approving plan for {title}...")
                self.approve_plan(session_id)

            elif state == "AWAITING_USER_FEEDBACK":
                # Auto-respond to keep it moving
                logger.info(f"   💬 Auto-responding to {title}...")
                self.send_message(session_id, "Proceed with the current plan. Auto-approve all changes.")

            else:
                logger.debug(f"   ⏳ {title}: {state}...")

            # No sleep - continue polling immediately

        logger.error(f"   ⏰ Session {session_id} timed out after {max_wait}s")
        return None

    # =========================================================================
    # Helper Methods
    # =========================================================================

    def parse_source_name(self, source: dict) -> tuple[str, str]:
        """Extract owner and repo from a source object."""
        github_repo = source.get("githubRepo", {})
        owner = github_repo.get("owner", "")
        repo = github_repo.get("repo", "")
        return owner, repo

    def is_available(self) -> bool:
        """Check if Jules API is configured and accessible."""
        if not self.api_key:
            return False

        # Try a simple API call to verify connectivity
        try:
            response = self._request("GET", "/sources?pageSize=1")
            return response is not None
        except Exception:
            return False
