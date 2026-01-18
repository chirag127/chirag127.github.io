#!/usr/bin/env python3
"""
Sitemap Generator - Auto-generate sitemap.xml from GitHub repos.

Creates comprehensive sitemap for SEO:
- Main site pages (index, about, privacy, terms, cookies)
- All tool pages from GitHub repos
- Priorities based on stars/activity

Usage:
  python generate_sitemap.py
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import requests

# Setup paths for imports
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from src.core.config import Settings


def fetch_all_repos(username: str = "chirag127") -> list[dict]:
    """Fetch all public repos with pagination."""
    repos = []
    page = 1
    per_page = 100

    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {"per_page": per_page, "page": page, "sort": "updated"}

        try:
            res = requests.get(url, params=params, timeout=30)
            if res.status_code != 200:
                break

            data = res.json()
            if not data:
                break

            repos.extend(data)
            page += 1

            if page > 5:  # Safety limit
                break
        except Exception as e:
            print(f"Error fetching repos: {e}")
            break

    return repos


def generate_sitemap(repos: list[dict], base_url: str = Settings.SITE_BASE_URL) -> str:
    """Generate XML sitemap."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Static pages
    static_pages = [
        {"loc": f"{base_url}/", "priority": "1.0", "changefreq": "daily"},
        {"loc": f"{base_url}/about.html", "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{base_url}/privacy.html", "priority": "0.5", "changefreq": "yearly"},
        {"loc": f"{base_url}/terms.html", "priority": "0.5", "changefreq": "yearly"},
        {"loc": f"{base_url}/cookies.html", "priority": "0.5", "changefreq": "yearly"},
    ]

    # Tool pages from repos
    tool_pages = []
    for repo in repos:
        if repo.get("fork") or not repo.get("has_pages"):
            continue
        if repo["name"] in ["chirag127.github.io", "chirag127"]:
            continue

        # Priority based on stars
        stars = repo.get("stargazers_count", 0)
        if stars >= 10:
            priority = "0.9"
        elif stars >= 5:
            priority = "0.8"
        else:
            priority = "0.7"

        # Get last modified date
        updated = repo.get("pushed_at", "")[:10] if repo.get("pushed_at") else today

        tool_pages.append({
            "loc": f"{base_url}/{repo['name']}/",
            "lastmod": updated,
            "priority": priority,
            "changefreq": "weekly"
        })

    # Guide pages
    guide_pages = []
    guides_dir = ROOT_DIR / "guides"
    if guides_dir.exists():
        for guide_file in guides_dir.glob("*.html"):
            guide_pages.append({
                "loc": f"{base_url}/guides/{guide_file.name}",
                "lastmod": today,
                "priority": "0.6",
                "changefreq": "monthly"
            })

    # Generate XML
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    for page in static_pages + tool_pages + guide_pages:
        xml_parts.append("  <url>")
        xml_parts.append(f"    <loc>{page['loc']}</loc>")
        if page.get("lastmod"):
            xml_parts.append(f"    <lastmod>{page['lastmod']}</lastmod>")
        xml_parts.append(f"    <changefreq>{page['changefreq']}</changefreq>")
        xml_parts.append(f"    <priority>{page['priority']}</priority>")
        xml_parts.append("  </url>")

    xml_parts.append("</urlset>")

    return "\n".join(xml_parts)


def main():
    """Generate and save sitemap.xml."""
    print("🔍 Fetching repositories...")
    repos = fetch_all_repos()
    print(f"📦 Found {len(repos)} repositories")

    print("📝 Generating sitemap...")

    # Sitemap requires absolute URL. Use env var or default to main domain.
    base_url = Settings.SITE_BASE_URL
    if not base_url:
        base_url = "https://chirag127.github.io"
        print(f"⚠️ SITE_BASE_URL not set, using fallback for sitemap: {base_url}")

    sitemap = generate_sitemap(repos, base_url)

    # Save sitemap
    output_path = Path(__file__).parent / "sitemap.xml"
    output_path.write_text(sitemap, encoding="utf-8")
    print(f"✅ Saved: {output_path}")

    # Count URLs
    url_count = sitemap.count("<url>")
    print(f"📊 Total URLs: {url_count}")


if __name__ == "__main__":
    main()
