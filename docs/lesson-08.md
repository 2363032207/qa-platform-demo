# 第 8 课笔记（请用自己的话补全）

## 1. Agent 在整条链路里负责哪几步？

POST /api/jobs/next

## 2. `POST /api/jobs/next` 和 `POST /api/jobs` 有什么不同？

自动执行下个任务

## 3. 为什么 Agent 要把结果 POST 回平台，而不是只在终端打印？

方便进行测试以及确认答案

## 4. 本次实操：Agent 跑通后的终端输出 + GET 任务详情摘要

```text
platform win32 -- Python 3.10.11, pytest-8.3.5, pluggy-1.6.0 -- C:\Users\linjiahao\Projects\qa-platform-demo\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\linjiahao\Projects\qa-platform-demo
configfile: pytest.ini
plugins: anyio-4.14.2
collected 8 items

tests/test_agent_api.py::test_claim_next_job_and_submit PASSED                                                   [ 12%]
tests/test_agent_api.py::test_claim_next_when_empty PASSED                                                       [ 25%]
tests/test_agent_api.py::test_parse_junit PASSED                                                                 [ 37%]
tests/test_platform_api.py::test_health PASSED                                                                   [ 50%]
tests/test_platform_api.py::test_create_and_get_job PASSED                                                       [ 62%]
tests/test_platform_api.py::test_submit_result_updates_status PASSED                                             [ 75%]
tests/test_platform_api.py::test_list_jobs PASSED                                                                [ 87%]
tests/test_platform_api.py::test_get_job_not_found PASSED                                                        [100%]

```

