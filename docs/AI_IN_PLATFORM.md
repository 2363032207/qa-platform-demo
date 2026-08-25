# AI 在测试平台中的用法（第 10 课）

## 能力

- 任务交卷且 `failed > 0` 时，平台自动生成 **AI/规则摘要**，写入 `job_results.ai_summary`
- 看板 `/` 会展示失败任务的摘要

## 开关与配置

| 环境变量 | 含义 | 默认 |
|----------|------|------|
| `QA_AI_SUMMARY` | `0`/`false` 关闭摘要 | 开启 |
| `QA_AI_API_KEY` 或 `OPENAI_API_KEY` | 有则尝试调用大模型 | 无则用本地规则 |
| `QA_AI_BASE_URL` | 兼容 OpenAI 的 API 地址 | `https://api.openai.com/v1` |
| `QA_AI_MODEL` | 模型名 | `gpt-4o-mini` |

## 护栏

1. **红灯仍以真实测试为准**：摘要只是辅助，不改变 `success`/`failed`
2. **摘要失败不影响交卷**：生成异常时写简短跳过信息或留空
3. **不编造**：Prompt 要求只根据日志；本地规则也只抽取 FAILED/assert 行
4. **密钥不入库**：API Key 只走环境变量，不要写进代码或 commit
5. **摘要不改门禁**：质量门禁只认 `failed/total`（见 `docs/QUALITY_GATE.md`）

## 人工评审

AI/规则摘要进看板后，仍需人工判断：产品缺陷 / 用例问题 / 环境问题。
