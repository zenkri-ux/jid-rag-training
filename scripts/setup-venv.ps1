param([string]$PythonCommand = "")

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$backendPath = Join-Path $projectRoot "backend"
$venvPath = Join-Path $backendPath ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$pythonArgs = @()

if (-not $PythonCommand) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $PythonCommand = "py"
        $pythonArgs = @("-3")
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        $PythonCommand = "python"
    } else {
        throw "Python 3.11 or newer was not found. Install Python, then run this script again."
    }
}

if (-not (Test-Path -LiteralPath (Join-Path $projectRoot ".env"))) {
    Copy-Item -LiteralPath (Join-Path $projectRoot ".env.example") -Destination (Join-Path $projectRoot ".env")
}

& $PythonCommand @pythonArgs -m venv $venvPath
if ($LASTEXITCODE -ne 0) { throw "Could not create the virtual environment." }

& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Could not update pip." }

& $venvPython -m pip install -r (Join-Path $backendPath "requirements.txt")
if ($LASTEXITCODE -ne 0) { throw "Could not install the application dependencies." }

Write-Host "Setup complete. Start the app with: .\scripts\run-venv.ps1"
