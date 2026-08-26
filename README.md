# Engineering Career & Study Path Assistant

A small workshop application for learning how modern AI assistants are engineered around an LLM. The application is intentionally limited at the starting stage; you will improve its instructions, context, retrieval, and orchestration during the workshop.

## Requirements

- Git
- Docker Desktop (or Docker Engine with Compose v2), **or Python 3.11+**
- 4 GB free memory recommended
- Optional: an API key for an OpenAI-compatible provider

## Setup with Docker

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

## Setup without virtualization (Windows)

Docker is optional. Participants whose computers do not support virtualization can run the same workshop app in a Python virtual environment. This mode uses an in-process knowledge index, so Qdrant and Docker are not required.

Install Python 3.11 or newer first and select **Add Python to PATH** during installation. Python includes `venv`; it does not need to be installed separately.

### Manual PowerShell setup

Open **Windows PowerShell** (not Command Prompt), change to the cloned repository directory, and run each command separately:

```powershell
cd "C:\path\to\jid-rag-training"
if (!(Test-Path .env)) { Copy-Item .env.example .env }
py -3 -m venv backend\.venv
Set-ExecutionPolicy -Scope Process Bypass
.\backend\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
$env:QDRANT_URL = "memory://"
$env:KNOWLEDGE_PATH = (Resolve-Path .\knowledge).Path
Set-Location backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

If `py` is not recognized but `python` works, replace `py -3 -m venv backend\.venv` with:

```powershell
python -m venv backend\.venv
```

`Set-ExecutionPolicy -Scope Process Bypass` applies only to the current PowerShell window; it does not permanently change the computer's execution policy. After Uvicorn starts, open <http://localhost:8000>. Stop the server with `Ctrl+C`.

For later sessions, open PowerShell in the repository root and run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\backend\.venv\Scripts\Activate.ps1
$env:QDRANT_URL = "memory://"
$env:KNOWLEDGE_PATH = (Resolve-Path .\knowledge).Path
Set-Location backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### Helper scripts

The repository also provides scripts that automate the same steps:

```powershell
.\scripts\setup-venv.ps1  # first session only
.\scripts\run-venv.ps1
```

The environment variables select the in-process knowledge index and point it at the repository's `knowledge` directory for the current PowerShell process only. Existing `.env` settings—including demo mode and optional provider credentials—continue to apply. Restarting the app rebuilds its in-memory index automatically.

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

## Security boundary

This is a local workshop application, not a production deployment. Docker Compose binds the API and Qdrant ports to `127.0.0.1` so they are not exposed to the local network. The debugging and reindexing endpoints intentionally have no authentication and must remain local unless authentication, authorization, rate limiting, and production monitoring are added.

Keep real provider credentials only in `.env`. The file is ignored by Git; `.env.example` contains no secret. Never place API keys in source files, workshop documents, screenshots, issue reports, or chat transcripts. If a key is exposed, revoke and replace it immediately.

## Project map

```text
backend/app/assistant/  behavior, provider, orchestration, deterministic tool
backend/app/rag/        loading, chunking, embeddings, Qdrant indexing/retrieval
knowledge/              local workshop knowledge and deliberate quality problems
training/participant/   participant handouts
training/instructor/    delivery guide, scenarios, expected outcomes
tests/                  focused code tests and evaluation prompts
```
