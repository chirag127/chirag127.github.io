import sys
import os

# Ensure src is in path
sys.path.append(os.path.abspath("src"))

try:
    from ai.unified_client import UnifiedAIClient
    from ai.models import UNIFIED_MODEL_CHAIN, MODEL_COUNT

    print("✅ Imports successful")

    # Initialize client
    client = UnifiedAIClient()
    print("✅ Client initialized")

    # Print status
    client.print_status()

    # Check model count
    print(f"\nModel Count: {MODEL_COUNT}")
    print(f"Chain Length: {len(client.model_chain)}")

    if MODEL_COUNT > 40:
        print("✅ Model catalog expansion verified (45+ models)")
    else:
        print(f"❌ Model count low: {MODEL_COUNT}")

except Exception as e:
    print(f"❌ Verification failed: {e}")
    import traceback
    traceback.print_exc()
