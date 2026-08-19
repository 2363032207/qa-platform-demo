# 启动测试平台 API（第 7～8 课）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$python = Join-Path $PWD ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    Write-Host "[ERROR] .venv not found" -ForegroundColor Red
    Write-Host "Run: python -m venv .venv"
    Write-Host "     .\.venv\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
}

Write-Host "Checking dependencies..."
& $python -c "import uvicorn, fastapi"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing requirements..."
    & $python -m pip install -r requirements.txt
}

Write-Host ""
Write-Host "Starting API - keep this window open, Ctrl+C to stop" -ForegroundColor Green
Write-Host "Swagger: http://127.0.0.1:8000/docs"
Write-Host "Health:  http://127.0.0.1:8000/health"
Write-Host ""

& $python -m uvicorn qa_platform.main:app --reload --host 127.0.0.1 --port 8000
