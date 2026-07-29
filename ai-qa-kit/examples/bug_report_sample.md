# 缺陷报告样例 v1（人工定稿）

- 来源 Prompt：`ai-qa-kit/prompts/bug_from_log.md`
- 状态：AI 草稿经人工修订

## 标题
[接口冒烟] GET /status/404 返回 503，与预期 404 不符

## 优先级建议
**P1** — 异常状态码场景失败，影响冒烟与错误处理验证；未阻断全部用例，但需排查环境或服务异常。

## 环境信息
- 版本：lesson-4 练习
- 模块：接口冒烟 / postman-echo
- base_url：https://postman-echo.com

## 复现步骤
1. 配置 `config/config.yaml`，base_url 为 postman-echo
2. 执行 `pytest tests/test_smoke_api.py::test_echo_status_404_should_return_404 -v`
3. 观察断言与 HttpClient 日志

## 期望结果
- HTTP 状态码为 **404**

## 实际结果
- HTTP 状态码为 **503**
- pytest 失败：`assert 503 == 404`

## 日志摘要
```text
FAILED ... test_echo_status_404 - assert 503 == 404
GET https://postman-echo.com/status/404 -> 503 (1200.0 ms)
```

## 影响面
- 单条异常场景用例失败
- 若生产类似接口也返回 5xx，客户端错误提示可能不正确

## 可能原因（推测，需标注）
- [推测] 第三方练习服务不稳定，临时 503
- [推测] 网络代理/防火墙干扰
- [推测] 客户端未区分 4xx 与 5xx 的展示逻辑（需另测）

## 待确认 TODO
- 换时间段重试 3 次，确认是否偶发
- 对比同环境 curl 结果
- 若服务稳定 404，则关闭本缺陷
