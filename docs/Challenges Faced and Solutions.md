### Challenges Faced and Solutions

- **Respecting Robots.txt**: Initially, the scraper did not adhere to the rules specified by `robots.txt`, leading to potential ethical issues. I implemented a robot parser to check permissions before making requests.

- **Caching Implementation**: Ensuring that the caching mechanism worked effectively while handling cache expiry was complex. I utilized JSON files for caching and implemented a clear mechanism for cache expiration and clearing outdated entries.

- **NLP Model Performance**: The initial version of the text processing was slow due to model loading times. To address this, I cached the embeddings for frequently used texts and optimized the embedding calculation process.