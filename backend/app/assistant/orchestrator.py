import json
import re
from collections import defaultdict, deque
from typing import Any

from app.assistant.prompts import build_prompt
from app.assistant.provider import ChatProvider
from app.assistant.tools import compare_roles, detect_comparison
from app.config import Settings
from app.rag.loader import load_documents
from app.rag.retriever import QdrantRetriever


STAGES = {"basic", "instructions", "all_context", "rag", "better_retrieval", "final"}


class AssistantOrchestrator:
    def __init__(self, settings: Settings, provider: ChatProvider, retriever: QdrantRetriever):
        self.settings = settings
        self.provider = provider
        self.retriever = retriever
        self.history: dict[str, deque[dict[str, str]]] = defaultdict(lambda: deque(maxlen=6))

    async def chat(self, message: str, conversation_id: str, requested_stage: str | None = None) -> dict[str, Any]:
        configured_stage = self.settings.assistant_stage if self.settings.assistant_stage in STAGES else "basic"
        stage = requested_stage if requested_stage in STAGES else configured_stage
        used_tool = None
        sources: list[dict[str, Any]] = []
        context = ""

        if stage == "all_context":
            documents = load_documents(self.settings.knowledge_path)
            context = "\n\n".join(f"[source: {d['metadata']['source']}]\n{d['text']}" for d in documents)
        elif stage in {"rag", "better_retrieval", "final"}:
            filters = self._infer_filters(message) if stage in {"better_retrieval", "final"} else None
            results = await self.retriever.search(message, filters=filters)
            results = self._resolve_conflicts(results) if stage in {"better_retrieval", "final"} else results
            context = "\n\n".join(
                f"[source: {r['source']} — {r.get('section', '')}; year={r.get('year', 'unknown')}]\n{r['text']}"
                for r in results
            )
            sources = [
                {"document": r["source"], "section": r.get("section", ""), "score": round(r["score"], 4), "year": r.get("year")}
                for r in results
            ]

        comparison = detect_comparison(message) if stage == "final" else None
        if comparison:
            tool_result = compare_roles(*comparison)
            context += f"\n\n[deterministic tool: compare_roles]\n{json.dumps(tool_result, indent=2)}"
            used_tool = "compare_roles"

        history = ""
        if stage == "final":
            history = "\n".join(f"{item['role']}: {item['content']}" for item in self.history[conversation_id])
        answer = await self.provider.complete(build_prompt(stage, context, history), message)
        self.history[conversation_id].extend([{"role": "user", "content": message}, {"role": "assistant", "content": answer}])
        return {"answer": answer, "sources": sources, "stage": stage, "used_tool": used_tool}

    @staticmethod
    def _infer_filters(message: str) -> dict[str, Any] | None:
        lower = message.lower()
        if any(term in lower for term in ("junior", "entry-level", "entry level", "beginner")):
            return {"experience": "entry_level"}
        return None

    @staticmethod
    def _resolve_conflicts(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
        # Keep provenance visible, but put current evidence first when dates exist.
        return sorted(results, key=lambda item: (item.get("year", 0), item.get("score", 0)), reverse=True)
