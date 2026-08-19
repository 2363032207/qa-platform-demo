# qa-platform-demo

个人测试开发练习仓库：接口自动化 → 迷你测试平台 → AI 辅助能力。

## 环境

- Python 3.10+
- Windows PowerShell：

```powershell
cd C:\Users\linjiahao\Projects\qa-platform-demo
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -v
```

切换环境（可选）：

```powershell
$env:QA_BASE_URL = "https://postman-echo.com"
pytest -v
```

## 目录

- `tests/` 用例（`conftest.py` 提供 `api_client`）
- `config/` 环境与用例表（`config.yaml`、`smoke_cases.yaml`）
- `core/` 框架核心（`settings.py`、`http_client.py`、`case_loader.py`）
- `qa_platform/` 迷你测试平台 API（FastAPI，第 7 课）
- `ai-qa-kit/` AI Prompt 与评审清单
- `docs/` 笔记与设计

## 测试平台 API（第 7 课）

**CMD（命令提示符）** — 提示符是 `C:\...>` 时用：

```cmd
scripts\run_api.bat
```

**PowerShell** — 提示符是 `PS C:\...>` 时用：

```powershell
.\scripts\run_api.ps1
```

或直接（CMD / PowerShell 都行）：

```powershell
.\.venv\Scripts\python.exe -m uvicorn qa_platform.main:app --reload --host 127.0.0.1 --port 8000
```

浏览器打开 Swagger：`http://127.0.0.1:8000/docs`

| 接口 | 作用 | 谁调 |
|------|------|------|
| `GET /health` | 健康检查 | 任何人 |
| `POST /api/jobs` | 创建测试任务 | 发起者（你/CI/看板） |
| `GET /api/jobs` | 任务列表 | 发起者/看板 |
| `POST /api/jobs/next` | 领取下一个 queued 任务 | **Agent** |
| `GET /api/jobs/{id}` | 任务详情 | 发起者/看板 |
| `POST /api/jobs/{id}/result` | 回传执行结果 | **Agent** |

## Agent 执行器（第 8 课）

开两个终端：

```powershell
# 终端 1：启动 API
.\scripts\run_api.ps1

# 终端 2：创建任务（Swagger 或 curl）后，跑 Agent 一次
.\.venv\Scripts\python.exe -m agent.runner --once

# 或循环监听
.\.venv\Scripts\python.exe -m agent.runner --loop --interval 5
```

## CI / Docker（第 6 课）

### 本地模拟 CI

```powershell
.\scripts\run_ci_local.ps1
```

### Docker

```powershell
docker build -t qa-platform-demo .
docker run --rm qa-platform-demo
```

### GitHub Actions

推送到 `main` / `master` 后，`.github/workflows/ci.yml` 自动跑 pytest。

## 当前进度

- [x] 第 1～6 课
- [x] 第 7 课：FastAPI 平台 API
- [x] 第 8 课：Agent 执行器
- [ ] 第 9 课：结果看板（待开始）
