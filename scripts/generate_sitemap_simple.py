#!/usr/bin/env python3
"""
Simple Sitemap Generator - Auto-generate sitemap.xml from GitHub repos.
Windows-compatible version without Unicode characters.
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
    """Generate comprehensive XML sitemap."""
    today = datetime.now().strftime("%Y-%m-%d")

    # Static pages with enhanced priorities
    static_pages = [
        {"loc": f"{base_url}/", "priority": "1.0", "changefreq": "daily"},
        {"loc": f"{base_url}/about.html", "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{base_url}/contact.html", "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{base_url}/voters.html", "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{base_url}/contractors.html", "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{base_url}/privacy.html", "priority": "0.5", "changefreq": "yearly"},
        {"loc": f"{base_url}/terms.html", "priority": "0.5", "changefreq": "yearly"},
        {"loc": f"{base_url}/cookies.html", "priority": "0.5", "changefreq": "yearly"},
    ]

    # Polymorph pages (alternative AI-generated versions)
    polymorph_pages = []
    polymorphs_dir = ROOT_DIR / "polymorphs"
    if polymorphs_dir.exists():
        for polymorph_file in polymorphs_dir.glob("*.html"):
            polymorph_pages.append({
                "loc": f"{base_url}/polymorphs/{polymorph_file.name}",
                "lastmod": today,
                "priority": "0.9",  # High priority for AI variants
                "changefreq": "weekly"
            })

    # Tool pages from repos with enhanced categorization
    tool_pages = []
    for repo in repos:
        if repo.get("fork") or not repo.get("has_pages"):
            continue
        if repo["name"] in ["chirag127.github.io", "chirag127"]:
            continue

        # Enhanced priority based on stars and activity
        stars = repo.get("stargazers_count", 0)
        updated_at = repo.get("pushed_at", "")

        # Calculate recency bonus (updated in last 30 days)
        recency_bonus = 0
        if updated_at:
            try:
                from datetime import datetime as dt, timedelta
                updated_date = dt.fromisoformat(updated_at.replace('Z', '+00:00'))
                if dt.now().replace(tzinfo=updated_date.tzinfo) - updated_date < timedelta(days=30):
                    recency_bonus = 0.1
            except:
                pass

        # Priority calculation
        if stars >= 50:
            priority = min(0.95, 0.9 + recency_bonus)
        elif stars >= 20:
            priority = min(0.9, 0.85 + recency_bonus)
        elif stars >= 10:
            priority = min(0.85, 0.8 + recency_bonus)
        elif stars >= 5:
            priority = min(0.8, 0.75 + recency_bonus)
        else:
            priority = min(0.75, 0.7 + recency_bonus)

        # Get last modified date
        updated = updated_at[:10] if updated_at else today

        # Determine change frequency based on activity
        changefreq = "weekly"
        if stars >= 20:
            changefreq = "daily"
        elif stars >= 10:
            changefreq = "weekly"
        else:
            changefreq = "monthly"

        tool_pages.append({
            "loc": f"{base_url}/{repo['name']}/",
            "lastmod": updated,
            "priority": f"{priority:.2f}",
            "changefreq": changefreq
        })

    # Generate XML with enhanced structure
    xml_parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        '        xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9',
        '        http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">',
    ]

    # Add all pages in priority order
    all_pages = static_pages + polymorph_pages + tool_pages

    # Sort by priority (highest first) for better SEO
    all_pages.sort(key=lambda x: float(x['priority']), reverse=True)

    for page in all_pages:
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
    """Generate and save comprehensive sitemap.xml."""
    print("Fetching repositories...")
    repos = fetch_all_repos()
    print(f"Found {len(repos)} repositories")

    # Filter for pages-enabled repos
    pages_repos = [r for r in repos if r.get("has_pages") and not r.get("fork")]
    excluded_repos = [r for r in repos if r["name"] in ["chirag127.github.io", "chirag127"]]

    print(f"Pages-enabled repos: {len(pages_repos)}")
    print(f"Excluded repos: {len(excluded_repos)}")

    print("Generating comprehensive sitemap...")

    # Sitemap requires absolute URL
    base_url = Settings.SITE_BASE_URL
    if not base_url:
        base_url = "https://chirag127.github.io"
        print(f"Using fallback URL: {base_url}")

    sitemap = generate_sitemap(repos, base_url)

    # Save sitemap to root directory
    output_path = ROOT_DIR / "sitemap.xml"
    output_path.write_text(sitemap, encoding="utf-8")
    print(f"Saved: {output_path}")

    # Count URLs by type
    url_count = sitemap.count("<url>")
    static_count = 8  # Known static pages
    polymorph_count = sitemap.count("/polymorphs/")
    tool_count = url_count - static_count - polymorph_count

    print("Sitemap Statistics:")
    print(f"  Static pages: {static_count}")
    print(f"  Polymorph pages: {polymorph_count}")
    print(f"  Tool pages: {tool_count}")
    print(f"  Total URLs: {url_count}")

    # Validate sitemap size
    sitemap_size = len(sitemap.encode('utf-8'))
    print(f"  Sitemap size: {sitemap_size / 1024:.1f} KB")

    if url_count > 50000:
        print("WARNING: Sitemap has >50k URLs")
    if sitemap_size > 50 * 1024 * 1024:
        print("WARNING: Sitemap >50MB")

    print("SEO Optimization complete!")
    print(f"Submit to: {base_url}/sitemap.xml")


if __name__ == "__main__":
    main()