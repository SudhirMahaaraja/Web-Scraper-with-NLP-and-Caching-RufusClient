## Documentation for RAG Pipeline Integration

To integrate this web scraper into a Retrieval-Augmented Generation (RAG) pipeline, follow these steps:

1. **Data Retrieval**: Use the `Crawler` class to fetch data from the web based on user queries or predefined topics.

2. **Data Processing**: Utilize the `ContentExtractor` to clean and process the fetched HTML content. This can include extracting text, removing unnecessary tags, and normalizing data.

3. **Embedding Generation**: Pass the processed content through the `EmbeddingModel` to generate embeddings for text representation.

4. **Query Processing**: When a user inputs a query, embed this query using the same embedding model.

5. **Similarity Calculation**: Compute the similarity between the user query embeddings and the embeddings of the retrieved content. Filter the content based on a predefined similarity threshold.

6. **Final Output**: Return the most relevant pieces of content to the user, possibly in a formatted manner for easy readability.

