from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class ScraperConfig:
    """Configuration settings for the web scraper."""
    max_depth: int = 3
    max_links_per_page: int = 10
    request_delay: float = 1.0
    cache_expiry: int = 3600
    similarity_threshold: float = 0.3
    max_retries: int = 3
    cache_dir: str = str(Path("data/cache"))
    output_dir: str = str(Path("data/output"))
    user_agent: str = "RufusBot/1.0"
    timeout: int = 30
    min_text_length: int = 50
    max_text_length: int = 100000
    parallel_requests: int = 3
    language: str = "en"
    follow_robots_txt: bool = True