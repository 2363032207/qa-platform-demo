# 本地模拟 CI + 质量门禁（不依赖 Docker）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "==> Install dependencies"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "==> Run pytest"
$env:QA_BASE_URL = "https://postman-echo.com"
New-Item -ItemType Directory -Force -Path reports | Out-Null
.\.venv\Scripts\python.exe -m pytest --junitxml=reports\junit.xml

Write-Host "==> Quality gate"
.\.venv\Scripts\python.exe scripts\check_gate.py reports\junit.xml
if ($LASTEXITCODE -ne 0) {
    Write-Host "GATE FAIL - do not merge" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "==> Done. Report: reports\junit.xml" -ForegroundColor Green
