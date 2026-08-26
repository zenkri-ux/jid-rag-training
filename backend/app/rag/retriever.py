import uuid
from typing import Any

import httpx

from app.config import Settings
from app.rag.embeddings import EmbeddingClient


class QdrantRetriever:
    def __init__(self, settings: Settings, embeddings: EmbeddingClient):
        self.settings = settings
        self.embeddings = embeddings
        self.base = f"{settings.qdrant_url.rstrip('/')}/collections/{settings.collection_name}"

    async def index(self, chunks: list[dict[str, Any]]) -> int:
        vectors = await self.embeddings.embed([chunk["text"] for chunk in chunks])
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
        body: dict[str, Any] = {"query": vector, "limit": limit or self.settings.top_k, "with_payload": True}
        if filters:
            body["filter"] = {"must": [{"key": key, "match": {"value": value}} for key, value in filters.items()]}
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(f"{self.base}/points/query", json=body)
            if response.status_code == 404:
                return []
            response.raise_for_status()
        return [{"score": hit["score"], **hit["payload"]} for hit in response.json()["result"]["points"]]
