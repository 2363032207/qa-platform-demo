@echo off
cd /d "%~dp0.."

set PYTHON=%CD%\.venv\Scripts\python.exe
if not exist "%PYTHON%" (
    echo [错误] 未找到 .venv，请先执行:
    echo   python -m venv .venv
    echo   .venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo 启动 API 服务（本窗口保持运行，Ctrl+C 停止）
echo Swagger: http://127.0.0.1:8000/docs
echo.

"%PYTHON%" -m pip install -q -r requirements.txt
"%PYTHON%" -m uvicorn qa_platform.main:app --reload --host 127.0.0.1 --port 8000

if errorlevel 1 (
    echo.
    echo [启动失败] 可尝试: netstat -ano ^| findstr :8000  检查端口占用
    pause
)
