# 缺陷报告草稿（AI 生成 + 待人工修订）

- 来源 Prompt：`ai-qa-kit/prompts/bug_from_log.md`
- 输入日志：test_smoke_from_yaml[S5] 失败
- 状态：草稿

### 标题

[接口冒烟][S5] GET /status/500 返回 500，与用例期望 501 不符

### 优先级建议

**P2** — 单条数据驱动冒烟用例失败；从日志看更可能是用例配置错误，而非服务端异常。若确认为配置问题，应修 yaml 而非提产品缺陷。

### 环境信息

- 版本：lesson-4 练习（TODO：补具体 commit/构建号）
- 模块：接口冒烟 / 数据驱动 `test_smoke_driven.py`
- 相关配置：`config/smoke_cases.yaml` 用例 S5；base_url 见 `config/config.yaml`（TODO：确认是否为 postman-echo.com）

### 复现步骤

1. 确保 `config/smoke_cases.yaml` 中 S5 为：`method: GET`，`path: /status/500`，`expected_status: 501`
2. 在项目根目录执行：`pytest tests/test_smoke_driven.py::test_smoke_from_yaml[S5] -v`
3. 观察断言失败信息



### 期望结果

- 根据用例配置，HTTP 状态码应为 **501**



### 实际结果

- HTTP 响应状态码为 **500**
- pytest 断言失败：`assert 500 == 501`
- 失败位置：`tests/test_smoke_driven.py` 第 28 行（`assert response.status_code == case["expected_status"]`）



### 日志摘要

```text
case = {'expected_status': 501, 'id': 'S5', 'method': 'GET', 'path': '/status/500', ...}
assert response.status_code == case["expected_status"]
E       assert 500 == 501
E        +  where 500 = <Response [500]>.status_code
FAILED tests/test_smoke_driven.py::test_smoke_from_yaml[S5] - assert 500 == 501
```



### 影响面

- S5 单条用例失败，S1～S4 是否通过：TODO（本次日志未提供全量结果）
- 不直接阻断游戏主流程（练习环境第三方接口）
- 若同类错误进入正式用例表，会导致**误报缺陷**，浪费排查时间



### 可能原因（推测，需标注）

- [推测] **用例数据配置错误**：路径为 `/status/500`，按 postman-echo 语义应返回 500，与 `expected_status: 501` 不一致
- [推测] 本意是测 `/status/501`，但 `path` 写成了 `/status/500`
- [推测] 第三方服务行为与文档不一致（需 curl 对比验证，日志中未提供响应体）



### 待确认 TODO

- 核对 `smoke_cases.yaml` S5：`path` 与 `expected_status` 是否应同为 500
- 本机执行：`curl -i https://postman-echo.com/status/500`，确认稳定返回码
- 修正 yaml 后重跑：`pytest tests/test_smoke_driven.py -v`
- 若修正后为 PASS，则关闭本单，归类为「用例维护问题」而非产品 Bug



### 人工修订说明（请你填写）

- AI 草稿中我同意的部分：我同意 AI 关于“用例配置错误”的判断
- 我删除/修改的部分及原因：优先级从 P1 改为 P2；我准备将此单从「产品缺陷」修改为「用例维护/数据修正」。因为经过人工核对，服务器的行为（Echo 状态码）是完全符合预期的，错在我们的测试数据。提给开发会被标记为 "Invalid"（无效单），所以我将直接在测试仓库中修正 YAML。

