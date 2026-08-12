# 启动测试平台 API（第 7 课）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "API docs: http://127.0.0.1:8000/docs"
.\.venv\Scripts\python.exe -m uvicorn qa_platform.main:app --reload --host 127.0.0.1 --port 8000
