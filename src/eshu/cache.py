"""Simple caching system for ESHU"""

import json
import time
import hashlib
from pathlib import Path
from typing import Any, Optional


class SimpleCache:
    """Simple file-based cache with TTL support"""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir / "query_cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, key: str) -> str:
        """Generate cache file name from key"""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return f"{key_hash}.json"

    def get(self, key: str, max_age: int = 3600) -> Optional[Any]:
        """
        Get cached value if it exists and isn't expired

        Args:
            key: Cache key
            max_age: Maximum age in seconds (default: 1 hour)

        Returns:
            Cached value or None if not found/expired
        """
        cache_file = self.cache_dir / self._get_cache_key(key)

        if not cache_file.exists():
            return None

        try:
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)

            # Check if expired
            age = time.time() - cached_data['timestamp']
            if age > max_age:
                # Expired, delete it
                cache_file.unlink()
                return None

            return cached_data['value']

        except (json.JSONDecodeError, KeyError, IOError):
            # Corrupted cache, delete it
            if cache_file.exists():
                cache_file.unlink()
            return None

    def set(self, key: str, value: Any) -> None:
        """
        Store value in cache

        Args:
            key: Cache key
            value: Value to cache (must be JSON-serializable)
        """
        cache_file = self.cache_dir / self._get_cache_key(key)

        try:
            cached_data = {
                'timestamp': time.time(),
                'value': value
            }

            with open(cache_file, 'w') as f:
                json.dump(cached_data, f)

        except (TypeError, IOError) as e:
            # Can't cache this value, skip silently
            pass

    def clear(self) -> int:
        """
        Clear all cached data

        Returns:
            Number of files deleted
        """
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        return count

    def clean_expired(self, max_age: int = 86400) -> int:
        """
        Remove expired cache entries

        Args:
            max_age: Maximum age in seconds (default: 24 hours)

        Returns:
            Number of files deleted
        """
        count = 0
        current_time = time.time()

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    cached_data = json.load(f)

                age = current_time - cached_data['timestamp']
                if age > max_age:
                    cache_file.unlink()
                    count += 1

            except (json.JSONDecodeError, KeyError, IOError):
                # Corrupted, delete it
                cache_file.unlink()
                count += 1

        return count
