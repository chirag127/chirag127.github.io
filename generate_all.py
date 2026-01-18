#!/usr/bin/env python3
"""
Quick Generation Script - Generate everything with one command

This is a simplified version of the complete site generator for easy use.

Usage:
    python generate_all.py                 # Generate everything
    python generate_all.py --polymorphs    # Only generate polymorphs
    python generate_all.py --sitemap       # Only generate sitemap
    python generate_all.py --dry-run       # Preview what would be done
"""

import argparse
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show the result."""
    print(f"\n🚀 {description}")
    print("=" * 60)

    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True, capture_output=True)
        if result.stdout:
            print(result.stdout)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate Chirag Hub website")
    parser.add_argument("--polymorphs", action="store_true", help="Only generate polymorphs")
    parser.add_argument("--sitemap", action="store_true", help="Only generate sitemap")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating")
    parser.add_argument("--workers", type=int, default=5, help="Concurrent workers for polymorphs")

    args = parser.parse_args()

    print("🌟 CHIRAG HUB GENERATOR")
    print("=" * 60)

    success_count = 0
    total_tasks = 0

    # Change to scripts directory
    scripts_dir = Path(__file__).parent / "scripts"

    if args.sitemap or not (args.polymorphs or args.sitemap):
        total_tasks += 1
        cmd = f"cd {scripts_dir} && python generate_sitemap_simple.py"
        if run_command(cmd, "Generating comprehensive sitemap"):
            success_count += 1

    if args.polymorphs or not (args.polymorphs or args.sitemap):
        total_tasks += 1
        dry_flag = "--dry-run" if args.dry_run else ""
        cmd = f"cd {scripts_dir} && python generate_polymorphs_hub.py --workers {args.workers} {dry_flag}"
        if run_command(cmd, f"Generating polymorphs (concurrent, {args.workers} workers)"):
            success_count += 1

    # Final summary
    print("\n" + "=" * 60)
    print("🎉 GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Completed: {success_count}/{total_tasks} tasks")

    if success_count == total_tasks:
        print("🌟 All tasks completed successfully!")
        print("🌐 Your website is ready!")
        print("📍 Main site: https://chirag127.github.io/")
        print("🔮 Polymorphs: https://chirag127.github.io/polymorphs/")
        print("🗺️ Sitemap: https://chirag127.github.io/sitemap.xml")
    else:
        print(f"⚠️ {total_tasks - success_count} tasks failed")
        sys.exit(1)

if __name__ == "__main__":
    main()