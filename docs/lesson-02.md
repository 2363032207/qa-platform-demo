# 第 2 课笔记（请用自己的话补全）

## 1. pytest 发现用例的规则是什么？

测试文件必须以 test_ 开头；测试函数需要以 test_ 开头

## 2. assert 失败时你会看到什么？

打印断言两侧实际值 vs 预期值（高亮差异）
输出变量、字典、字符串完整内容

## 3. 为什么冒烟用例要同时写「正常」和「异常」？

需要各个方面都考虑都，这样才能确保当前版本具备基本稳定性

## 4. 本次实操：你跑 pytest 的结果（复制终端摘要）

```text
platform win32 -- Python 3.10.11, pytest-8.3.5, pluggy-1.6.0 -- C:\Users\linjiahao\Projects\qa-platform-demo\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\linjiahao\Projects\qa-platform-demo
collected 2 items

tests/test_smoke_api.py::test_echo_get_should_return_200 PASSED                                                  [ 50%]
tests/test_smoke_api.py::test_echo_status_404_should_return_404 PASSED                                           [100%]
```

