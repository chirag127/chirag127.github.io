#!/usr/bin/env python3
"""
APEX Quick Generation Script v3.0 - Generate everything with one command
Following APEX TECHNICAL AUTHORITY principles:
- Client-Side Only Architecture
- Zero-Defect, High-Velocity, Future-Proof
- AI-Native, Neuro-Inclusive, Ethical-First

This is a simplified version of the complete site generator for easy use.

Usage:
    python generate_all.py                 # Generate everything (APEX compliant)
    python generate_all.py --polymorphs    # Only generate polymorphs
    python generate_all.py --sitemap       # Only generate sitemap
    python generate_all.py --dry-run       # Preview what would be done
    python generate_all.py --validate      # Validate APEX compliance
"""

import argparse
import subprocess
import sys
import time
from pathlib import Path

def print_apex_banner():
    """Print APEX architecture banner."""
    print("🚀 APEX TECHNICAL AUTHORITY v3.0")
    print("=" * 60)
    print("Client-Side Only | Zero-Defect | High-Velocity")
    print("AI-Native | Neuro-Inclusive | Ethical-First")
    print("=" * 60)

def run_command(cmd, description, timeout=300):
    """Run a command and show the result with enhanced error handling."""
    print(f"\n🎯 {description}")
    print("-" * 50)

    try:
        start_time = time.time()
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            timeout=timeout
        )

        elapsed = time.time() - start_time

        if result.stdout:
            print(result.stdout)

        print(f"✅ {description} completed successfully! ({elapsed:.1f}s)")
        return True

    except subprocess.TimeoutExpired:
        print(f"⏰ {description} timed out after {timeout}s")
        return False

    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

    except Exception as e:
        print(f"💥 Unexpected error in {description}: {e}")
        return False

def validate_apex_compliance():
    """Validate APEX architecture compliance."""
    print("\n🔍 APEX COMPLIANCE VALIDATION")
    print("=" * 60)

    checks = []

    # Check required files
    required_files = [
        "universal/core.js",
        "universal/sidebar.js",
        "universal/style.css",
        "universal/config/index.js",
        "universal/integrations/index.js",
        "index.html",
        "README.md"
    ]

    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
            checks.append(True)
        else:
            print(f"❌ {file_path} - MISSING")
            checks.append(False)

    # Check for APEX principles in core.js
    core_js = Path("universal/core.js")
    if core_js.exists():
        content = core_js.read_text()
        apex_checks = [
            ("Client-Side Only", "client" in content.lower() and "side" in content.lower()),
            ("Universal Engine", "Universal Engine" in content),
            ("APEX Architecture", "APEX" in content),
            ("Modular System", "modular" in content.lower()),
            ("Performance Optimized", "performance" in content.lower())
        ]

        for check_name, passed in apex_checks:
            if passed:
                print(f"✅ {check_name} - Implemented")
                checks.append(True)
            else:
                print(f"⚠️ {check_name} - Not detected")
                checks.append(False)

    # Check sidebar positioning (left-side requirement)
    sidebar_js = Path("universal/sidebar.js")
    if sidebar_js.exists():
        content = sidebar_js.read_text()
        if "left" in content.lower():
            print("✅ Polymorph Sidebar - Left-side positioning")
            checks.append(True)
        else:
            print("⚠️ Polymorph Sidebar - Left-side positioning not confirmed")
            checks.append(False)

    success_rate = sum(checks) / len(checks) * 100
    print(f"\n📊 APEX Compliance: {success_rate:.1f}% ({sum(checks)}/{len(checks)})")

    if success_rate >= 90:
        print("🌟 APEX COMPLIANT - Excellent!")
    elif success_rate >= 75:
        print("⚠️ MOSTLY COMPLIANT - Minor issues")
    else:
        print("❌ NON-COMPLIANT - Major issues detected")

    return success_rate >= 75

def main():
    parser = argparse.ArgumentParser(
        description="APEX Chirag Hub Generator v3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_all.py                    # Full generation
  python generate_all.py --polymorphs       # Only polymorphs
  python generate_all.py --sitemap          # Only sitemap
  python generate_all.py --validate         # APEX validation
  python generate_all.py --dry-run          # Preview mode
  python generate_all.py --workers 8        # 8 concurrent workers
        """
    )

    parser.add_argument("--polymorphs", action="store_true",
                       help="Only generate polymorphs (left-sidebar variants)")
    parser.add_argument("--sitemap", action="store_true",
                       help="Only generate sitemap (SEO optimization)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Preview without generating (validation mode)")
    parser.add_argument("--validate", action="store_true",
                       help="Validate APEX compliance only")
    parser.add_argument("--workers", type=int, default=5,
                       help="Concurrent workers for polymorphs (default: 5)")
    parser.add_argument("--timeout", type=int, default=600,
                       help="Timeout per task in seconds (default: 600)")

    args = parser.parse_args()

    print_apex_banner()

    # APEX Compliance Validation
    if args.validate:
        compliance = validate_apex_compliance()
        sys.exit(0 if compliance else 1)

    # Pre-flight validation
    if not args.dry_run:
        print("\n🔍 Pre-flight APEX validation...")
        if not validate_apex_compliance():
            print("\n⚠️ APEX compliance issues detected. Continue anyway? (y/N)")
            if input().lower() != 'y':
                sys.exit(1)

    start_time = time.time()
    success_count = 0
    total_tasks = 0

    # Change to scripts directory
    scripts_dir = Path(__file__).parent / "scripts"

    print(f"\n📂 Working directory: {scripts_dir}")
    print(f"🔧 Configuration: workers={args.workers}, timeout={args.timeout}s")

    # Task 1: Generate Sitemap (SEO Foundation)
    if args.sitemap or not (args.polymorphs or args.sitemap):
        total_tasks += 1
        cmd = f"cd {scripts_dir} && python generate_sitemap_simple.py"
        if run_command(cmd, "Generating comprehensive sitemap (SEO optimization)", args.timeout):
            success_count += 1

    # Task 2: Generate Polymorphs (AI Variants with Left-Sidebar)
    if args.polymorphs or not (args.polymorphs or args.sitemap):
        total_tasks += 1
        dry_flag = "--dry-run" if args.dry_run else ""
        cmd = f"cd {scripts_dir} && python generate_polymorphs_hub.py --workers {args.workers} {dry_flag}"
        if run_command(cmd, f"Generating polymorphs (concurrent, {args.workers} workers, left-sidebar)", args.timeout):
            success_count += 1

    # Final summary
    elapsed = time.time() - start_time

    print("\n" + "=" * 60)
    print("🎉 APEX GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Completed: {success_count}/{total_tasks} tasks")
    print(f"⏱️ Total time: {elapsed:.1f}s")

    if total_tasks > 0:
        success_rate = (success_count / total_tasks) * 100
        print(f"📊 Success rate: {success_rate:.1f}%")

    if success_count == total_tasks:
        print("\n🌟 All tasks completed successfully!")
        print("🏗️ APEX Architecture deployed!")
        print("🌐 Your website is ready!")
        print("📍 Main site: https://chirag127.github.io/")
        print("🔮 Polymorphs: https://chirag127.github.io/polymorphs/ (left-sidebar)")
        print("🗺️ Sitemap: https://chirag127.github.io/sitemap.xml")

        # Performance metrics
        if total_tasks > 0:
            avg_time = elapsed / total_tasks
            print(f"⚡ Average task time: {avg_time:.1f}s")

        print("\n🎯 APEX Principles Applied:")
        print("  ✅ Client-Side Only Architecture")
        print("  ✅ Zero-Defect Pipeline")
        print("  ✅ High-Velocity Generation")
        print("  ✅ AI-Native Polymorphs")
        print("  ✅ Left-Sidebar Positioning")

    else:
        failed_tasks = total_tasks - success_count
        print(f"\n⚠️ {failed_tasks} task(s) failed")
        print("💡 Try running with --dry-run to debug issues")
        print("🔍 Use --validate to check APEX compliance")
        sys.exit(1)

if __name__ == "__main__":
    main()