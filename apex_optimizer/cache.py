import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from .config import Settings

logger = logging.getLogger("ApexOptimizer")

class CacheManager:
    def __init__(self, config: Settings) -> None:
        self.cache_dir = Path(config.CACHE_DIR)
        self._ensure_cache_dir()

    def _ensure_cache_dir(self) -> None:
        """Creates the cache directory if it doesn't exist."""
        try:
            if not self.cache_dir.exists():
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                logger.info(f"   📁 Created cache directory at {self.cache_dir}")
        except Exception as e:
            logger.error(f"   ❌ Failed to create cache directory at {self.cache_dir}: {e}")
            # We might want to re-raise or handle this, but for now logging is key.
            # If cache dir fails, the whole app might fail to write cache, but could still run.

    def _generate_key(self, data: str) -> str:
        """Generates an MD5 hash key from the input data."""
        return hashlib.md5(data.encode("utf-8")).hexdigest()

    def _get_file_path(self, key: str) -> Path:
        """Returns the full file path for a given cache key."""
        return self.cache_dir / f"{key}.json"

    def get(self, key_data: str) -> Any | None:
        """Retrieves data from the cache using a key derived from key_data."""
        key = self._generate_key(key_data)
        file_path = self._get_file_path(key)

        if file_path.exists():
            try:
                with open(file_path, encoding="utf-8") as f:
                    data = json.load(f)
                # logger.info(f"   📦 Cache Hit: {key}")
                return data
            except Exception as e:
                logger.warning(f"   ⚠️  Failed to read cache for {key}: {e}")
                return None
        return None

    def set(self, key_data: str, value: Any) -> None:
        """Saves data to the cache using a key derived from key_data."""
        key = self._generate_key(key_data)
        file_path = self._get_file_path(key)

        try:
            # Ensure directory exists before writing (defensive)
            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(value, f, indent=2)
            # logger.info(f"   💾 Cache Saved: {key}")
        except Exception as e:
            logger.error(f"   ❌ Failed to write to cache for {key}: {e}")

    def exists(self, key_data: str) -> bool:
        """Checks if a key exists in the cache."""
        key = self._generate_key(key_data)
        return self._get_file_path(key).exists()
