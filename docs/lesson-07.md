# 第 7 课笔记（请用自己的话补全）

## 1. REST API 在本项目里解决什么问题？


|               |
| ------------- |
| 用 HTTP 管理测试任务 |


## 2. `POST /api/jobs` 和 `POST /api/jobs/{id}/result` 分别谁调用？

## `POST /api/jobs由发起测试的人调用，POST /api/jobs/{id}/result已经完成测试的人`

## 3. Swagger `/docs` 页面有什么用？

方便其他人员调用

## 4. 本次实操：`pytest tests/test_platform_api.py -v` 结果

```text
PS C:\Users\linjiahao\Projects\qa-platform-demo> .\.venv\Scripts\python.exe -m pytest tests/test_platform_api.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.10.11, pytest-8.3.5, pluggy-1.6.0 -- C:\Users\linjiahao\Projects\qa-platform-demo\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\linjiahao\Projects\qa-platform-demo
configfile: pytest.ini
plugins: anyio-4.14.2
collected 5 items

tests/test_platform_api.py::test_health PASSED                                                                   [ 20%]
tests/test_platform_api.py::test_create_and_get_job PASSED                                                       [ 40%]
tests/test_platform_api.py::test_submit_result_updates_status PASSED                                             [ 60%]
tests/test_platform_api.py::test_list_jobs PASSED                                                                [ 80%]
tests/test_platform_api.py::test_get_job_not_found PASSED                                                        [100%]
```

