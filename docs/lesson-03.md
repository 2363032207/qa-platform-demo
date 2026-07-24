# 第 3 课笔记（请用自己的话补全）

## 1. 为什么要做「分层」？用例层和 HttpClient 各管什么？

因为复用性，易维护。用例层管理结果和流程，HTTP client管理怎么发送，怎么运行

## 2. config.yaml 和环境变量 QA_BASE_URL 分别解决什么问题？

config.yaml解决了团队通用的、相对稳定的配置，QA_BASE_URL解决了不同环境的快速切换

## 3. conftest.py 里的 fixture 是干什么的？

前置准备

## 4. 本次实操：pytest -v 结果摘要

platform win32 -- Python 3.10.11, pytest-8.3.5, pluggy-1.6.0 -- C:\Users\linjiahao\Projects\qa-platform-demovenv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\linjiahao\Projects\qa-platform-demo
collected 3 items

tests/test_smoke_api.py::test_echo_get_should_return_200 PASSED
tests/test_smoke_api.py::test_echo_status_404_should_return_404 PASSED
tests/test_smoke_api.py::test_echo_get_with_query_foo PASSED

```text
粘贴这里
```

