# main.py

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import json
import yaml

from src.client import RufusClient
from src.config import ScraperConfig
from src.utils.logging import setup_logging


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from a YAML file or use defaults.

    Args:
        config_path: Path to configuration YAML file

    Returns:
        Dictionary containing configuration values
    """
    default_config = {
        'max_depth': 3,
        'max_links_per_page': 10,
        'request_delay': 1.0,
        'cache_expiry': 3600,
        'similarity_threshold': 0.3,
        'max_retries': 3,
        'cache_dir': 'data/cache',
        'output_dir': 'data/output'
    }

    if not config_path:
        return default_config

    try:
        with open(config_path, 'r') as f:
            custom_config = yaml.safe_load(f)
            return {**default_config, **custom_config}
    except Exception as e:
        logging.warning(f"Error loading config file: {e}. Using defaults.")
        return default_config


def setup_directories(config: Dict[str, Any]):
    """Create necessary directories for the project."""
    for dir_path in [config['cache_dir'], config['output_dir']]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def save_results(results: Dict[str, Any], output_path: str, format: str = 'json'):
    """Save scraping results to file."""
    output_file = Path(output_path)
    if format == 'json':
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
    else:
        raise ValueError(f"Unsupported output format: {format}")


def scrape_website(
        url: str,
        instructions: str,
        config: Dict[str, Any],
        output_path: Optional[str] = None,
        rag_format: bool = False
) -> Dict[str, Any]:
    """
    Scrape website and process results.

    Args:
        url: Target website URL
        instructions: Scraping instructions
        config: Configuration dictionary
        output_path: Path to save results
        rag_format: Whether to convert results to RAG format

    Returns:
        Dictionary containing scraped data
    """
    # Initialize client with configuration
    scraper_config = ScraperConfig(**config)
    client = RufusClient(scraper_config)

    # Perform scraping
    logging.info(f"Starting scrape of {url}")
    results = client.scrape(url, instructions)

    if results is None:
        logging.error("Scraping failed")
        return {}

    # Convert to RAG format if requested
    if rag_format:
        results = client.to_rag_format(results)

    # Save results if output path provided
    if output_path:
        save_results(results, output_path)
        logging.info(f"Results saved to {output_path}")

    return results


def main():
    """Main entry point for the scraping tool."""
    parser = argparse.ArgumentParser(description='Web scraping tool for RAG pipelines')

    parser.add_argument('--url', required=True,
                        help='URL to scrape')
    parser.add_argument('--instructions', required=True,
                        help='Instructions for scraping')
    parser.add_argument('--config', type=str,
                        help='Path to configuration YAML file')
    parser.add_argument('--output', type=str,
                        help='Path to save output')
    parser.add_argument('--rag-format', action='store_true',
                        help='Convert output to RAG format')
    parser.add_argument('--log-level', default='INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                        help='Set logging level')

    args = parser.parse_args()

    # Setup logging
    setup_logging(level=args.log_level)

    try:
        # Load configuration
        config = load_config(args.config)

        # Setup directories
        setup_directories(config)

        # Generate output path if not provided
        output_path = args.output
        if not output_path and config['output_dir']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = Path(config['output_dir']) / f"scrape_results_{timestamp}.json"

        # Perform scraping
        results = scrape_website(
            url=args.url,
            instructions=args.instructions,
            config=config,
            output_path=output_path,
            rag_format=args.rag_format
        )

        # Print summary
        num_documents = len(results.get('results', []))
        logging.info(f"Scraping completed. Retrieved {num_documents} documents.")

        return 0

    except Exception as e:
        logging.error(f"Error during execution: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())