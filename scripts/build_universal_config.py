#!/usr/bin/env python3
"""
Universal Config Builder (Jan 2026)

This script reads the server-side .env file and the config/services.json schema
to generate the client-side `public/universal/config.js` file.

It ensures that ONLY variables explicitly defined in `services.json` are exposed
to the client. Private AI keys (GEMINI_API_KEY, etc.) are strictly excluded.
"""

import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Define Paths
ROOT_DIR = Path(__file__).parent.parent
CONFIG_DIR = ROOT_DIR / "config"
PUBLIC_DIR = ROOT_DIR / "public" / "universal"
ENV_FILE = ROOT_DIR / ".env"
SCHEMA_FILE = CONFIG_DIR / "services.json"

def main():
    print("🚀 Building Universal Client Configuration...")

    # 1. Load Environment Variables
    if not ENV_FILE.exists():
        print(f"❌ Error: .env file not found at {ENV_FILE}")
        sys.exit(1)

    load_dotenv(ENV_FILE)
    print("✅ Loaded .env")

    # 2. Load Service Schema
    if not SCHEMA_FILE.exists():
        print(f"❌ Error: Schema file not found at {SCHEMA_FILE}")
        sys.exit(1)

    with open(SCHEMA_FILE, "r") as f:
        schema = json.load(f)
    print(f"✅ Loaded schema ({len(schema)} services)")

    # 3. Map values
    client_config = {}

    for service_name, service_fields in schema.items():
        client_config[service_name] = {}
        for field_key, env_var_name in service_fields.items():
            # Retrieve from env, default to validation placeholder or empty
            val = os.getenv(env_var_name)
            if val:
                client_config[service_name][field_key] = val
            else:
                # Optional: Warn if missing?
                # For now we just omit or set null to keep JSON clean.
                client_config[service_name][field_key] = None

    # 4. Generate JavaScript Content
    # We create a self-executing configuration object attached to window
    js_content = f"""/*
   UNIVERSAL CONFIGURATION (GENERATED)
   Source: .env via scripts/build_universal_config.py
   Timestamp: {os.popen('date -u').read().strip() if sys.platform != 'win32' else 'Windows_Build'}
*/

window.SITE_CONFIG = {json.dumps(client_config, indent=4)};

console.log("✅ Universal Config Loaded");
"""

    # 5. Write to File
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    out_file = PUBLIC_DIR / "config.js"

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"🎉 Generated {out_file}")
    print("Dumping preview:")
    print("-" * 40)
    print(js_content[:500] + "...")
    print("-" * 40)

if __name__ == "__main__":
    main()
