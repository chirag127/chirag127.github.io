#!/usr/bin/env python3
"""
GitHub Repository Info Fetcher

Fetches the name and description of all GitHub repositories for a user.
Handles pagination to retrieve all repos (not just first 100).

Usage:
    python get_repos_info.py [--username USERNAME] [--output OUTPUT_FILE] [--format FORMAT]

Environment Variables:
    GH_TOKEN: GitHub Personal Access Token (required for private repos)
    GH_USERNAME: Default username if not provided via CLI
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass
from typing import Optional

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class RepoInfo:
    """Repository information container."""

    name: str
    description: Optional[str]
    full_name: str
    private: bool
    url: str


def fetch_all_repos(
    token: str, username: Optional[str] = None
) -> list[RepoInfo]:
    """
    Fetch all repositories for a user, handling pagination.

    Args:
        token: GitHub Personal Access Token
        username: GitHub username (if None, fetches authenticated user's repos)

    Returns:
        List of RepoInfo objects
    """
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

    repos: list[RepoInfo] = []
    page = 1
    per_page = 100  # Maximum allowed by GitHub API

    # Use different endpoints based on whether username is provided
    if username:
        base_url = f"https://api.github.com/users/{username}/repos"
    else:
        base_url = "https://api.github.com/user/repos"

    print(f"Fetching repositories from: {base_url}")

    while True:
        params = {
            "page": page,
            "per_page": per_page,
            "type": "all" if not username else "owner",  # Get all types for authenticated user
            "sort": "updated",
            "direction": "desc",
        }

        try:
            response = requests.get(
                base_url, headers=headers, params=params, timeout=30
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}", file=sys.stderr)
            break

        data = response.json()

        if not data:
            break

        for repo in data:
            repos.append(
                RepoInfo(
                    name=repo["name"],
                    description=repo.get("description"),
                    full_name=repo["full_name"],
                    private=repo["private"],
                    url=repo["html_url"],
                )
            )

        print(f"  Page {page}: fetched {len(data)} repos (total: {len(repos)})")

        # Check if there are more pages
        if len(data) < per_page:
            break

        page += 1

    return repos


def output_as_table(repos: list[RepoInfo]) -> str:
    """Format repos as a readable table."""
    if not repos:
        return "No repositories found."

    lines = []
    lines.append(f"{'#':>4}  {'Repository Name':<40}  {'Description':<60}")
    lines.append("-" * 110)

    for i, repo in enumerate(repos, 1):
        desc = (repo.description or "No description")[:57]
        if repo.description and len(repo.description) > 57:
            desc += "..."
        visibility = "[PRIVATE]" if repo.private else ""
        name = f"{repo.name} {visibility}"[:40]
        lines.append(f"{i:>4}  {name:<40}  {desc:<60}")

    return "\n".join(lines)


def output_as_json(repos: list[RepoInfo]) -> str:
    """Format repos as JSON."""
    return json.dumps(
        [
            {
                "name": r.name,
                "full_name": r.full_name,
                "description": r.description,
                "private": r.private,
                "url": r.url,
            }
            for r in repos
        ],
        indent=2,
    )


def output_as_csv(repos: list[RepoInfo]) -> str:
    """Format repos as CSV."""
    lines = ["name,full_name,description,private,url"]
    for repo in repos:
        desc = (repo.description or "").replace('"', '""')
        lines.append(f'"{repo.name}","{repo.full_name}","{desc}",{repo.private},"{repo.url}"')
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch GitHub repository names and descriptions"
    )
    parser.add_argument(
        "--username",
        "-u",
        help="GitHub username (default: authenticated user from GH_USERNAME env)",
        default=os.getenv("GH_USERNAME"),
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "--format",
        "-f",
        choices=["table", "json", "csv"],
        default="table",
        help="Output format (default: table)",
    )
    parser.add_argument(
        "--token",
        "-t",
        help="GitHub token (default: from GH_TOKEN env)",
        default=os.getenv("GH_TOKEN"),
    )

    args = parser.parse_args()

    # Validate token
    if not args.token:
        print(
            "Error: GitHub token required. Set GH_TOKEN env or use --token flag.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"GitHub Username: {args.username or '(authenticated user)'}")
    print(f"Output Format: {args.format}")
    print("-" * 50)

    # Fetch repositories
    repos = fetch_all_repos(args.token, args.username)

    print("-" * 50)
    print(f"Total repositories found: {len(repos)}")
    print()

    # Format output
    if args.format == "json":
        output = output_as_json(repos)
    elif args.format == "csv":
        output = output_as_csv(repos)
    else:
        output = output_as_table(repos)

    # Write output
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Output written to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
