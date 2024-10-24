import time
import logging
from collections import defaultdict
from threading import Lock
from typing import Dict
from .utils import extract_domain


class RateLimiter:
    """Thread-safe rate limiter for web requests."""

    def __init__(self, delay: float):
        self.delay = delay
        self.last_request_time: Dict[str, float] = defaultdict(float)
        self.locks: Dict[str, Lock] = defaultdict(Lock)

    def wait(self, url: str):
        """Wait appropriate amount of time between requests to the same domain."""
        domain = extract_domain(url)

        with self.locks[domain]:
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time[domain]

            if time_since_last_request < self.delay:
                wait_time = self.delay - time_since_last_request
                logging.debug(f"Rate limiting: waiting {wait_time:.2f}s for {domain}")
                time.sleep(wait_time)

            self.last_request_time[domain] = time.time()