# 质量门禁说明（第 11 课）

## 一句话

**门禁 = 能不能合代码 / 能不能放行的硬规则。**  
只认真实测试计数；AI 摘要只给人看，不改红灯。

## 默认规则（本仓库）

```text
failed == 0 且 total > 0  →  PASS（放行）
failed > 0               →  FAIL（阻断）
total == 0               →  FAIL（没有跑测也算未通过）
```

## 怎么用

### 本地

```powershell
# 先跑测试产出报告
.\.venv\Scripts\python.exe -m pytest --junitxml=reports\junit.xml

# 再过门禁
.\.venv\Scripts\python.exe scripts\check_gate.py reports\junit.xml
```

退出码 `0` = 通过；`1` = 未通过。

### CI

GitHub Actions 在 pytest 之后执行 `scripts/check_gate.py`。  
pytest 已经失败时流水线会红；门禁步骤再明确一次「放行规则」。

### 平台 API

`POST /api/gates/evaluate`

```json
{
  "passed": 12,
  "failed": 0,
  "total": 12,
  "ai_summary": "任意文字都不影响结论"
}
```

## 与 AI 摘要的关系

| 能力 | 作用 |
|------|------|
| pytest / junit | 决定红绿 |
| 质量门禁 | 根据红绿决定能否放行 |
| AI 摘要 | 帮助人读失败原因 |

**摘要写「可能是环境问题」也不能自动放行。**

## PR 合入建议

- CI 红了：**不要合入**
- 仅文档改动仍建议跑通门禁（本仓库默认全量 pytest）
- 临时失败要隔离/修复后再合，不要靠改摘要绕过
