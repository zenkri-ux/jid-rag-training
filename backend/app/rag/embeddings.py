import hashlib
import math
import re

import httpx

from app.config import Settings


SYNONYMS = {
    "hardware": ["embedded", "electronics", "microcontroller", "edge"],
    "electronics": ["hardware", "embedded", "circuits"],
    "programming": ["software", "coding", "python"],
    "operations": ["devops", "infrastructure", "cloud"],
    "intelligent": ["ai", "machine", "learning"],
}


class EmbeddingClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if not self.settings.demo_mode and self.settings.llm_api_key:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.settings.llm_base_url.rstrip('/')}/embeddings",
                    headers={"Authorization": f"Bearer {self.settings.llm_api_key}"},
                    json={"model": self.settings.embedding_model, "input": texts},
                )
                response.raise_for_status()
                return [item["embedding"] for item in response.json()["data"]]
        return [self._demo_embedding(text) for text in texts]

    def _demo_embedding(self, text: str) -> list[float]:
        # Stable feature hashing keeps the no-key workshop mode small and reproducible.
        tokens = re.findall(r"[a-z0-9+#.-]+", text.lower())
        expanded = tokens + [term for token in tokens for term in SYNONYMS.get(token, [])]
        vector = [0.0] * self.settings.embedding_dimension
        for token in expanded:
            digest = hashlib.sha256(token.encode()).digest()
            index = int.from_bytes(digest[:4], "big") % len(vector)
            vector[index] += 1.0 if digest[4] % 2 else -1.0
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

