# 第 6 课笔记（请用自己的话补全）

## 1. CI 是什么？和「本地手动跑 pytest」有什么区别？

每次对自动跑代码进行测试，本地手动跑需要人工进行测试，CI可以在代码更新的时候进行自动化测试

## 2. Dockerfile 在这里起什么作用？

自动化构建依赖和拷贝代码只是装依赖，还保证**任何人/任何机器**用同一环境跑测试

## 3. GitHub Actions 里 `on: push` 和 `jobs.test.steps` 各干什么？

on:push：**什么时候**触发流水线  `jobs.test.steps：`触发后**具体做哪些步骤**（拉代码 → 装包 → pytest）

## 4. 本次实操结果（贴命令输出或 Actions 截图说明）

```text
================================================= test session starts =================================================
platform win32 -- Python 3.10.11, pytest-8.3.5, pluggy-1.6.0 -- C:\Users\linjiahao\Projects\qa-platform-demo\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\linjiahao\Projects\qa-platform-demo
configfile: pytest.ini
testpaths: tests
collected 12 items

tests/test_network.py::test_offline_should_raise_network_offline_error PASSED                                    [  8%]
tests/test_network.py::test_retry_should_succeed_on_second_attempt PASSED                                        [ 16%]
tests/test_network.py::test_retry_exhausted_should_raise_timeout PASSED                                          [ 25%]
tests/test_smoke_api.py::test_echo_get_should_return_200 PASSED                                                  [ 33%]
tests/test_smoke_api.py::test_echo_status_404_should_return_404 PASSED                                           [ 41%]
tests/test_smoke_api.py::test_echo_get_with_query_foo PASSED                                                     [ 50%]
tests/test_smoke_api.py::test_echo_post_json PASSED                                                              [ 58%]
tests/test_smoke_driven.py::test_smoke_from_yaml[S1] PASSED                                                      [ 66%]
tests/test_smoke_driven.py::test_smoke_from_yaml[S2] PASSED                                                      [ 75%]
tests/test_smoke_driven.py::test_smoke_from_yaml[S3] PASSED                                                      [ 83%]
tests/test_smoke_driven.py::test_smoke_from_yaml[S4] PASSED                                                      [ 91%]
tests/test_smoke_driven.py::test_smoke_from_yaml[S5] PASSED                                                      [100%]

----------------- generated xml file: C:\Users\linjiahao\Projects\qa-platform-demo\reports\junit.xml ------------------
================================================= 12 passed in 3.65s ==================================================
==> Done. Report: reports\junit.xml
```

1. **PR 时 CI 红了，不该合入** 

