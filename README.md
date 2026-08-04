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
- `config/config.yaml` 环境与超时
- `config/smoke_cases.yaml` 数据驱动用例表
- `core/` 框架核心（`settings.py`、`http_client.py`、`case_loader.py`）
- `ai-qa-kit/` AI Prompt 与评审清单
- `docs/` 笔记与设计

## 当前进度

- [x] 第 1 课：仓库初始化
- [x] 第 2 课：pytest 冒烟
- [x] 第 3 课：HttpClient 分层 + 配置
## CI / Docker（第 6 课）

### 本地模拟 CI（推荐，无需 Docker）

```powershell
.\scripts\run_ci_local.ps1
```

### Docker 跑测试（需安装 Docker Desktop）

```powershell
docker build -t qa-platform-demo .
docker run --rm qa-platform-demo
```

### GitHub Actions

推送到 GitHub 的 `main` / `master` 分支后，`.github/workflows/ci.yml` 会自动跑 pytest。  
PR 也会触发同一套检查。

## 当前进度

- [x] 第 5 课：网络异常（超时/重试/断网 Mock）
- [ ] 第 6 课：Docker + CI（进行中）