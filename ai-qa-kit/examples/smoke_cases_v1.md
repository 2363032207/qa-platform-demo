# 冒烟用例定稿 v1（postman-echo）

- 来源 Prompt：`ai-qa-kit/prompts/api_smoke_from_doc.md`
- 环境 base_url：`https://postman-echo.com`
- 文档输入：GET `/get` 回显；GET `/status/{code}` 返回指定状态码
- 状态：人工评审后定稿（可进练习用例）

| ID | 标题 | Method | Path | 断言 | 优先级 |
|----|------|--------|------|------|--------|
| S1 | 获取回显成功 | GET | /get | status==200 且 body 含 url | P0 |
| S2 | 带查询参数回显 | GET | /get?foo=bar | status==200 且 args.foo=="bar" | P0 |
| S3 | 状态码 404 | GET | /status/404 | status==404 | P1 |
| S4 | 状态码 500 | GET | /status/500 | status==500 | P1 |

## 评审备注

- S1/S3：文档明确能力，冒烟必留。
- S2：`/get` 回显查询参数，与「回显」一致，对应第 2 课自增用例。
- S4：同一 `/status/{code}` 机制的异常扩展，P1；最小集可只保留 S1+S3。
- 超时 / 缺参：文档未约定，不编造；有真实项目文档后再补 `TODO`。
