# Engineering Career & Study Path Assistant

A small workshop application for learning how modern AI assistants are engineered around an LLM. The application is intentionally limited at the starting stage; you will improve its instructions, context, retrieval, and orchestration during the workshop.

## Requirements

- Git
- Docker Desktop (or Docker Engine with Compose v2)
- 4 GB free memory recommended
- Optional: an API key for an OpenAI-compatible provider

## Setup

```bash
git clone <repository-url>
cd jid-rag-training
cp .env.example .env
docker compose up --build
```

PowerShell equivalent:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Demo mode is enabled by default, so the infrastructure works without a key. It uses a deterministic educational fallback, not a real LLM or learned embedding model. To use a real provider, set `DEMO_MODE=false`, `LLM_API_KEY`, `LLM_BASE_URL`, `LLM_MODEL`, and `EMBEDDING_MODEL` in `.env`.

Open <http://localhost:8000>. Verify the API:

```bash
curl http://localhost:8000/health
```

The interface is a responsive, build-free single page served directly by FastAPI. It includes guided prompts, workshop-stage visibility, conversation controls, source relevance indicators, and an evidence inspector without adding a frontend container or JavaScript toolchain.

## Workshop stages

Use the six buttons in the **Workshop journey** rail to switch stages immediately. The UI sends the selected stage with each chat request and remembers it for the current browser session. No `.env` edit or container rebuild is required.

Available stages are `basic`, `instructions`, `all_context`, `rag`, `better_retrieval`, and `final`. `ASSISTANT_STAGE` remains the initial default for a new browser session and for API calls that omit `stage`.

The application builds the knowledge index on startup so every RAG stage is ready. Rebuild it manually after changing documents or chunking configuration:

```bash
curl -X POST http://localhost:8000/knowledge/reindex
# or: python scripts/ingest.py
```

Inspect retrieval (encode spaces as `%20` when needed):

```bash
curl "http://localhost:8000/debug/retrieval?q=programming%20close%20to%20hardware"
```

## Useful Docker commands

```bash
docker compose logs -f assistant-api
docker compose ps
docker compose down
docker compose down -v  # also resets the Qdrant index
```

The API contract is visible at <http://localhost:8000/docs>. Workshop participants should start here; instructor explanations and solutions live separately under `training/instructor/` and should be distributed on an instructor-only branch.

## Project map

```text
backend/app/assistant/  behavior, provider, orchestration, deterministic tool
backend/app/rag/        loading, chunking, embeddings, Qdrant indexing/retrieval
knowledge/              local workshop knowledge and deliberate quality problems
training/participant/   participant handouts
training/instructor/    delivery guide, scenarios, expected outcomes
tests/                  focused code tests and evaluation prompts
```
