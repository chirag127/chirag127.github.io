#!/usr/bin/env python3
"""
Universal Config Builder (Jan 2026) -> V3 (Hardcoded Public Keys)

This script reads `config/services.json` (which now contains the actual public IDs)
and generates the client-side `public/universal/config.js` file.

It does NOT read .env anymore, as per the mandate to hardcode public keys
and separate them from private server-side secrets.
"""

import json
import os
import sys
from pathlib import Path

# Define Paths
ROOT_DIR = Path(__file__).parent.parent
CONFIG_DIR = ROOT_DIR / "config"
PUBLIC_DIR = ROOT_DIR / "public" / "universal"
SCHEMA_FILE = CONFIG_DIR / "services.json"

def main():
    print("🚀 Building Universal Client Configuration (V3)...")

    # 1. Load Service Schema (Now Source of Truth)
    if not SCHEMA_FILE.exists():
        print(f"❌ Error: Schema file not found at {SCHEMA_FILE}")
        sys.exit(1)

    with open(SCHEMA_FILE, "r") as f:
        client_config = json.load(f)
    print(f"✅ Loaded public config ({len(client_config)} services)")

    # 2. Generate JavaScript Content
    # We create a self-executing configuration object attached to window
    js_content = f"""/*
   UNIVERSAL CONFIGURATION (GENERATED)
   Source: config/services.json
   Timestamp: {os.popen('date -u').read().strip() if sys.platform != 'win32' else 'Windows_Build'}
*/

window.SITE_CONFIG = {json.dumps(client_config, indent=4)};

console.log("✅ Universal Config Loaded");
"""

    # 3. Write to File
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PUBLIC_DIR / "config.js"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"🎉 Generated {out_file}")

if __name__ == "__main__":
    main()
