# AI Assistant Workshop Cheat Sheet

| Term | Concise intuition |
|---|---|
| AI | Broad field of building systems that perform tasks associated with intelligent behavior. |
| LLM | A model trained to predict tokens; it generates fluent text but is not a fact database. |
| Prompt | The input messages and context supplied for one model call. |
| System instructions | High-priority application behavior supplied before the user message. |
| Token | A unit of text processed by the model; not always a whole word. |
| Context | Information available during the current inference call. |
| Context window | Maximum token budget for input and output together. |
| Embedding | A learned numeric representation used to compare text patterns. It is not human understanding. |
| Vector | An ordered list of numbers, such as an embedding. |
| Vector database | A store optimized for saving vectors and finding nearby ones, often with metadata filters. |
| Chunk | A retrievable piece of a document. Its boundaries affect retrieval quality. |
| Retriever | Component that selects possible evidence for a question. Relevance is not correctness. |
| RAG | Retrieve relevant external context, then ask a model to generate using it. RAG reduces some knowledge gaps; it does not eliminate hallucinations. |
| Metadata | Structured facts about a chunk, such as role, year, seniority, or authority. |
| Tool calling | Letting a model request a deterministic function or external operation through a controlled interface. |
| Hallucination | Unsupported or false generated content that may still sound confident. |

## Debugging flow

```text
Question → instructions → conversation state → retrieval query
         → retrieved chunks + metadata → model context → output checks
```

When an answer is wrong, ask: Was the fact in the documents? Was it chunked clearly? Was the correct chunk retrieved? Did metadata exclude it? Did the model receive and follow it? Did validation catch unsupported claims?

## Useful commands

Start with Docker, or use the Windows virtual-environment fallback when virtualization is unavailable:

```powershell
.\scripts\setup-venv.ps1  # first run only
.\scripts\run-venv.ps1
```

```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/knowledge/reindex
curl "http://localhost:8000/debug/retrieval?q=hardware%20and%20programming"
docker compose logs -f assistant-api
```

`docker compose logs` applies only to the Docker setup. In venv mode, server logs appear directly in the PowerShell window.
