#!/usr/bin/env python3
"""
Modify Existing Repositories - Enhanced with Concurrent AI Analysis

Purpose:
- Deep repository analysis using multiple AI models
- Concurrent analysis and modification workflow
- Optimize README files, archive dead repos, manage visibility
- Uses all available AI providers for comprehensive review

Features:
- Multi-model parallel analysis for consensus-based decisions
- Fetches actual README content for deep analysis
- Concurrent processing with semaphore-based rate limiting
- Dry-run mode for safe testing
- Detailed statistics on provider utilization

Runs daily via GitHub Actions.
"""

import asyncio
import base64
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Add Root to Path
sys.path.append(str(Path(__file__).parent.parent))

from src.ai.unified_client import UnifiedAIClient
from src.core.config import Settings


# =============================================================================
# CONFIGURATION
# =============================================================================

GH_TOKEN = os.getenv("GH_TOKEN")
GH_USERNAME = "chirag127"
DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT", "5"))
MAX_REPOS_PER_RUN = int(os.getenv("MAX_REPOS_PER_RUN", "10"))
SINGLE_REPO = os.getenv("SINGLE_REPO", "")  # For testing single repo

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ModifyRepos")


# =============================================================================
# STATISTICS TRACKING
# =============================================================================

@dataclass
class ExecutionStats:
    """Track execution statistics."""
    repos_analyzed: int = 0
    repos_modified: int = 0
    actions_taken: dict[str, int] = field(default_factory=lambda: {
        "KEEP": 0, "OPTIMIZE": 0, "ARCHIVE": 0, "DELETE": 0, "MAKE_PUBLIC": 0, "SKIP": 0
    })
    models_used: dict[str, int] = field(default_factory=dict)
    providers_used: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)

    def log_model_used(self, model: str, provider: str) -> None:
        self.models_used[model] = self.models_used.get(model, 0) + 1
        self.providers_used[provider] = self.providers_used.get(provider, 0) + 1

    def print_summary(self) -> None:
        elapsed = time.time() - self.start_time
        logger.info("\n" + "=" * 60)
        logger.info("EXECUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Time Elapsed: {elapsed:.1f}s")
        logger.info(f"Repositories Analyzed: {self.repos_analyzed}")
        logger.info(f"Repositories Modified: {self.repos_modified}")
        logger.info(f"Dry Run Mode: {DRY_RUN}")
        logger.info("\nActions Taken:")
        for action, count in self.actions_taken.items():
            if count > 0:
                logger.info(f"  {action}: {count}")
        logger.info("\nModels Used:")
        for model, count in sorted(self.models_used.items(), key=lambda x: -x[1]):
            logger.info(f"  {model}: {count} calls")
        logger.info("\nProviders Used:")
        for provider, count in sorted(self.providers_used.items(), key=lambda x: -x[1]):
            logger.info(f"  {provider}: {count} calls")
        if self.errors:
            logger.info(f"\nErrors ({len(self.errors)}):")
            for err in self.errors[:5]:
                logger.info(f"  - {err}")
        logger.info("=" * 60)


stats = ExecutionStats()


# =============================================================================
# GITHUB API
# =============================================================================

def gh_api(method: str, endpoint: str, data: dict = None) -> requests.Response:
    """Make GitHub API request."""
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
    return requests.Response()


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


def get_repo_readme(name: str) -> str:
    """Fetch actual README content for deep analysis."""
    try:
        r = gh_api("GET", f"/repos/{GH_USERNAME}/{name}/readme")
        if r.status_code == 200:
            content = r.json().get("content", "")
            return base64.b64decode(content).decode("utf-8", errors="ignore")
    except Exception as e:
        logger.debug(f"Could not fetch README for {name}: {e}")
    return ""


def get_repo_languages(name: str) -> dict[str, int]:
    """Get language breakdown for repository."""
    try:
        r = gh_api("GET", f"/repos/{GH_USERNAME}/{name}/languages")
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return {}


def get_repo_commits(name: str, count: int = 5) -> list[dict]:
    """Get recent commits for activity analysis."""
    try:
        r = gh_api("GET", f"/repos/{GH_USERNAME}/{name}/commits?per_page={count}")
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return []


def is_repo_empty(name: str) -> bool:
    """Check if repo has no commits."""
    r = gh_api("GET", f"/repos/{GH_USERNAME}/{name}/commits?per_page=1")
    return r.status_code == 409 or not r.json()


# =============================================================================
# REPOSITORY ACTIONS
# =============================================================================

def archive_repo(name: str) -> bool:
    """Archive a repository."""
    if DRY_RUN:
        logger.info(f"  [DRY-RUN] Would archive: {name}")
        return True
    logger.info(f"  Archiving: {name}")
    r = gh_api("PATCH", f"/repos/{GH_USERNAME}/{name}", {"archived": True})
    return r.status_code == 200


def delete_repo(name: str) -> bool:
    """Delete a repository (careful!)."""
    if DRY_RUN:
        logger.info(f"  [DRY-RUN] Would delete: {name}")
        return True
    logger.info(f"  Deleting: {name}")
    r = gh_api("DELETE", f"/repos/{GH_USERNAME}/{name}")
    return r.status_code == 204


def make_public(name: str) -> bool:
    """Make repository public."""
    if DRY_RUN:
        logger.info(f"  [DRY-RUN] Would make public: {name}")
        return True
    logger.info(f"  Making public: {name}")
    r = gh_api("PATCH", f"/repos/{GH_USERNAME}/{name}", {"private": False})
    return r.status_code == 200


def make_private(name: str) -> bool:
    """Make repository private."""
    if DRY_RUN:
        logger.info(f"  [DRY-RUN] Would make private: {name}")
        return True
    logger.info(f"  Making private: {name}")
    r = gh_api("PATCH", f"/repos/{GH_USERNAME}/{name}", {"private": True})
    return r.status_code == 200


def update_repo_metadata(name: str, description: str = None, topics: list[str] = None) -> bool:
    """Update repo description and topics."""
    if DRY_RUN:
        logger.info(f"  [DRY-RUN] Would update metadata: {name}")
        if description:
            logger.info(f"    Description: {description[:100]}...")
        if topics:
            logger.info(f"    Topics: {topics[:5]}...")
        return True

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
# DEEP REPOSITORY ANALYSIS
# =============================================================================

@dataclass
class DeepAnalysis:
    """Comprehensive repository analysis result."""
    action: str = "KEEP"
    reason: str = ""
    confidence: float = 0.0
    project_quality: int = 5
    doc_quality: int = 5
    maintenance_status: str = "unknown"
    new_description: str | None = None
    topics: list[str] = field(default_factory=list)
    seo_suggestions: list[str] = field(default_factory=list)
    model_used: str = ""
    provider_used: str = ""


def build_deep_analysis_prompt(repo: dict, readme: str, languages: dict, commits: list) -> str:
    """Build comprehensive analysis prompt with all available context."""
    name = repo["name"]
    desc = repo.get("description", "") or ""
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    updated = repo.get("updated_at", "")
    created = repo.get("created_at", "")
    private = repo.get("private", False)
    archived = repo.get("archived", False)
    size_kb = repo.get("size", 0)
    default_branch = repo.get("default_branch", "main")
    has_issues = repo.get("has_issues", False)
    open_issues = repo.get("open_issues_count", 0)

    # Format languages
    lang_str = ", ".join([f"{lang}: {bytes_}B" for lang, bytes_ in languages.items()][:5]) or "Unknown"

    # Format recent activity
    activity = []
    for commit in commits[:3]:
        msg = commit.get("commit", {}).get("message", "")[:80]
        date = commit.get("commit", {}).get("author", {}).get("date", "")[:10]
        activity.append(f"  - [{date}] {msg}")
    activity_str = "\n".join(activity) if activity else "  No recent commits"

    # Truncate README
    readme_preview = readme[:4000] if readme else "[No README found]"

    return f"""Analyze this GitHub repository COMPREHENSIVELY using all available context.

## BASIC INFO
- Name: {name}
- Description: {desc or "[No description]"}
- Stars: {stars} | Forks: {forks} | Size: {size_kb}KB
- Created: {created[:10]} | Last Updated: {updated[:10]}
- Private: {private} | Archived: {archived}
- Default Branch: {default_branch}
- Open Issues: {open_issues}

## LANGUAGES
{lang_str}

## RECENT ACTIVITY
{activity_str}

## README CONTENT (first 4000 chars)
```
{readme_preview}
```

## ANALYSIS REQUIRED

Provide a DETAILED analysis covering:

1. **PROJECT_QUALITY** (1-10): Code quality indicators from README and languages
2. **DOC_QUALITY** (1-10): README completeness, clarity, installation instructions
3. **MAINTENANCE_STATUS**: "active" / "stale" (3-12 months) / "abandoned" (>12 months)
4. **SEO_SCORE** (1-10): Current discoverability and keyword usage
5. **RECOMMENDED_ACTION**: One of:
   - KEEP: Repository is valuable, well-maintained, keep as is
   - OPTIMIZE: Needs better description/topics for SEO and visibility
   - ARCHIVE: Old/abandoned project that should be archived
   - DELETE: Spam/test/empty/worthless repo (ONLY if stars=0 AND forks=0)
   - MAKE_PUBLIC: Private repo that should be made public for visibility

6. **OPTIMIZATION_DETAILS** (if action is OPTIMIZE):
   - new_description: SEO-optimized description (max 250 chars)
   - topics: Array of 15-20 relevant lowercase tags

7. **CONFIDENCE** (0.0-1.0): How confident are you in this recommendation?

Return ONLY valid JSON:
{{
    "action": "KEEP|OPTIMIZE|ARCHIVE|DELETE|MAKE_PUBLIC",
    "reason": "Detailed explanation of recommendation",
    "confidence": 0.95,
    "project_quality": 7,
    "doc_quality": 8,
    "maintenance_status": "active|stale|abandoned",
    "seo_score": 6,
    "new_description": "SEO-optimized description if OPTIMIZE",
    "topics": ["topic1", "topic2", "..."],
    "seo_suggestions": ["Suggestion 1", "Suggestion 2"]
}}"""


def analyze_repo_deep(repo: dict, ai: UnifiedAIClient) -> DeepAnalysis:
    """Perform deep AI analysis of a repository."""
    name = repo["name"]
    archived = repo.get("archived", False)

    if archived:
        return DeepAnalysis(action="SKIP", reason="Already archived", confidence=1.0)

    # Check if empty first (fast path)
    if is_repo_empty(name):
        return DeepAnalysis(
            action="DELETE",
            reason="Empty repository with no commits",
            confidence=1.0
        )

    # Fetch comprehensive repo data
    readme = get_repo_readme(name)
    languages = get_repo_languages(name)
    commits = get_repo_commits(name, 5)

    # Build detailed prompt
    prompt = build_deep_analysis_prompt(repo, readme, languages, commits)

    # Use AI with large model preference for complex analysis
    result = ai.generate_json(
        prompt=prompt,
        system_prompt="You are an expert GitHub repository analyst and SEO specialist. Analyze repositories thoroughly and provide actionable recommendations.",
        max_tokens=2000,
        min_model_size=32  # Prefer 32B+ models for complex reasoning
    )

    if result.success and result.json_content:
        data = result.json_content
        analysis = DeepAnalysis(
            action=data.get("action", "KEEP"),
            reason=data.get("reason", ""),
            confidence=data.get("confidence", 0.5),
            project_quality=data.get("project_quality", 5),
            doc_quality=data.get("doc_quality", 5),
            maintenance_status=data.get("maintenance_status", "unknown"),
            new_description=data.get("new_description"),
            topics=data.get("topics", []),
            seo_suggestions=data.get("seo_suggestions", []),
            model_used=result.model_used,
            provider_used=result.provider_used or _extract_provider(result.model_used)
        )

        # Track statistics
        if result.model_used:
            stats.log_model_used(result.model_used, analysis.provider_used)

        return analysis

    # Fallback on failure
    logger.warning(f"AI analysis failed for {name}: {result.error}")
    return DeepAnalysis(
        action="KEEP",
        reason=f"AI analysis failed: {result.error}. Keeping safe.",
        confidence=0.1
    )


def _extract_provider(model_name: str) -> str:
    """Extract provider name from model identifier."""
    if "/" in model_name:
        return model_name.split("/")[0]
    providers = ["cerebras", "groq", "gemini", "mistral", "nvidia", "cloudflare"]
    model_lower = model_name.lower()
    for p in providers:
        if p in model_lower:
            return p
    return "unknown"


# =============================================================================
# CONCURRENT PROCESSING
# =============================================================================

def process_single_repo(repo: dict, ai: UnifiedAIClient) -> dict:
    """Process a single repository: analyze and act immediately."""
    name = repo["name"]
    logger.info(f"\n{'='*50}")
    logger.info(f"Analyzing: {name}")
    logger.info(f"{'='*50}")

    try:
        # Deep analysis
        analysis = analyze_repo_deep(repo, ai)
        stats.repos_analyzed += 1

        action = analysis.action
        stats.actions_taken[action] = stats.actions_taken.get(action, 0) + 1

        logger.info(f"  Model: {analysis.model_used or 'unknown'}")
        logger.info(f"  Action: {action} (confidence: {analysis.confidence:.0%})")
        logger.info(f"  Quality: project={analysis.project_quality}/10, docs={analysis.doc_quality}/10")
        logger.info(f"  Status: {analysis.maintenance_status}")
        logger.info(f"  Reason: {analysis.reason[:150]}...")

        # Execute action immediately (concurrent analysis + action)
        success = execute_action(repo, analysis)

        if success and action not in ["KEEP", "SKIP"]:
            stats.repos_modified += 1

        return {
            "repo": name,
            "action": action,
            "success": success,
            "analysis": analysis
        }

    except Exception as e:
        error_msg = f"Error processing {name}: {e}"
        logger.error(error_msg)
        stats.errors.append(error_msg)
        return {"repo": name, "action": "ERROR", "success": False, "error": str(e)}


def execute_action(repo: dict, analysis: DeepAnalysis) -> bool:
    """Execute the recommended action for a repository."""
    name = repo["name"]
    action = analysis.action

    if action == "KEEP":
        logger.info(f"  → Keeping {name} as is")
        return True

    elif action == "SKIP":
        logger.info(f"  → Skipping {name}")
        return True

    elif action == "OPTIMIZE":
        logger.info(f"  → Optimizing {name}")
        return update_repo_metadata(
            name,
            description=analysis.new_description,
            topics=analysis.topics
        )

    elif action == "ARCHIVE":
        logger.info(f"  → Archiving {name}")
        return archive_repo(name)

    elif action == "DELETE":
        # Safety check: only delete if truly worthless
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        if stars == 0 and forks == 0:
            logger.info(f"  → Deleting {name} (no stars/forks)")
            return delete_repo(name)
        else:
            logger.info(f"  → Archiving instead of deleting {name} (has stars/forks)")
            return archive_repo(name)

    elif action == "MAKE_PUBLIC":
        logger.info(f"  → Making {name} public")
        return make_public(name)

    return True


def process_repos_concurrent(repos: list[dict], ai: UnifiedAIClient) -> list[dict]:
    """Process multiple repositories concurrently."""
    results = []

    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        futures = {executor.submit(process_single_repo, repo, ai): repo for repo in repos}

        for future in futures:
            try:
                result = future.result(timeout=120)
                results.append(result)
            except Exception as e:
                repo = futures[future]
                error_msg = f"Concurrent processing error for {repo['name']}: {e}"
                logger.error(error_msg)
                stats.errors.append(error_msg)
                results.append({"repo": repo["name"], "action": "ERROR", "success": False})

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    if not GH_TOKEN:
        logger.error("GH_TOKEN not set")
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("MODIFY EXISTING REPOSITORIES - Enhanced Concurrent Analysis")
    logger.info("=" * 60)
    logger.info(f"Mode: {'DRY-RUN (no changes)' if DRY_RUN else 'LIVE (will modify repos)'}")
    logger.info(f"Max Concurrent: {MAX_CONCURRENT}")
    logger.info(f"Max Repos Per Run: {MAX_REPOS_PER_RUN}")

    # Initialize AI client
    ai = UnifiedAIClient()
    ai.print_status()

    # Get repositories
    if SINGLE_REPO:
        logger.info(f"\nSingle repo mode: {SINGLE_REPO}")
        repo_data = gh_api("GET", f"/repos/{GH_USERNAME}/{SINGLE_REPO}")
        if repo_data.status_code != 200:
            logger.error(f"Repository not found: {SINGLE_REPO}")
            sys.exit(1)
        repos = [repo_data.json()]
    else:
        repos = get_all_repos()

    # Filter to active (non-archived) repos
    active_repos = [r for r in repos if not r.get("archived", False)]
    logger.info(f"\nProcessing {min(len(active_repos), MAX_REPOS_PER_RUN)} of {len(active_repos)} active repositories...")

    # Process repos concurrently
    repos_to_process = active_repos[:MAX_REPOS_PER_RUN]
    results = process_repos_concurrent(repos_to_process, ai)

    # Print summary
    stats.print_summary()

    # Print action summary
    logger.info("\nACTION SUMMARY:")
    for result in results:
        status = "✓" if result.get("success") else "✗"
        logger.info(f"  [{status}] {result['repo']}: {result['action']}")

    logger.info("\nDone!")

    if DRY_RUN:
        logger.info("\n⚠️  DRY-RUN MODE: No actual changes were made.")
        logger.info("   Set DRY_RUN=false to apply changes.")


if __name__ == "__main__":
    # Handle command line args for single repo testing
    if len(sys.argv) > 1:
        if sys.argv[1] == "--repo" and len(sys.argv) > 2:
            os.environ["SINGLE_REPO"] = sys.argv[2]
            SINGLE_REPO = sys.argv[2]
        elif sys.argv[1] == "--dry-run":
            os.environ["DRY_RUN"] = "true"
            DRY_RUN = True

    main()
