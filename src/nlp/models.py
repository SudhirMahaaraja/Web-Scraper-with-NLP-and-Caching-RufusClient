from transformers import AutoTokenizer, AutoModel
import torch
from typing import List, Optional


class EmbeddingModel:
    """Manages text embedding models for similarity calculations."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def get_embedding(self, text: str) -> torch.Tensor:
        """Generate embedding for a text string."""
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        return outputs.last_hidden_state.mean(dim=1)

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate cosine similarity between two text strings."""
        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)

        similarity = torch.cosine_similarity(emb1, emb2)
        return similarity.item()