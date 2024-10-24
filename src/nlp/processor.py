import spacy
from typing import List, Optional
from .models import EmbeddingModel


class TextProcessor:
    """Handles text processing and analysis tasks."""

    def __init__(self, language: str = "en"):
        self.nlp = spacy.load(f"{language}_core_web_sm")
        self.embedding_model = EmbeddingModel()

    def extract_sentences(self, text: str) -> List[str]:
        """Extract sentences from text."""
        doc = self.nlp(text)
        return [sent.text.strip() for sent in doc.sents]

    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract key terms from text."""
        doc = self.nlp(text)
        keywords = []

        for token in doc:
            if (token.pos_ in ["NOUN", "PROPN"] and
                    not token.is_stop and
                    len(token.text) > 2):
                keywords.append(token.text.lower())

        # Get frequency distribution
        keyword_freq = {}
        for keyword in keywords:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1

        # Sort by frequency and return top N
        sorted_keywords = sorted(
            keyword_freq.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [k for k, _ in sorted_keywords[:top_n]]

    def filter_relevant_content(
            self,
            content: str,
            query: str,
            threshold: float = 0.5
    ) -> List[str]:
        """Filter content based on relevance to query."""
        sentences = self.extract_sentences(content)
        relevant_sentences = []

        for sentence in sentences:
            similarity = self.embedding_model.calculate_similarity(query, sentence)
            if similarity > threshold:
                relevant_sentences.append(sentence)

        return relevant_sentences