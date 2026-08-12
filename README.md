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

```powershell
pip install -r requirements.txt
.\scripts\run_api.ps1
```

浏览器打开 Swagger：`http://127.0.0.1:8000/docs`

| 接口 | 作用 |
|------|------|
| `GET /health` | 健康检查 |
| `POST /api/jobs` | 创建测试任务 |
| `GET /api/jobs` | 任务列表 |
| `GET /api/jobs/{id}` | 任务详情 |
| `POST /api/jobs/{id}/result` | 回传执行结果 |

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
- [ ] 第 8 课：Agent 执行器（待开始）
