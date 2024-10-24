# Web Scraper with NLP and Caching

## Overview

This repository contains a web scraper designed to extract and process content from web pages. It integrates natural language processing (NLP) capabilities for text analysis and similarity calculation, and it implements caching to improve efficiency. The scraper is built with modularity in mind, allowing for easy integration into various applications, including retrieval-augmented generation (RAG) pipelines.

## Features

- **Configurable Scraper**: Customize the depth of crawling, request delays, caching options, and more.
- **NLP Integration**: Utilize state-of-the-art models for text embedding and analysis.
- **Caching Mechanism**: Cache responses to reduce redundant web requests and improve performance.
- **Rate Limiting**: Avoid overwhelming servers with a built-in rate limiter for web requests.
- **Compliance with Robots.txt**: Respect the rules set by websites regarding web scraping.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Required Python packages (install using `pip install -r requirements.txt`)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

Configure the scraper settings by modifying the `src/config.py` file. Here are some important parameters you can customize:

- `max_depth`: Maximum depth of crawling.
- `max_links_per_page`: Number of links to follow from each page.
- `request_delay`: Time delay between requests to avoid overwhelming servers.
- `cache_expiry`: Duration for which cached content is valid.
- `language`: Language for NLP processing (default is English).

### Usage

1. Create an instance of the `Crawler` class with your configuration:
   ```python
   from config import ScraperConfig
   from scraper.crawler import Crawler

   config = ScraperConfig(max_depth=2)
   crawler = Crawler(config)
   ```

2. Start crawling:
   ```python
   links = crawler.crawl("https://example.com")
   print(links)
   ```

3. To extract content from the crawled pages, use the `ContentExtractor` class:
   ```python
   from scraper.extractor import ContentExtractor

   extractor = ContentExtractor(config)
   for link in links:
       content = extractor.extract_content(link)
       # Process the content as needed
   ```

### Running the Tests

To run the tests included in this repository, use the following command:
```bash
pytest tests/
```

## Summary of the Approach

This project aims to create an efficient and effective web scraper that can handle various challenges in web crawling and data extraction. The approach involves the following key components:

1. **Crawling**: The `Crawler` class navigates the web, respecting `robots.txt` directives and implementing a rate limiter to prevent server overload. It uses BeautifulSoup for HTML parsing and extracts links for further crawling.

2. **Caching**: The `Cache` class ensures that previously fetched data is stored, allowing the scraper to avoid redundant requests. This improves efficiency, especially when dealing with frequently accessed pages.

3. **NLP Processing**: The `TextProcessor` class integrates with the `EmbeddingModel` to extract meaningful information from the crawled content. It employs advanced models to calculate text similarity, enabling the filtering of relevant information based on user queries.


### Example Integration Code

```python
from config import ScraperConfig
from scraper.crawler import Crawler
from scraper.extractor import ContentExtractor
from nlp.models import EmbeddingModel

# Step 1: Setup scraper and extract content
config = ScraperConfig(max_depth=2)
crawler = Crawler(config)
extractor = ContentExtractor(config)

# Fetch links and extract content
links = crawler.crawl("https://example.com")
contents = [extractor.extract_content(link) for link in links]

# Step 2: Process contents with embedding model
embedding_model = EmbeddingModel()
embeddings = [embedding_model.get_embedding(content) for content in contents]

# Step 3: Process user query
query = "Your user query here"
query_embedding = embedding_model.get_embedding(query)

# Step 4: Calculate similarity and retrieve relevant content
relevant_contents = []
for content, embedding in zip(contents, embeddings):
    similarity = embedding_model.calculate_similarity(query_embedding, embedding)
    if similarity > config.similarity_threshold:
        relevant_contents.append(content)

# Step 5: Return or display relevant contents
for content in relevant_contents:
    print(content)
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

