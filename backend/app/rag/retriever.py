import math
import uuid
from typing import Any

import httpx

from app.config import Settings
from app.rag.embeddings import EmbeddingClient


class QdrantRetriever:
    def __init__(self, settings: Settings, embeddings: EmbeddingClient):
        self.settings = settings
        self.embeddings = embeddings
        self.in_memory = settings.qdrant_url.lower().startswith("memory://")
        self._points: list[dict[str, Any]] = []
        self.base = f"{settings.qdrant_url.rstrip('/')}/collections/{settings.collection_name}"

    async def index(self, chunks: list[dict[str, Any]]) -> int:
        vectors = await self.embeddings.embed([chunk["text"] for chunk in chunks])
        if self.in_memory:
            self._points = [
                {"vector": vector, "payload": {**chunk["metadata"], "text": chunk["text"]}}
                for chunk, vector in zip(chunks, vectors)
            ]
            return len(self._points)

        async with httpx.AsyncClient(timeout=90) as client:
            await client.delete(self.base)
            create = await client.put(self.base, json={"vectors": {"size": len(vectors[0]), "distance": "Cosine"}})
            create.raise_for_status()
            points = []
            for index, (chunk, vector) in enumerate(zip(chunks, vectors)):
                payload = {**chunk["metadata"], "text": chunk["text"]}
                point_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{payload.get('path')}:{payload.get('section')}:{index}"))
                points.append({"id": point_id, "vector": vector, "payload": payload})
            for start in range(0, len(points), 64):
                response = await client.put(f"{self.base}/points?wait=true", json={"points": points[start:start + 64]})
                response.raise_for_status()
        return len(points)

    async def search(self, query: str, limit: int | None = None, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        vector = (await self.embeddings.embed([query]))[0]
        if self.in_memory:
            matches = [
                {
                    "score": self._cosine_similarity(vector, point["vector"]),
                    **point["payload"],
                }
                for point in self._points
                if not filters or all(point["payload"].get(key) == value for key, value in filters.items())
            ]
            matches.sort(key=lambda item: item["score"], reverse=True)
            return matches[:limit or self.settings.top_k]

        body: dict[str, Any] = {"query": vector, "limit": limit or self.settings.top_k, "with_payload": True}
        if filters:
            body["filter"] = {"must": [{"key": key, "match": {"value": value}} for key, value in filters.items()]}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{self.base}/points/query", json=body)
            if response.status_code == 404:
                return []
            response.raise_for_status()
        return [{"score": hit["score"], **hit["payload"]} for hit in response.json()["result"]["points"]]

    @staticmethod
    def _cosine_similarity(left: list[float], right: list[float]) -> float:
        numerator = sum(a * b for a, b in zip(left, right))
        left_norm = math.sqrt(sum(value * value for value in left))
        right_norm = math.sqrt(sum(value * value for value in right))
        denominator = left_norm * right_norm
        return numerator / denominator if denominator else 0.0
