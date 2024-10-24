import json
import time
from pathlib import Path
from typing import Optional, Dict, Any
from .utils import generate_cache_key


class Cache:
    """File-based cache implementation with expiration."""

    def __init__(self, cache_dir: str, expiry_time: int):
        self.cache_dir = Path(cache_dir)
        self.expiry_time = expiry_time
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, key: str) -> Path:
        """Get the file path for a cache key."""
        return self.cache_dir / f"{key}.json"

    def get(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached content if it exists and is not expired."""
        cache_key = generate_cache_key(url)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        try:
            with cache_path.open('r') as f:
                cached_data = json.load(f)

            if time.time() - cached_data['timestamp'] > self.expiry_time:
                cache_path.unlink()
                return None

            return cached_data['content']
        except (json.JSONDecodeError, KeyError):
            return None

    def set(self, url: str, content: Dict[str, Any]):
        """Cache content for a given URL."""
        cache_key = generate_cache_key(url)
        cache_path = self._get_cache_path(cache_key)

        cache_data = {
            'timestamp': time.time(),
            'content': content
        }

        with cache_path.open('w') as f:
            json.dump(cache_data, f)

    def clear_expired(self):
        """Remove expired cache entries."""
        current_time = time.time()
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with cache_file.open('r') as f:
                    cached_data = json.load(f)
                if current_time - cached_data['timestamp'] > self.expiry_time:
                    cache_file.unlink()
            except (json.JSONDecodeError, KeyError):
                cache_file.unlink()