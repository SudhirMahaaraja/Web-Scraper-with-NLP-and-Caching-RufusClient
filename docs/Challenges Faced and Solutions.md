### Challenges Faced and Solutions

- **Respecting `robots.txt`**:
  - **Challenge**: Initially, the web scraper ignored the directives specified in `robots.txt` files, which can lead to ethical concerns and potential legal repercussions. This oversight risked scraping content that the website owner had explicitly disallowed.
  - **Solution**: I integrated a robot parser library to check the permissions outlined in `robots.txt` before making any requests. This involved parsing the `robots.txt` file of each target site to ensure compliance with their scraping policies. By implementing this check, the scraper now respects the rules set by website administrators, fostering ethical web scraping practices.

- **Caching Implementation**:
  - **Challenge**: Developing an effective caching mechanism posed several difficulties, particularly in managing cache expiration and ensuring that the system did not serve outdated or irrelevant data. Inconsistent cache management could lead to increased load times and unnecessary repeated requests to the server.
  - **Solution**: I employed JSON files for storing cached data, allowing for structured and easy-to-manage cache entries. To handle cache expiry, I implemented a timestamping system that marked each cached entry with a creation time. An automated process was developed to regularly check these timestamps and clear out outdated entries, thus ensuring that the scraper always retrieves fresh data while minimizing server load.

- **NLP Model Performance**:
  - **Challenge**: The initial performance of the Natural Language Processing (NLP) model was unsatisfactory due to slow loading times for the model and the high computational cost of generating embeddings for input texts. This latency significantly affected the overall efficiency of the text processing workflow.
  - **Solution**: To enhance performance, I introduced caching for embeddings of frequently used texts. This involved storing the generated embeddings in memory, reducing the need for repetitive calculations. Additionally, I optimized the embedding calculation process by parallelizing computations where feasible and utilizing batch processing techniques. These optimizations resulted in a significant reduction in processing time, allowing the system to handle larger datasets more efficiently.

