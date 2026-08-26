from app.config import Settings
from app.rag.chunker import chunk_document
from app.rag.loader import load_documents
from app.rag.retriever import QdrantRetriever


async def rebuild_index(settings: Settings, retriever: QdrantRetriever) -> int:
    documents = load_documents(settings.knowledge_path)
    chunks = [
        chunk
        for document in documents
        for chunk in chunk_document(document, settings.chunk_size, settings.chunk_overlap)
    ]
    return await retriever.index(chunks)
