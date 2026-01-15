#!/usr/bin/env python3
"""
GitHub PR Batch Merger
A production-ready script to batch merge Pull Requests across all repositories for a GitHub user.

Author: Chirag Singhal (chirag127)
License: MIT
"""

import argparse
import logging
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
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
logger = logging.getLogger("PRBatchMerger")

try:
    from github import Auth, Github, GithubException, RateLimitExceededException
    from github.PullRequest import PullRequest
    from github.Repository import Repository
except ImportError as e:
    logger.error(f"Error: Required dependency not found: {e}")
    logger.error("Please install dependencies using: pip install -r requirements.txt")
    sys.exit(1)


@dataclass
class MergeStats:
    """Statistics for merge operations."""

    total_repos: int = 0
    total_prs: int = 0
    successful_merges: int = 0
    skipped_conflicts: int = 0
    skipped_already_merged: int = 0
    failed_permissions: int = 0
    failed_other: int = 0
    dry_run_skipped: int = 0



@dataclass
class MergerConfig:
    """Configuration for the PR Batch Merger."""
    token: str
    dry_run: bool = True
    merge_method: str = "merge"
    repo_filter: str | None = None
    exclude_archived: bool = True
    max_prs: int | None = None
    max_workers: int = 10


class PRBatchMerger:
    """Batch merge Pull Requests across GitHub repositories."""

    def __init__(self, config: MergerConfig) -> None:
        """
        Initialize the PR Batch Merger.

        Args:
            config: Configuration object
        """
        self.config = config
        self.repo_filter = re.compile(config.repo_filter) if config.repo_filter else None
        self.stats = MergeStats()
        self.github: Github | None = None

        # Thread safety locks
        self._log_lock = threading.Lock()
        self._stats_lock = threading.Lock()

        # Initialize colorama for cross-platform colored output
        colorama_init(autoreset=True)

    def log_info(self, message: str) -> None:
        """Log informational message in cyan."""
        with self._log_lock:
            logger.info(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} {message}")

    def log_success(self, message: str) -> None:
        """Log success message in green."""
        with self._log_lock:
            logger.info(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} {message}")

    def log_warning(self, message: str) -> None:
        """Log warning message in yellow."""
        with self._log_lock:
            logger.warning(f"{Fore.YELLOW}[SKIPPED]{Style.RESET_ALL} {message}")

    def log_error(self, message: str) -> None:
        """Log error message in red."""
        with self._log_lock:
            logger.error(f"{Fore.RED}[FAILED]{Style.RESET_ALL} {message}")

    def log_dry_run(self, message: str) -> None:
        """Log dry-run message in yellow."""
        with self._log_lock:
            logger.info(f"{Fore.YELLOW}[DRY-RUN]{Style.RESET_ALL} {message}")

    def log_scanning(self, message: str) -> None:
        """Log scanning message in cyan."""
        with self._log_lock:
            logger.info(f"{Fore.CYAN}[SCANNING]{Style.RESET_ALL} {message}")

    def authenticate(self) -> bool:
        """
        Authenticate with GitHub API.

        Returns:
            True if authentication successful, False otherwise
        """
        try:
            self.log_info("Authenticating with GitHub API...")
            auth = Auth.Token(self.config.token)
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
        if self.config.exclude_archived and repo.archived:
            return False

        if self.repo_filter and not self.repo_filter.search(repo.full_name):
            return False

        return True

    def _handle_merge_exception(self, e: GithubException, pr_info: str) -> tuple[bool, str]:
        """Handle exceptions during merge."""
        if e.status == 405:
            with self._stats_lock:
                self.stats.skipped_conflicts += 1
            return (
                False,
                f"{pr_info} (not mergeable: {e.data.get('message', 'unknown error')})",
            )
        elif e.status == 403:
            with self._stats_lock:
                self.stats.failed_permissions += 1
            return False, f"{pr_info} (permission denied)"
        else:
            with self._stats_lock:
                self.stats.failed_other += 1
            error_msg = (
                e.data.get("message", str(e)) if hasattr(e, "data") else str(e)
            )
            return False, f"{pr_info} (error: {error_msg})"

    def merge_pull_request(self, pr: PullRequest, repo: Repository) -> tuple[bool, str]:
        """
        Attempt to merge a pull request.
        Handles draft PRs by converting them to ready-for-review first.
        """
        pr_info = f"PR #{pr.number}: {pr.title}"

        if pr.merged:
            with self._stats_lock:
                self.stats.skipped_already_merged += 1
            return False, f"{pr_info} (already merged)"

        # Handle draft PRs - convert to ready-for-review first
        if pr.draft:
            self.log_info(f"Converting draft PR to ready: {pr_info}")
            try:
                # Use GraphQL API to mark as ready for review
                self._mark_pr_ready_for_review(pr)
                # Refresh PR state
                pr = repo.get_pull(pr.number)
            except Exception as e:
                self.log_warning(f"Could not convert draft: {e}")
                # Continue anyway - try to merge

        # Check mergeable after converting from draft
        if pr.mergeable is False:
            with self._stats_lock:
                self.stats.skipped_conflicts += 1
            return False, f"{pr_info} (merge conflicts detected)"

        if self.config.dry_run:
            with self._stats_lock:
                self.stats.dry_run_skipped += 1
            merge_status = "✓ Can merge" if pr.mergeable else "✗ Has conflicts"
            return True, f"{pr_info} [{merge_status}]"

        try:
            result = pr.merge(merge_method=self.config.merge_method)

            if result.merged:
                with self._stats_lock:
                    self.stats.successful_merges += 1
                return True, f"{pr_info} ✓"
            else:
                with self._stats_lock:
                    self.stats.failed_other += 1
                return False, f"{pr_info} (merge failed: {result.message})"

        except GithubException as e:
            return self._handle_merge_exception(e, pr_info)

    def _mark_pr_ready_for_review(self, pr: PullRequest) -> None:
        """
        Convert a draft PR to ready-for-review using GitHub GraphQL API.
        """
        import requests

        query = """
        mutation MarkPRReady($pullRequestId: ID!) {
            markPullRequestReadyForReview(input: {pullRequestId: $pullRequestId}) {
                pullRequest {
                    isDraft
                }
            }
        }
        """

        headers = {
            "Authorization": f"Bearer {self.config.token}",
            "Content-Type": "application/json"
        }

        # Get the PR node ID
        node_id = pr.raw_data.get("node_id", pr.node_id if hasattr(pr, 'node_id') else None)
        if not node_id:
            raise ValueError("Could not get PR node_id")

        response = requests.post(
            "https://api.github.com/graphql",
            headers=headers,
            json={"query": query, "variables": {"pullRequestId": node_id}},
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"GraphQL error: {response.text[:200]}")

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
            if self.config.max_prs and (current_total_processed + processed_count) >= self.config.max_prs:
                break

            with self._stats_lock:
                self.stats.total_prs += 1
            processed_count += 1

            success, message = self.merge_pull_request(pr, repo)

            if self.config.dry_run:
                self.log_dry_run(f"Would merge {message}")
            elif success:
                self.log_success(f"Merged {message}")
            else:
                self.log_warning(message)

            self.handle_rate_limit()

        return processed_count

    def process_repositories(self) -> None:
        """Process all repositories and merge their open PRs concurrently."""
        if not self.github:
            return

        try:
            user = self.github.get_user()
            repos = list(user.get_repos(type="owner", sort="updated", direction="desc"))

            self.log_info(f"Scanning {len(repos)} repositories for {user.login}...")

            if self.config.dry_run:
                self.log_dry_run("DRY-RUN MODE: No PRs will be actually merged")

            total_prs_processed = 0

            # Use ThreadPoolExecutor for concurrent processing
            with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
                futures = {}
                for repo in repos:
                    if self.config.max_prs and total_prs_processed >= self.config.max_prs:
                        self.log_info(
                            f"Reached maximum PR limit ({self.config.max_prs}). Stopping new tasks."
                        )
                        break

                    if not self.should_process_repo(repo):
                        continue

                    with self._stats_lock:
                        self.stats.total_repos += 1

                    # Submit task
                    future = executor.submit(self._process_repo_prs, repo, total_prs_processed)
                    futures[future] = repo.full_name

                # Wait for completion
                for future in as_completed(futures):
                    try:
                        count = future.result()
                        total_prs_processed += count
                    except Exception as exc:
                        repo_name = futures[future]
                        self.log_error(f"Repository {repo_name} generated an exception: {exc}")

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

        if self.config.dry_run:
            print(
                f"  {Fore.YELLOW}PRs That Would Be Processed: {self.stats.dry_run_skipped}{Style.RESET_ALL}"
            )
            print(
                f"  {Fore.YELLOW}PRs Already Merged: {self.stats.skipped_already_merged}{Style.RESET_ALL}"
            )
            print(
                f"  {Fore.YELLOW}PRs With Conflicts: {self.stats.skipped_conflicts}{Style.RESET_ALL}"
            )
        else:
            print(
                f"  {Fore.GREEN}Successfully Merged: {self.stats.successful_merges}{Style.RESET_ALL}"
            )
            print(
                f"  {Fore.YELLOW}Skipped (Already Merged): {self.stats.skipped_already_merged}{Style.RESET_ALL}"
            )
            print(
                f"  {Fore.YELLOW}Skipped (Conflicts): {self.stats.skipped_conflicts}{Style.RESET_ALL}"
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
        Execute the batch merge operation.

        Returns:
            Exit code (0 for success, 1 for failure)
        """
        if not self.authenticate():
            return 1

        self.process_repositories()
        self.print_summary()
        return 0


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Batch merge Pull Requests across all GitHub repositories for a user.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry-run (default - safe mode)
  python pr_batch_merger.py --token ghp_xxxxx

  # Actually merge PRs (use with caution!)
  python pr_batch_merger.py --token ghp_xxxxx --no-dry-run

  # Merge only in repositories matching a pattern
  python pr_batch_merger.py --token ghp_xxxxx --repo-filter "myproject.*"

  # Use squash merge method
  python pr_batch_merger.py --token ghp_xxxxx --merge-method squash --no-dry-run

  # Limit to first 10 PRs
  python pr_batch_merger.py --token ghp_xxxxx --max-prs 10 --no-dry-run
        """,
    )

    parser.add_argument(
        "--token",
        type=str,
        help="GitHub Personal Access Token (can also use GH_TOKEN env var)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Dry-run mode: list what would happen without merging (default: True)",
    )

    parser.add_argument(
        "--no-dry-run",
        action="store_false",
        dest="dry_run",
        help="Disable dry-run mode and actually merge PRs",
    )

    parser.add_argument(
        "--merge-method",
        type=str,
        choices=["merge", "squash", "rebase"],
        default="merge",
        help="Merge method to use (default: merge)",
    )

    parser.add_argument(
        "--repo-filter",
        type=str,
        help="Regex pattern to filter repository names",
    )

    parser.add_argument(
        "--exclude-archived",
        action="store_true",
        default=True,
        help="Exclude archived repositories (default: True)",
    )

    parser.add_argument(
        "--include-archived",
        action="store_false",
        dest="exclude_archived",
        help="Include archived repositories",
    )

    parser.add_argument(
        "--max-prs",
        type=int,
        help="Maximum number of PRs to process (default: unlimited)",
    )

    parser.add_argument(
        "--workers",
        type=int,
        default=20,
        help="Number of concurrent workers (default: 20)",
    )

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_arguments()

    # Get token from args or environment
    token = args.token or os.getenv("GH_TOKEN")

    if not token:
        logger.error("❌ CRITICAL: GH_TOKEN is missing in .env or arguments")
        return 1

    # Create and run merger
    config = MergerConfig(
        token=token,
        dry_run=args.dry_run,
        merge_method=args.merge_method,
        repo_filter=args.repo_filter,
        exclude_archived=args.exclude_archived,
        max_prs=args.max_prs,
        max_workers=args.workers,
    )
    merger = PRBatchMerger(config)

    return merger.run()


if __name__ == "__main__":
    sys.exit(main())
