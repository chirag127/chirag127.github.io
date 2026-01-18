#!/usr/bin/env python3
"""
Complete Site Generator - Automated Website Generation Pipeline

Generates thecomplete Chirag Hub ecosystem:
1. Main index.html (using largest model)
2. Polymorphs (concurrent generation with fallback)
3. Enhanced sitemap with all pages
4. SEO optimization and validation

Usage:
    python generate_complete_site.py                    # Full generation
    python generate_complete_site.py --skip-main        # Skip main index
    python generate_complete_site.py --skip-polymorphs  # Skip polymorphs
    python generate_complete_site.py --workers 8        # Set concurrency
    python generate_complete_site.py --dry-run          # Preview only
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Setup paths
SCRIPT_DIR = Path(__file__).parent.absolute()
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

from src.ai.unified_client import UnifiedAIClient
from src.ai.models import get_sidebar_enabled_models
from src.core.config import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('CompleteGenerator')

def run_script(script_name: str, args: list = None, cwd: Path = None) -> bool:
    """Run a Python script and return success status."""
    if args is None:
        args = []

    cmd = [sys.executable, script_name] + args
    cwd = cwd or SCRIPT_DIR

    logger.info(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.error(f"Script {script_name} timed out after 1 hour")
        return False
    except Exception as e:
        logger.error(f"Failed to run {script_name}: {e}")
        return False

def generate_main_index(dry_run: bool = False) -> bool:
    """Generate the main index.html using the largest available model."""
    logger.info("=" * 60)
    logger.info("GENERATING MAIN INDEX.HTML")
    logger.info("=" * 60)

    if dry_run:
        logger.info("DRY RUN - Skipping main index generation")
        return True

    try:
        # Use the project generation script to create the main hub
        args = ["--website", "chirag-hub-main"]
        if dry_run:
            args.append("--dry-run")

        success = run_script("generate_projects.py", args)

        if success:
            logger.info("✅ Main index.html generated successfully")
        else:
            logger.error("❌ Failed to generate main index.html")

        return success

    except Exception as e:
        logger.error(f"Error generating main index: {e}")
        return False

def generate_polymorphs(workers: int = 5, dry_run: bool = False) -> bool:
    """Generate all polymorph variants concurrently."""
    logger.info("=" * 60)
    logger.info("GENERATING POLYMORPHS (CONCURRENT)")
    logger.info(f"Workers: {workers}")
    logger.info("=" * 60)

    try:
        args = ["--workers", str(workers)]
        if dry_run:
            args.append("--dry-run")

        success = run_script("generate_polymorphs_hub.py", args)

        if success:
            logger.info("✅ Polymorphs generated successfully")
        else:
            logger.error("❌ Failed to generate polymorphs")

        return success

    except Exception as e:
        logger.error(f"Error generating polymorphs: {e}")
        return False

def generate_sitemap(dry_run: bool = False) -> bool:
    """Generate comprehensive sitemap with all pages."""
    logger.info("=" * 60)
    logger.info("GENERATING COMPREHENSIVE SITEMAP")
    logger.info("=" * 60)

    if dry_run:
        logger.info("DRY RUN - Skipping sitemap generation")
        return True

    try:
        success = run_script("generate_sitemap.py")

        if success:
            logger.info("✅ Sitemap generated successfully")
        else:
            logger.error("❌ Failed to generate sitemap")

        return success

    except Exception as e:
        logger.error(f"Error generating sitemap: {e}")
        return False

def validate_setup() -> bool:
    """Validate that the environment is properly configured."""
    logger.info("🔍 Validating setup...")

    # Check required directories
    required_dirs = [
        ROOT_DIR / "polymorphs",
        ROOT_DIR / "universal",
        ROOT_DIR / "src",
        ROOT_DIR / "scripts"
    ]

    for dir_path in required_dirs:
        if not dir_path.exists():
            logger.error(f"❌ Required directory missing: {dir_path}")
            return False
        logger.info(f"✅ Directory exists: {dir_path}")

    # Check required files
    required_files = [
        ROOT_DIR / "universal" / "core.js",
        ROOT_DIR / "universal" / "sidebar.js",
        ROOT_DIR / "universal" / "style.css",
        SCRIPT_DIR / "generate_polymorphs_hub.py",
        SCRIPT_DIR / "generate_sitemap.py"
    ]

    for file_path in required_files:
        if not file_path.exists():
            logger.error(f"❌ Required file missing: {file_path}")
            return False
        logger.info(f"✅ File exists: {file_path}")

    # Check AI client
    try:
        ai = UnifiedAIClient()
        models = get_sidebar_enabled_models()
        logger.info(f"✅ AI client initialized with {len(models)} models")
    except Exception as e:
        logger.error(f"❌ AI client initialization failed: {e}")
        return False

    # Check environment variables
    required_env = ["CEREBRAS_API_KEY"]
    for env_var in required_env:
        if not os.getenv(env_var):
            logger.error(f"❌ Required environment variable missing: {env_var}")
            return False
        logger.info(f"✅ Environment variable set: {env_var}")

    logger.info("✅ Setup validation complete")
    return True

def optimize_seo() -> bool:
    """Perform additional SEO optimizations."""
    logger.info("=" * 60)
    logger.info("SEO OPTIMIZATION")
    logger.info("=" * 60)

    try:
        # Validate robots.txt
        robots_file = ROOT_DIR / "robots.txt"
        if robots_file.exists():
            logger.info("✅ robots.txt exists")
        else:
            logger.warning("⚠️ robots.txt missing")

        # Validate sitemap.xml
        sitemap_file = ROOT_DIR / "sitemap.xml"
        if sitemap_file.exists():
            logger.info("✅ sitemap.xml exists")

            # Check sitemap size
            sitemap_size = sitemap_file.stat().st_size
            logger.info(f"📊 Sitemap size: {sitemap_size / 1024:.1f} KB")

            if sitemap_size > 50 * 1024 * 1024:  # 50MB
                logger.warning("⚠️ Sitemap exceeds 50MB limit")
        else:
            logger.error("❌ sitemap.xml missing")
            return False

        # Check meta tags in main index
        index_file = ROOT_DIR / "index.html"
        if index_file.exists():
            content = index_file.read_text(encoding='utf-8')

            seo_checks = [
                ('meta name="description"', "Meta description"),
                ('meta name="keywords"', "Meta keywords"),
                ('meta property="og:title"', "Open Graph title"),
                ('meta property="og:description"', "Open Graph description"),
               ('meta name="twitter:card"', "Twitter Card"),
                ('<title>', "Page title"),
                ('application/ld+json', "Structured data")
            ]

            for check, name in seo_checks:
                if check in content:
                    logger.info(f"✅ {name} found")
                else:
                    logger.warning(f"⚠️ {name} missing")

        logger.info("✅ SEO optimization complete")
        return True

    except Exception as e:
        logger.error(f"Error during SEO optimization: {e}")
        return False

def main():
    """Main generation pipeline."""
    parser = argparse.ArgumentParser(description="Complete Site Generator")
    parser.add_argument("--skip-main", action="store_true", help="Skip main index generation")
    parser.add_argument("--skip-polymorphs", action="store_true", help="Skip polymorph generation")
    parser.add_argument("--skip-sitemap", action="store_true", help="Skip sitemap generation")
    parser.add_argument("--skip-seo", action="store_true", help="Skip SEO optimization")
    parser.add_argument("--workers", type=int, default=5, help="Concurrent workers for polymorphs")
    parser.add_argument("--dry-run", action="store_true", help="Preview without generating")
    parser.add_argument("--validate-only", action="store_true", help="Only validate setup")

    args = parser.parse_args()

    start_time = time.time()

    logger.info("🚀 CHIRAG HUB COMPLETE SITE GENERATOR")
    logger.info("=" * 60)

    # Validate setup
    if not validate_setup():
        logger.error("❌ Setup validation failed")
        sys.exit(1)

    if args.validate_only:
        logger.info("✅ Validation complete - exiting")
        return

    success_count = 0
    total_steps = 4

    # Step 1: Generate main index (largest model first)
    if not args.skip_main:
        if generate_main_index(args.dry_run):
            success_count += 1
        else:
            logger.error("❌ Main index generation failed - continuing with polymorphs")
    else:
        logger.info("⏭️ Skipping main index generation")
        success_count += 1

    # Step 2: Generate polymorphs (concurrent)
    if not args.skip_polymorphs:
        if generate_polymorphs(args.workers, args.dry_run):
            success_count += 1
        else:
            logger.error("❌ Polymorph generation failed")
    else:
        logger.info("⏭️ Skipping polymorph generation")
        success_count += 1

    # Step 3: Generate sitemap
    if not args.skip_sitemap:
        if generate_sitemap(args.dry_run):
            success_count += 1
        else:
            logger.error("❌ Sitemap generation failed")
    else:
        logger.info("⏭️ Skipping sitemap generation")
        success_count += 1

    # Step 4: SEO optimization
    if not args.skip_seo and not args.dry_run:
        if optimize_seo():
            success_count += 1
        else:
            logger.error("❌ SEO optimization failed")
    else:
        if args.dry_run:
            logger.info("⏭️ Skipping SEO optimization (dry run)")
        else:
            logger.info("⏭️ Skipping SEO optimization")
        success_count += 1

    # Final summary
    elapsed = time.time() - start_time

    logger.info("=" * 60)
    logger.info("GENERATION COMPLETE")
    logger.info(f"✅ Success: {success_count}/{total_steps} steps")
    logger.info(f"⏱️ Total time: {elapsed:.1f}s")

    if success_count == total_steps:
        logger.info("🎉 All steps completed successfully!")
        logger.info("🌐 Your website is ready for deployment")
        logger.info(f"📍 Main site: {Settings.SITE_BASE_URL}")
        logger.info(f"🔮 Polymorphs: {Settings.SITE_BASE_URL}/polymorphs/")
        logger.info(f"🗺️ Sitemap: {Settings.SITE_BASE_URL}/sitemap.xml")
    else:
        logger.warning(f"⚠️ {total_steps - success_count} steps failed")
        sys.exit(1)

if __name__ == "__main__":
    main()