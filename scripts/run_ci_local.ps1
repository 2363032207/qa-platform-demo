# 本地模拟 CI（不依赖 Docker）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "==> Install dependencies"
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "==> Run pytest (same as GitHub Actions)"
$env:QA_BASE_URL = "https://postman-echo.com"
New-Item -ItemType Directory -Force -Path reports | Out-Null
.\.venv\Scripts\python.exe -m pytest --junitxml=reports\junit.xml

Write-Host "==> Done. Report: reports\junit.xml"
