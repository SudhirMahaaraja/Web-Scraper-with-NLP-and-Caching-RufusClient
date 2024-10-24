import hashlib
from urllib.parse import urlparse, urljoin
from typing import List, Set
import re

def generate_cache_key(url: str) -> str:
    """Generate a unique cache key for a URL."""
    return hashlib.md5(url.encode()).hexdigest()

def normalize_url(url: str) -> str:
    """Normalize URL by removing fragments and normalizing slashes."""
    parsed = urlparse(url)
    return urljoin(url, parsed.path)

def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    return urlparse(url).netloc

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    return text

def get_unique_links(urls: List[str]) -> List[str]:
    """Remove duplicate URLs while preserving order."""
    seen: Set[str] = set()
    return [url for url in urls if not (url in seen or seen.add(url))]