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
