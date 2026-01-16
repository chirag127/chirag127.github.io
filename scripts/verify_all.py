import sys
import os

# Ensure src is in path
src_path = os.path.abspath("src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

print(f"Checking imports with path: {src_path}")

try:
    # 1. Verify AI Providers (Consolidated)
    print("\n--- Verifying AI Providers ---")
    import ai.providers
    from ai.providers import CerebrasProvider, GroqProvider
    print("✅ Successfully imported ai.providers")

    # 2. Verify AI Unified Client
    print("\n--- Verifying AI Unified Client ---")
    # This triggers 'from .providers import ...' inside unified_client
    import ai.unified_client
    print("✅ Successfully imported ai.unified_client")

    # 3. Verify Trend Discovery (Consolidated)
    print("\n--- Verifying Trend Discovery ---")
    import trend_discovery.sources
    from trend_discovery.sources import GitHubTrendingSource
    print("✅ Successfully imported trend_discovery.sources")

    # Verify __init__ exports
    from trend_discovery import GitHubTrendingSource as GH_Init
    print("✅ Successfully imported GitHubTrendingSource from trend_discovery package")

    print("\n🎉 ALL VERIFICATIONS PASSED")

except Exception as e:
    print(f"\n❌ VERIFICATION FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
