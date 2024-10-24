from typing import List, Dict, Any
from bs4 import BeautifulSoup
import requests
from ..config import ScraperConfig
from ..nlp import TextProcessor


class ContentExtractor:
    """Extracts and processes content from web pages."""

    def __init__(self, config: ScraperConfig):
        self.config = config
        self.text_processor = TextProcessor(config.language)

    def clean_html(self, html: str) -> BeautifulSoup:
        """Clean and parse HTML content."""
        soup = BeautifulSoup(html, 'html.parser')

        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'footer']):
            element.decompose()

        return soup

    def extract_text(self, soup: BeautifulSoup) -> str:
        """Extract clean text from HTML soup."""
        text = soup.get_text(separator=' ', strip=True)
        return self.clean_text(text)

    def clean_text(self, text: str) -> str:
        """Clean extracted text by removing extra whitespace and normalizing characters."""
        # Replace multiple spaces with single space
        text = ' '.join(text.split())
        # Remove special characters and normalize whitespace
        text = text.replace('\n', ' ').replace('\t', ' ').strip()
        return text

    def extract_metadata(self, soup: BeautifulSoup) -> Dict[str, str]:
        """Extract metadata from HTML."""
        metadata = {}

        # Extract title
        title = soup.find('title')
        if title:
            metadata['title'] = title.get_text(strip=True)

        # Extract meta description
        description = soup.find('meta', attrs={'name': 'description'})
        if description:
            metadata['description'] = description.get('content', '')

        # Extract meta keywords
        keywords = soup.find('meta', attrs={'name': 'keywords'})
        if keywords:
            metadata['keywords'] = keywords.get('content', '')

        # Extract author
        author = soup.find('meta', attrs={'name': 'author'})
        if author:
            metadata['author'] = author.get('content', '')

        # Extract Open Graph metadata
        og_tags = {
            'og:title': 'og_title',
            'og:description': 'og_description',
            'og:image': 'og_image',
            'og:url': 'og_url',
            'og:type': 'og_type'
        }

        for og_tag, key in og_tags.items():
            meta = soup.find('meta', attrs={'property': og_tag})
            if meta:
                metadata[key] = meta.get('content', '')

        return metadata

    def extract_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all links from the page."""
        links = []
        for link in soup.find_all('a', href=True):
            links.append({
                'text': link.get_text(strip=True),
                'href': link['href']
            })
        return links

    def extract_images(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all images from the page."""
        images = []
        for img in soup.find_all('img'):
            image_data = {
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'title': img.get('title', '')
            }
            images.append(image_data)
        return images

    def process_page(self, url: str) -> Dict[str, Any]:
        """Process a complete web page and extract all relevant information."""
        try:
            response = requests.get(url, headers=self.config.headers)
            response.raise_for_status()

            soup = self.clean_html(response.text)

            return {
                'url': url,
                'metadata': self.extract_metadata(soup),
                'text': self.extract_text(soup),
                'links': self.extract_links(soup),
                'images': self.extract_images(soup),
                'status': 'success'
            }

        except Exception as e:
            return {
                'url': url,
                'status': 'error',
                'error': str(e)
            }

    def process_multiple_pages(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Process multiple pages in batch."""
        results = []
        for url in urls:
            results.append(self.process_page(url))
        return results