import pytest

from app.config import Settings
from app.rag.embeddings import EmbeddingClient
from app.rag.retriever import QdrantRetriever


@pytest.mark.asyncio
async def test_memory_retriever_indexes_and_ranks_chunks(tmp_path):
    settings = Settings(
        _env_file=None,
        demo_mode=True,
        qdrant_url="memory://",
        knowledge_path=tmp_path,
        embedding_dimension=64,
    )
    retriever = QdrantRetriever(settings, EmbeddingClient(settings))
    chunks = [
        {"text": "Embedded hardware and microcontrollers", "metadata": {"source": "hardware"}},
        {"text": "Cloud operations and infrastructure", "metadata": {"source": "cloud"}},
    ]

    assert await retriever.index(chunks) == 2
    results = await retriever.search("electronics hardware", limit=1)

    assert len(results) == 1
    assert results[0]["source"] == "hardware"


@pytest.mark.asyncio
async def test_memory_retriever_applies_filters(tmp_path):
    settings = Settings(_env_file=None, qdrant_url="memory://", knowledge_path=tmp_path)
    retriever = QdrantRetriever(settings, EmbeddingClient(settings))
    await retriever.index([
        {"text": "Python software", "metadata": {"source": "one", "section": "allowed"}},
        {"text": "Python coding", "metadata": {"source": "two", "section": "blocked"}},
    ])

    results = await retriever.search("Python", filters={"section": "allowed"})

    assert [result["source"] for result in results] == ["one"]
