import os
import json
import time
import hashlib
from typing import Optional, Dict, Any


class Cache:
    """
    Implements a file-based caching system for web scraping results.
    """

    def __init__(self, cache_dir: str, expiry_time: int):
        self.cache_dir = cache_dir
        self.expiry_time = expiry_time
        os.makedirs(cache_dir, exist_ok=True)

    def _get_cache_path(self, url: str) -> str:
        """Generate a cache file path for a given URL."""
        url_hash = hashlib.md5(url.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{url_hash}.json")

    def get(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieve cached content if it exists and is not expired."""
        cache_path = self._get_cache_path(url)
        if not os.path.exists(cache_path):
            return None

        with open(cache_path, 'r') as f:
            cached_data = json.load(f)

        if time.time() - cached_data['timestamp'] > self.expiry_time:
            os.remove(cache_path)
            return None

        return cached_data['content']

    def set(self, url: str, content: Dict[str, Any]):
        """Cache content for a given URL."""
        cache_path = self._get_cache_path(url)
        cache_data = {
            'timestamp': time.time(),
            'content': content
        }
        with open(cache_path, 'w') as f:
            json.dump(cache_data, f)