# 第 9 课笔记（请用自己的话补全）

## 1. 看板页面和 Swagger `/docs` 有什么区别？

一个是看通过率一个是可以操作接口测试

## 2. 通过率是怎么算出来的？

看执行过的接口有多少成功

## 3. 为什么看板要读平台里的 result，而不是直接看 Agent 终端？

result可以更清晰的看到

## 4. 本次实操：打开 [http://127.0.0.1:8000/](http://127.0.0.1:8000/) 看到了什么？（可贴截图说明或文字）

```text
platform win32 -- Python 3.10.11, pytest-8.3.5, pluggy-1.6.0 -- C:\Users\linjiahao\Projects\qa-platform-demo\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\linjiahao\Projects\qa-platform-demo
configfile: pytest.ini
plugins: anyio-4.14.2
collected 3 items

tests/test_dashboard.py::test_build_summary_empty PASSED                                                         [ 33%]
tests/test_dashboard.py::test_build_summary_with_results PASSED                                                  [ 66%]
tests/test_dashboard.py::test_dashboard_page PASSED                                                              [100%]

```

