# 第 5 课笔记（请用自己的话补全）

## 1. 超时和 HTTP 404/500 有什么区别？为什么要分开测？

**超时**：请求已发出，但在约定时间内没收到完整响应（可能根本没连上，也可能连上但响应太慢）。  
**404/500**：服务器已经返回了 HTTP 响应，只是状态码表示「路径不对」或「服务端错误」。

超时走重试逻辑，404/500 走业务错误处理。

## 2. `NetworkSimulator` 解决什么问题？和真机飞行模式怎么分工？

模拟断网，可以自动化和重复使用。一个是模拟，一个是真实体验

## 3. 重试应该针对什么错误？为什么不应对 404 重试？

**重试适合**：`Timeout`、`ConnectionError` 等**瞬时网络问题**。  
**不重试**：404、500 等**已收到 HTTP 响应**的情况——再试通常还是同样结果，除非服务恢复。

## 4. 本次实操：pytest tests/test_network.py -v 结果

```text
C:\Users\linjiahao\Projects\qa-platform-demo>.\.venv\Scripts\python.exe -m pytest tests/test_network.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.10.11, pytest-8.3.5, pluggy-1.6.0 -- C:\Users\linjiahao\Projects\qa-platform-demo\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\linjiahao\Projects\qa-platform-demo
collected 3 items

tests/test_network.py::test_offline_should_raise_network_offline_error PASSED                                    [ 33%]
tests/test_network.py::test_retry_should_succeed_on_second_attempt PASSED                                        [ 66%]
tests/test_network.py::test_retry_exhausted_should_raise_timeout PASSED                                          [100%]

================================================== 3 passed in 0.04s ==================================================
```

