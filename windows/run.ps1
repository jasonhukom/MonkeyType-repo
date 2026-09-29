# Creates a virtual environment (first run only), installs rich, and starts the typing test.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..."
    if (Get-Command py -ErrorAction SilentlyContinue) { py -3 -m venv .venv }
    else { python -m venv .venv }
}

& .\.venv\Scripts\python.exe -m pip install --quiet -r ..\requirements.txt
& .\.venv\Scripts\python.exe speed-test.py
