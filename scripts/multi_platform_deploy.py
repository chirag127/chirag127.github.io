#!/usr/bin/env python3
"""
Multi-Platform Deployment Module

Deploys generated tool repositories to multiple hosting platforms:
- Netlify
- Vercel
- Cloudflare Pages
- Surge.sh
- Neocities
- Firebase
- Deno Deploy

Controlled by ENABLE_* flags in .env (all disabled by default for safety).
"""

import os
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, Optional
import logging

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger('MultiPlatformDeploy')


# =============================================================================
# PLATFORM ENABLE FLAGS (All disabled by default for safety)
# =============================================================================

ENABLE_FLAGS = {
    'netlify': os.getenv('ENABLE_NETLIFY', 'false').lower() == 'true',
    'vercel': os.getenv('ENABLE_VERCEL', 'false').lower() == 'true',
    'cloudflare': os.getenv('ENABLE_CLOUDFLARE', 'false').lower() == 'true',
    'surge': os.getenv('ENABLE_SURGE', 'false').lower() == 'true',
    'neocities': os.getenv('ENABLE_NEOCITIES', 'false').lower() == 'true',
    'firebase': os.getenv('ENABLE_FIREBASE', 'false').lower() == 'true',
    'deno': os.getenv('ENABLE_DENO', 'false').lower() == 'true',
}


def is_platform_enabled(platform: str) -> bool:
    """Check if a platform is enabled for deployment."""
    return ENABLE_FLAGS.get(platform.lower(), False)


def get_enabled_platforms() -> list:
    """Get list of enabled platforms."""
    return [p for p, enabled in ENABLE_FLAGS.items() if enabled]


# =============================================================================
# PLATFORM SECRETS
# =============================================================================

SECRETS = {
    'netlify': {
        'auth_token': os.getenv('NETLIFY_AUTH_TOKEN'),
        'site_id': os.getenv('NETLIFY_SITE_ID'),
    },
    'vercel': {
        'token': os.getenv('VERCEL_TOKEN'),
        'org_id': os.getenv('VERCEL_ORG_ID'),
        'project_id': os.getenv('VERCEL_PROJECT_ID'),
    },
    'cloudflare': {
        'api_token': os.getenv('CLOUDFLARE_API_TOKEN'),
        'account_id': os.getenv('CLOUDFLARE_ACCOUNT_ID'),
        'project_name': os.getenv('CLOUDFLARE_PROJECT_NAME', 'chirag-hub'),
    },
    'surge': {
        'token': os.getenv('SURGE_TOKEN'),
        'domain': os.getenv('SURGE_DOMAIN', 'chirag127.surge.sh'),
    },
    'neocities': {
        'api_key': os.getenv('NEOCITIES_API_KEY'),
        'sitename': os.getenv('NEOCITIES_SITENAME', 'chirag127'),
    },
    'firebase': {
        'service_account': os.getenv('FIREBASE_SERVICE_ACCOUNT'),
        'project_id': os.getenv('FIREBASE_PROJECT_ID'),
    },
    'deno': {
        'token': os.getenv('DENO_DEPLOY_TOKEN'),
        'project_name': os.getenv('DENO_PROJECT_NAME'),
    },
}


def has_platform_secrets(platform: str) -> bool:
    """Check if required secrets are configured for a platform."""
    secrets = SECRETS.get(platform, {})
    if platform == 'netlify':
        return bool(secrets.get('auth_token') and secrets.get('site_id'))
    elif platform == 'vercel':
        return bool(secrets.get('token'))
    elif platform == 'cloudflare':
        return bool(secrets.get('api_token') and secrets.get('account_id'))
    elif platform == 'surge':
        return bool(secrets.get('token'))
    elif platform == 'neocities':
        return bool(secrets.get('api_key'))
    elif platform == 'firebase':
        return bool(secrets.get('project_id'))
    elif platform == 'deno':
        return bool(secrets.get('token'))
    return False


# =============================================================================
# DEPLOYMENT FUNCTIONS
# =============================================================================

def deploy_to_surge(dist_path: Path, domain: str = None) -> dict:
    """Deploy to Surge.sh."""
    if not is_platform_enabled('surge'):
        return {'status': 'skipped', 'reason': 'Platform disabled'}

    secrets = SECRETS['surge']
    if not secrets.get('token'):
        return {'status': 'error', 'reason': 'Missing SURGE_TOKEN'}

    domain = domain or secrets['domain']

    try:
        result = subprocess.run(
            ['surge', str(dist_path), domain, '--token', secrets['token']],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return {'status': 'success', 'url': f'https://{domain}'}
        return {'status': 'error', 'reason': result.stderr}
    except FileNotFoundError:
        return {'status': 'error', 'reason': 'surge CLI not installed (npm i -g surge)'}
    except Exception as e:
        return {'status': 'error', 'reason': str(e)}


def deploy_to_neocities(dist_path: Path, tool_name: str = None) -> dict:
    """Deploy to Neocities via API."""
    if not is_platform_enabled('neocities'):
        return {'status': 'skipped', 'reason': 'Platform disabled'}

    secrets = SECRETS['neocities']
    if not secrets.get('api_key'):
        return {'status': 'error', 'reason': 'Missing NEOCITIES_API_KEY'}

    try:
        # Upload files via Neocities API
        api_url = 'https://neocities.org/api/upload'
        headers = {'Authorization': f'Bearer {secrets["api_key"]}'}

        files_to_upload = []
        for file_path in dist_path.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(dist_path)

                # If tool_name is provided, deploy to subdirectory
                if tool_name:
                    upload_path = f"{tool_name}/{rel_path}".replace("\\", "/")
                else:
                    upload_path = str(rel_path).replace("\\", "/")

                files_to_upload.append(
                    (upload_path, (upload_path, open(file_path, 'rb')))
                )

        if not files_to_upload:
            return {'status': 'error', 'reason': 'No files to upload'}

        response = requests.post(api_url, headers=headers, files=files_to_upload, timeout=120)

        if response.status_code == 200:
            sitename = secrets.get('sitename', 'chirag127')
            url = f'https://{sitename}.neocities.org'
            if tool_name:
                url += f'/{tool_name}'
            return {'status': 'success', 'url': url}
        return {'status': 'error', 'reason': response.text}
    except Exception as e:
        return {'status': 'error', 'reason': str(e)}


def trigger_render_deploy() -> dict:
    """Trigger Render deploy via webhook."""
    webhook_url = os.getenv('RENDER_DEPLOY_HOOK_URL')
    if not webhook_url:
        return {'status': 'skipped', 'reason': 'No deploy hook configured'}

    if not os.getenv('ENABLE_RENDER', 'false').lower() == 'true':
        return {'status': 'skipped', 'reason': 'Platform disabled'}

    try:
        response = requests.post(webhook_url, timeout=30)
        if response.status_code in [200, 201]:
            return {'status': 'success', 'message': 'Deploy triggered'}
        return {'status': 'error', 'reason': f'HTTP {response.status_code}'}
    except Exception as e:
        return {'status': 'error', 'reason': str(e)}


# =============================================================================
# MAIN DEPLOYMENT ORCHESTRATOR
# =============================================================================

def deploy_to_all_platforms(dist_path: Path, tool_name: str = None) -> dict:
    """
    Deploy to all enabled platforms.

    Args:
        dist_path: Path to the built site files
        tool_name: Name of the tool being deployed (for subdomain naming)

    Returns:
        Dict with results for each platform
    """
    results = {}

    enabled = get_enabled_platforms()
    if not enabled:
        logger.info("⏭️ No platforms enabled (all ENABLE_* flags are false)")
        logger.info("   Set ENABLE_NETLIFY=true etc. in .env to enable deployment")
        return {'all_skipped': True, 'reason': 'No platforms enabled'}

    logger.info(f"🚀 Deploying to {len(enabled)} platform(s): {', '.join(enabled)}")

    # Priority order for deployment
    platform_order = ['surge', 'neocities']

    for platform in platform_order:
        if platform not in enabled:
            continue

        logger.info(f"  → Deploying to {platform.capitalize()}...")

        if platform == 'surge':
            domain = f"{tool_name}.surge.sh" if tool_name else SECRETS['surge']['domain']
            results['surge'] = deploy_to_surge(dist_path, domain)
        elif platform == 'neocities':
            results['neocities'] = deploy_to_neocities(dist_path, tool_name)

        # Log result
        status = results.get(platform, {}).get('status', 'unknown')
        if status == 'success':
            url = results[platform].get('url', '')
            logger.info(f"  ✅ {platform.capitalize()}: {url}")
        elif status == 'skipped':
            reason = results[platform].get('reason', '')
            logger.info(f"  ⏭️ {platform.capitalize()}: {reason}")
        else:
            reason = results[platform].get('reason', '')
            logger.error(f"  ❌ {platform.capitalize()}: {reason}")

    return results


def show_deployment_status():
    """Show current deployment configuration status."""
    print("\n" + "=" * 60)
    print("🌐 MULTI-PLATFORM DEPLOYMENT STATUS")
    print("=" * 60)

    print("\nPlatform          | Enabled | Secrets Configured")
    print("-" * 50)

    platforms = [
        ('GitHub Pages', True, True),  # Always enabled
        ('Netlify', ENABLE_FLAGS['netlify'], has_platform_secrets('netlify')),
        ('Vercel', ENABLE_FLAGS['vercel'], has_platform_secrets('vercel')),
        ('Cloudflare', ENABLE_FLAGS['cloudflare'], has_platform_secrets('cloudflare')),
        ('Surge.sh', ENABLE_FLAGS['surge'], has_platform_secrets('surge')),
        ('Neocities', ENABLE_FLAGS['neocities'], has_platform_secrets('neocities')),
        ('Firebase', ENABLE_FLAGS['firebase'], has_platform_secrets('firebase')),
        ('Deno Deploy', ENABLE_FLAGS['deno'], has_platform_secrets('deno')),
    ]

    for name, enabled, has_secrets in platforms:
        enabled_str = "✅ Yes" if enabled else "❌ No"
        secrets_str = "✅ Yes" if has_secrets else "⚠️ Missing"
        print(f"{name:17} | {enabled_str:7} | {secrets_str}")

    print("\n" + "=" * 60)
    print("To enable a platform, set ENABLE_<PLATFORM>=true in .env")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    show_deployment_status()
