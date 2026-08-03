# 第 5 课笔记（请用自己的话补全）

## 1. 超时和 HTTP 404/500 有什么区别？为什么要分开测？

超时：没有接收到请求

HTTP 404/500：接收到了回调，404是路径不对，500是服务器报错

## 2. `NetworkSimulator` 解决什么问题？和真机飞行模式怎么分工？

模拟断网，可以自动化和重复使用。一个是模拟，一个是真实体验

## 3. 重试应该针对什么错误？为什么不应对 404 重试？

针对“偶然性错误”404是永久性错误，已经确定了

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

