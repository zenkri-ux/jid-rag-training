from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.assistant.orchestrator import AssistantOrchestrator
from app.assistant.provider import ChatProvider
from app.config import get_settings
from app.models import ChatRequest, ChatResponse
from app.rag.embeddings import EmbeddingClient
from app.rag.indexer import rebuild_index
from app.rag.retriever import QdrantRetriever
from app.ui import INDEX_HTML


settings = get_settings()
embeddings = EmbeddingClient(settings)
retriever = QdrantRetriever(settings, embeddings)
orchestrator = AssistantOrchestrator(settings, ChatProvider(settings), retriever)


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await rebuild_index(settings, retriever)
    except Exception as exc:
        print(f"Index startup warning: {exc}")
    yield


app = FastAPI(title="Engineering Career & Study Path Assistant", version="1.0.0", lifespan=lifespan)
app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")


@app.get("/", response_class=HTMLResponse)
async def home() -> str:
    return INDEX_HTML


@app.get("/health")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "stage": settings.assistant_stage,
        "demo_mode": settings.demo_mode,
        "runtime_stage_selection": True,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> dict:
    try:
        return await orchestrator.chat(request.message, request.conversation_id, request.stage)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Assistant dependency unavailable: {exc}") from exc


@app.post("/knowledge/reindex")
async def reindex() -> dict[str, int | str]:
    try:
        count = await rebuild_index(settings, retriever)
        return {"status": "indexed", "chunks": count}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Indexing failed: {exc}") from exc


@app.get("/debug/retrieval")
async def debug_retrieval(q: str = Query(min_length=2), limit: int = Query(default=5, ge=1, le=20)) -> dict:
    try:
        results = await retriever.search(q, limit=limit)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Retrieval failed: {exc}") from exc
    return {
        "query": q,
        "results": [
            {
                "source": item["source"], "section": item.get("section", ""),
                "score": round(item["score"], 4), "text": item["text"],
                "metadata": {k: v for k, v in item.items() if k not in {"text", "score", "source", "section"}},
            }
            for item in results
        ],
    }
