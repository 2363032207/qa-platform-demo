# 第 4 课笔记（请用自己的话补全）

## 1. 数据驱动测试解决什么问题？

消除代码冗余，降低维护成本

## 2. `smoke_cases.yaml` 和 `test_smoke_api.py` 各管什么？

- `smoke_cases.yaml`：管**测什么**（数据/用例表）
- `test_smoke_api.py`：管**怎么测**（手写逻辑与特殊断言）
- `test_smoke_driven.py`：读 yaml，**一套代码跑多行数据**

## 3. `@pytest.mark.parametrize` 是干什么的？

**一套代码，多组数据，批量运行**

## 4. AI 生成缺陷报告时，为什么要区分「事实」和「推测」？

AI 容易根据日志「猜」原因；事实（状态码、断言）必须和日志一致，推测要标出来，避免把猜测当定论误导研发。

## 5. 本次实操：pytest tests/test_smoke_driven.py -v 结果

```text
collected 5 items
test_smoke_from_yaml[S1]~[S5] PASSED
5 passed in 1.97s
```

