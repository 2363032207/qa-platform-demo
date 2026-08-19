@echo off
cd /d "%~dp0.."

set PYTHON=%CD%\.venv\Scripts\python.exe
if not exist "%PYTHON%" (
    echo [错误] 未找到 .venv
    pause
    exit /b 1
)

echo Agent 单次执行（请先另开窗口运行 run_api.bat）
echo.
"%PYTHON%" -m agent.runner --once
pause
