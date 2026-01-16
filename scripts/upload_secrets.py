"""
Upload Secrets to GitHub Actions
Reads .env file and uploads all keys to the current repository's GitHub Secrets.
Requires 'gh' CLI to be installed and authenticated.
"""

import os
import subprocess
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("SecretsSync")

def main():
    if not os.path.exists(".env"):
        logger.error("❌ .env file not found!")
        return

    # Load environment variables from .env
    # We load them into a dict to iterate
    config = {}
    with open(".env", "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    if not config:
        logger.warning("⚠️ No secrets found in .env")
        return

    logger.info(f"🔑 Found {len(config)} secrets to sync...")

    count = 0
    for key, value in config.items():
        if not value:
            continue

        logger.info(f"   ⬆️ Uploading {key}...")
        try:
            # Use gh cli to set secret
            # echo "VALUE" | gh secret set KEY
            process = subprocess.Popen(
                ["gh", "secret", "set", key],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True # Required for piping in some envs, but here we pipe via stdin
            )
            # Actually, standard Popen with input avoids shell=True for security
            # But 'gh secret set' reads from stdin by default if no body flag?
            # 'gh secret set NAME --body "VALUE"' is safer/easier

            cmd = ["gh", "secret", "set", key, "--body", value]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                count += 1
            else:
                logger.error(f"   ❌ Failed to set {key}: {result.stderr.strip()}")

        except Exception as e:
            logger.error(f"   ❌ Error processing {key}: {e}")

    logger.info(f"\n✅ Synced {count} secrets to GitHub Actions!")

if __name__ == "__main__":
    main()
