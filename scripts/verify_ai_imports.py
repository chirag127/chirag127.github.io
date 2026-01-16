import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

try:
    print("Attempting to import src.ai.providers...")
    import ai.providers
    print("SUCCESS: Imported ai.providers")

    print("Attempting to import classes from ai.providers...")
    from ai.providers import CerebrasProvider, GroqProvider, GeminiProvider
    print(f"SUCCESS: Imported CerebrasProvider: {CerebrasProvider}")

    print("Attempting to import UnifiedAIClient...")
    from ai.unified_client import UnifiedAIClient
    print("SUCCESS: Imported UnifiedAIClient")

except Exception as e:
    print(f"FAILURE: {e}")
    sys.exit(1)
