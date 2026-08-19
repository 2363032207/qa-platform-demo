# 启动 Agent（请先另开终端运行 .\scripts\run_api.ps1）
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

Write-Host "Platform: http://127.0.0.1:8000"
Write-Host "Example: .\scripts\run_agent.ps1"
Write-Host "         .\.venv\Scripts\python.exe -m agent.runner --once"
Write-Host "         .\.venv\Scripts\python.exe -m agent.runner --loop --interval 5"

if ($args.Count -eq 0) {
    .\.venv\Scripts\python.exe -m agent.runner --once
} else {
    .\.venv\Scripts\python.exe -m agent.runner @args
}
