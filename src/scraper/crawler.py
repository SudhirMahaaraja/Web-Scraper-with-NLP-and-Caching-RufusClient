import logging
from typing import List, Set, Optional
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
import requests
from ..utils import normalize_url, get_unique_links
from ..config import ScraperConfig


class Crawler:
    """Handles web crawling with respect for robots.txt."""

    def __init__(self, config: ScraperConfig):
        self.config = config
        self.visited: Set[str] = set()
        self.robot_parsers: dict = {}

    def _get_robot_parser(self, url: str) -> Optional[RobotFileParser]:
        """Get or create robot parser for a domain."""
        if not self.config.follow_robots_txt:
            return None

        domain = urlparse(url).netloc
        if domain not in self.robot_parsers:
            rp = RobotFileParser()
            rp.set_url(f"https://{domain}/robots.txt")
            try:
                rp.read()
                self.robot_parsers[domain] = rp
            except Exception as e:
                logging.warning(f"Could not fetch robots.txt for {domain}: {e}")
                return None
        return self.robot_parsers.get(domain)

    def can_fetch(self, url: str) -> bool:
        """Check if URL can be fetched according to robots.txt."""
        rp = self._get_robot_parser(url)
        if not rp:
            return True
        return rp.can_fetch(self.config.user_agent, url)

    def extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract and normalize links from HTML."""
        links = []
        for a in soup.find_all('a', href=True):
            href = a.get('href', '').strip()
            if href and not href.startswith(('#', 'mailto:', 'tel:')):
                absolute_url = urljoin(base_url, href)
                normalized_url = normalize_url(absolute_url)
                links.append(normalized_url)
        return get_unique_links(links)

    def crawl(self, url: str, depth: int = 0) -> List[str]:
        """Crawl website recursively up to specified depth."""
        if (depth >= self.config.max_depth or
                url in self.visited or
                not self.can_fetch(url)):
            return []

        self.visited.add(url)
        links = []

        try:
            response = requests.get(
                url,
                headers={'User-Agent': self.config.user_agent},
                timeout=self.config.timeout
            )
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            page_links = self.extract_links(soup, url)

            links.extend(page_links[:self.config.max_links_per_page])

            if depth < self.config.max_depth:
                for link in links:
                    links.extend(self.crawl(link, depth + 1))

        except Exception as e:
            logging.error(f"Error crawling {url}: {e}")

        return get_unique_links(links)