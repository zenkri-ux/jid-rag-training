param([int]$Port = 8000)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$backendPath = Join-Path $projectRoot "backend"
$venvPython = Join-Path $backendPath ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $venvPython)) {
    throw "Virtual environment not found. Run .\scripts\setup-venv.ps1 first."
}

$env:QDRANT_URL = "memory://"
$env:KNOWLEDGE_PATH = Join-Path $projectRoot "knowledge"

Push-Location $backendPath
try {
    & $venvPython -m uvicorn app.main:app --host 127.0.0.1 --port $Port
} finally {
    Pop-Location
}
