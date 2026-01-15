"""
Session Manager - Handles Jules session lifecycle with intelligent recovery.

Manages session creation, polling, auto-approval, and AI-based analysis
for stuck sessions using the UnifiedAIClient.
"""

import logging
import time
from typing import Any

from .ai import UnifiedAIClient
from .clients.jules import JulesClient

logger = logging.getLogger("SessionManager")


class SessionManager:
    """
    Manages Jules session lifecycle with intelligent recovery.
    """

    def __init__(self, jules: JulesClient, ai: UnifiedAIClient) -> None:
        self.jules = jules
        self.ai = ai


    def create_session(
        self,
        source_name: str,
        prompt: str,
        title: str,
        repo: str
    ) -> str | None:
        """
        Create a Jules session with error handling.

        Returns:
            session_id or None if failed
        """
        try:
            session = self.jules.create_session(
                source_name=source_name,
                prompt=prompt,
                title=title,
                starting_branch="main",
                auto_create_pr=True,
                require_plan_approval=False
            )

            if session:
                session_id = session.get("id", session.get("name", ""))
                logger.info(f"   🚀 [{repo}] Session created: {session_id[:20]}...")
                return session_id

            logger.warning(f"   ❌ [{repo}] Failed to create session")
            return None

        except Exception as e:
            logger.error(f"   ❌ [{repo}] Create error: {e}")
            return None

    def poll_session_once(self, session_id: str, repo: str) -> tuple[str, str]:
        """
        Poll a session ONCE and handle state transitions.

        Returns:
            (status, pr_url)
            Status: "WORKING", "COMPLETED", "FAILED", "APPROVED", "RESPONDED", "ANALYZED"
        """
        try:
            session = self.jules.get_session(session_id)
            if not session:
                return ("FAILED", "")

            state = session.get("state", "UNKNOWN")

            # Terminal states
            if state == "COMPLETED":
                pr_url = self._extract_pr_url(session)
                return ("COMPLETED", pr_url)

            if state == "FAILED":
                return ("FAILED", "")

            # Auto-approve plan
            if state == "AWAITING_PLAN_APPROVAL":
                logger.info(f"   📋 [{repo}] Auto-approving plan...")
                self.jules.approve_plan(session_id)
                return ("APPROVED", "")

            # Auto-respond with intelligent analysis
            if state == "AWAITING_USER_FEEDBACK":
                response = self._generate_intelligent_response(session_id, repo)
                logger.info(f"   💬 [{repo}] Auto-responding: {response[:50]}...")
                self.jules.send_message(session_id, response)
                return ("RESPONDED", "")

            # Still working
            return ("WORKING", "")

        except Exception as e:
            logger.error(f"   ❌ [{repo}] Poll error: {e}")
            return ("WORKING", "")  # Retry next iteration

    def _extract_pr_url(self, session: dict) -> str:
        """Extract PR URL from session outputs."""
        for output in session.get("outputs", []):
            if "pullRequest" in output:
                return output["pullRequest"].get("url", "")
        return ""

    def _generate_intelligent_response(self, session_id: str, repo: str) -> str:
        """
        Use AI to analyze session activities and generate intelligent response.
        Falls back to generic response if AI fails.
        """
        try:
            # Get session activities
            activities = self.jules.list_activities(session_id)

            if not activities:
                return "Proceed with your best judgment. Auto-approve all changes."

            # Extract last few activities for context
            recent_activities = activities[-5:] if len(activities) > 5 else activities
            context = "\n".join([
                f"- {act.get('type', 'UNKNOWN')}: {act.get('message', '')[:100]}"
                for act in recent_activities
            ])

            # Use UnifiedAI to analyze and generate response
            prompt = f"""<session_analysis>
Repository: {repo}
Recent Activities:
{context}
</session_analysis>

The Jules AI agent is waiting for user feedback. Based on the recent activities,
generate a SHORT, ACTIONABLE response (max 100 chars) that will help the agent proceed.

Examples:
- "Proceed with the current approach"
- "Use the first option and continue"
- "Auto-approve all changes"
- "Skip this step and move forward"

Response:"""

            result = self.ai.generate(
                prompt=prompt,
                system_prompt="You are a helpful assistant guiding code automation.",
                max_tokens=50,
                min_model_size=8  # Fast 8B+ models
            )

            if result.success and result.content and len(result.content.strip()) > 10:
                return result.content.strip()

        except Exception as e:
            logger.warning(f"   ⚠️ [{repo}] AI analysis failed: {e}")

        # Fallback response
        return "Proceed with your best judgment. Auto-approve all changes. Use first approach."

    def analyze_stuck_session(self, session_id: str, repo: str) -> dict:
        """
        Use AI to deeply analyze a stuck session and suggest recovery actions.

        Returns:
            {
                "status": "stuck" | "recoverable" | "failed",
                "reason": "explanation",
                "action": "suggested action"
            }
        """
        try:
            session = self.jules.get_session(session_id)
            activities = self.jules.list_activities(session_id)

            if not session or not activities:
                return {
                    "status": "failed",
                    "reason": "Cannot fetch session data",
                    "action": "Mark as failed"
                }

            # Build context for AI analysis
            state = session.get("state", "UNKNOWN")
            activity_summary = "\n".join([
                f"{i+1}. {act.get('type', 'UNKNOWN')}: {act.get('message', '')[:200]}"
                for i, act in enumerate(activities[-10:])
            ])

            prompt = f"""<stuck_session_analysis>
Repository: {repo}
Current State: {state}
Session ID: {session_id}

Last 10 Activities:
{activity_summary}
</stuck_session_analysis>

This Jules AI session appears to be stuck. Analyze the activities and determine:
1. Is it truly stuck or just slow?
2. What is the root cause?
3. What action should be taken?

Respond in JSON format:
{{
  "status": "stuck" | "recoverable" | "working",
  "reason": "brief explanation",
  "action": "specific action to take"
}}"""

            result = self.ai.generate_json(
                prompt=prompt,
                system_prompt="You are an expert at diagnosing automation issues.",
                max_tokens=200,
                min_model_size=70  # Use smarter 70B+ model for analysis
            )

            if result.success and result.json_content:
                return result.json_content

        except Exception as e:
            logger.error(f"   ❌ [{repo}] Stuck session analysis failed: {e}")

        # Fallback
        return {
            "status": "stuck",
            "reason": "Analysis failed",
            "action": "Continue polling or mark as failed after timeout"
        }