#!/usr/bin/env python3
"""
GitHub PR Batch Closer
A production-ready script to batch close Pull Requests across all repositories for a GitHub user.

Author: Chirag Singhal (chirag127)
License: MIT
"""

import logging
import os
import re
import sys
import time
from dataclasses import dataclass

from colorama import Fore, Style
from colorama import init as colorama_init
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("PRBatchCloser")

try:
    from github import Auth, Github, GithubException, RateLimitExceededException
    from github.PullRequest import PullRequest
    from github.Repository import Repository
except ImportError as e:
    logger.error(f"Error: Required dependency not found: {e}")
    logger.error("Please install dependencies using: pip install -r requirements.txt")
    sys.exit(1)


@dataclass
class CloseStats:
    """Statistics for close operations."""

    total_repos: int = 0
    total_prs: int = 0
    successful_closes: int = 0
    skipped_already_closed: int = 0
    failed_permissions: int = 0
    failed_other: int = 0
    dry_run_skipped: int = 0


class PRBatchCloser:
    """Batch close Pull Requests across GitHub repositories."""

    def __init__(
        self,
        token: str,
        dry_run: bool = True,
        repo_filter: str | None = None,
        exclude_archived: bool = True,
        max_prs: int | None = None,
    ) -> None:
        """
        Initialize the PR Batch Closer.

        Args:
            token: GitHub Personal Access Token
            dry_run: If True, only list what would happen without closing
            repo_filter: Regex pattern to filter repository names
            exclude_archived: Skip archived repositories
            max_prs: Maximum number of PRs to process (None for unlimited)
        """
        self.token = token
        self.dry_run = dry_run
        self.repo_filter = re.compile(repo_filter) if repo_filter else None
        self.exclude_archived = exclude_archived
        self.max_prs = max_prs
        self.stats = CloseStats()
        self.github: Github | None = None

        # Initialize colorama for cross-platform colored output
        colorama_init(autoreset=True)

    def log_info(self, message: str) -> None:
        """Log informational message in cyan."""
        logger.info(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")

    def log_success(self, message: str) -> None:
        """Log success message in green."""
        logger.info(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")

    def log_warning(self, message: str) -> None:
        """Log warning message in yellow."""
        logger.warning(f"{Fore.YELLOW}[SKIPPED]{Style.RESET_ALL} {message}")

    def log_error(self, message: str) -> None:
        """Log error message in red."""
        logger.error(f"{Fore.RED}[FAILED]{Style.RESET_ALL} {message}")

    def log_dry_run(self, message: str) -> None:
        """Log dry-run message in yellow."""
        logger.info(f"{Fore.YELLOW}[DRY-RUN]{Style.RESET_ALL} {message}")

    def log_scanning(self, message: str) -> None:
        """Log scanning message in cyan."""
        logger.info(f"{Fore.CYAN}[SCANNING]{Style.RESET_ALL} {message}")

    def authenticate(self) -> bool:
        """
        Authenticate with GitHub API.

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            self.log_info("Authenticating with GitHub API...")
            auth = Auth.Token(self.token)
            self.github = Github(auth=auth)

            # Test authentication by getting user info
            user = self.github.get_user()
            username = user.login

            self.log_success(f"Authenticated as: {username}")

            # Check rate limit
            try:
                rate_limit = self.github.get_rate_limit()
                if hasattr(rate_limit, "core"):
                    core_remaining = rate_limit.core.remaining
                    core_limit = rate_limit.core.limit
                elif hasattr(rate_limit, "rate"):
                    core_remaining = rate_limit.rate.remaining
                    core_limit = rate_limit.rate.limit
                else:
                    return True

                if core_remaining < 100:
                    self.log_warning(
                        f"Low API rate limit: {core_remaining}/{core_limit} requests remaining"
                    )
                else:
                    self.log_info(
                        f"API rate limit: {core_remaining}/{core_limit} requests remaining"
                    )
            except Exception as rate_error:
                self.log_warning(f"Could not check rate limit: {rate_error}")

            return True

        except GithubException as e:
            if e.status == 401:
                self.log_error("Authentication failed: Invalid token")
            else:
                self.log_error(f"GitHub API error: {e.data.get('message', str(e))}")
            return False
        except Exception as e:
            self.log_error(f"Unexpected error during authentication: {e!s}")
            return False

    def should_process_repo(self, repo: Repository) -> bool:
        """
        Determine if a repository should be processed.
        """
        if self.exclude_archived and repo.archived:
            return False

        if self.repo_filter and not self.repo_filter.search(repo.full_name):
            return False

        return True

    def close_pull_request(self, pr: PullRequest, repo: Repository) -> tuple[bool, str]:
        """
        Attempt to close a pull request.
        """
        pr_info = f"PR #{pr.number}: {pr.title}"

        if pr.state == "closed":
            self.stats.skipped_already_closed += 1
            return False, f"{pr_info} (already closed)"

        if self.dry_run:
            self.stats.dry_run_skipped += 1
            return True, f"{pr_info} [Would Close]"

        try:
            pr.edit(state="closed")
            self.stats.successful_closes += 1
            return True, f"{pr_info} ✓ (Closed)"

        except GithubException as e:
            if e.status == 403:
                self.stats.failed_permissions += 1
                return False, f"{pr_info} (permission denied)"
            else:
                self.stats.failed_other += 1
                error_msg = (
                    e.data.get("message", str(e)) if hasattr(e, "data") else str(e)
                )
                return False, f"{pr_info} (error: {error_msg})"

    def handle_rate_limit(self) -> None:
        """Handle GitHub API rate limiting with exponential backoff."""
        if not self.github:
            return

        try:
            rate_limit = self.github.get_rate_limit()
            if hasattr(rate_limit, "core"):
                remaining = rate_limit.core.remaining
                reset_time = rate_limit.core.reset
            elif hasattr(rate_limit, "rate"):
                remaining = rate_limit.rate.remaining
                reset_time = rate_limit.rate.reset
            else:
                return

            if remaining < 10:
                sleep_time = (reset_time.timestamp() - time.time()) + 10
                if sleep_time > 0:
                    self.log_warning(
                        f"Rate limit nearly exceeded. Sleeping for {int(sleep_time)} seconds..."
                    )
                    time.sleep(sleep_time)
        except Exception as e:
            self.log_warning(f"Could not check rate limit: {e}")

    def _process_repo_prs(self, repo: Repository, current_total_processed: int) -> int:
        """
        Process PRs for a single repository.
        Returns the number of PRs processed.
        """
        try:
            open_prs = list(repo.get_pulls(state="open"))
        except GithubException as e:
            self.log_error(
                f"Could not access PRs in {repo.full_name}: {e.data.get('message', str(e))}"
            )
            return 0

        if not open_prs:
            return 0

        self.log_scanning(
            f"Repository: {repo.full_name} ({len(open_prs)} open PR{'s' if len(open_prs) != 1 else ''})"
        )

        processed_count = 0
        for pr in open_prs:
            if self.max_prs and (current_total_processed + processed_count) >= self.max_prs:
                break

            self.stats.total_prs += 1
            processed_count += 1

            success, message = self.close_pull_request(pr, repo)

            if self.dry_run:
                self.log_dry_run(f"Would close {message}")
            elif success:
                self.log_success(f"Closed {message}")
            else:
                self.log_warning(message)

            self.handle_rate_limit()

        return processed_count

    def process_repositories(self) -> None:
        """Process all repositories and close their open PRs."""
        if not self.github:
            return

        try:
            user = self.github.get_user()
            repos = user.get_repos(type="owner", sort="updated", direction="desc")

            self.log_info(f"Scanning repositories for {user.login}...")

            if self.dry_run:
                self.log_dry_run("DRY-RUN MODE: No PRs will be actually closed")

            total_prs_processed = 0

            for repo in repos:
                if self.max_prs and total_prs_processed >= self.max_prs:
                    self.log_info(
                        f"Reached maximum PR limit ({self.max_prs}). Stopping."
                    )
                    break

                if not self.should_process_repo(repo):
                    continue

                self.stats.total_repos += 1
                total_prs_processed += self._process_repo_prs(repo, total_prs_processed)

        except RateLimitExceededException:
            self.log_error("GitHub API rate limit exceeded. Please try again later.")
        except Exception as e:
            self.log_error(f"Unexpected error while processing repositories: {e!s}")

    def print_summary(self) -> None:
        """Print summary statistics."""
        print()
        print(f"{Fore.MAGENTA}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'SUMMARY':^60}{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}{'=' * 60}{Style.RESET_ALL}")
        print()
        print(f"  Total Repositories Scanned: {self.stats.total_repos}")
        print(f"  Total PRs Found: {self.stats.total_prs}")
        print()

        if self.dry_run:
            print(
                f"  {Fore.YELLOW}PRs That Would Be Closed: {self.stats.dry_run_skipped}{Style.RESET_ALL}"
            )
            print(
                f"  {Fore.YELLOW}PRs Already Closed: {self.stats.skipped_already_closed}{Style.RESET_ALL}"
            )
        else:
            print(
                f"  {Fore.GREEN}Successfully Closed: {self.stats.successful_closes}{Style.RESET_ALL}"
            )
            print(
                f"  {Fore.YELLOW}Skipped (Already Closed): {self.stats.skipped_already_closed}{Style.RESET_ALL}"
            )
            print(
                f"  {Fore.RED}Failed (Permissions): {self.stats.failed_permissions}{Style.RESET_ALL}"
            )
            print(
                f"  {Fore.RED}Failed (Other Errors): {self.stats.failed_other}{Style.RESET_ALL}"
            )

        print()
        print(f"{Fore.MAGENTA}{'=' * 60}{Style.RESET_ALL}")

    def run(self) -> int:
        """
        Execute the batch close operation.

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        if not self.authenticate():
            return 1

        self.process_repositories()
        self.print_summary()
        return 0


def main() -> int:
    """Main entry point."""
    token = os.getenv("GH_TOKEN")
    if not token:
        logger.error("❌ CRITICAL: GH_TOKEN is missing in .env")
        return 1

    # Default to DRY RUN for safety
    dry_run = os.getenv("DRY_RUN", "false").lower() == "true"

    closer = PRBatchCloser(
        token=token,
        dry_run=dry_run,
        repo_filter=None,
        exclude_archived=True,
        max_prs=None,
    )

    return closer.run()


if __name__ == "__main__":
    sys.exit(main())
