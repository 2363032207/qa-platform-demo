# 第 8 课笔记（请用自己的话补全）

## 1. Agent 在整条链路里负责哪几步？

1. POST /api/jobs/next     → 领取任务（queued → running）

2. 本地跑 pytest

3. POST /api/jobs/{id}/result → 回传 passed/failed/total

## 2. `POST /api/jobs/next` 和 `POST /api/jobs` 有什么不同？


| **接口**                | **谁调**    | **干什么**                           |
| --------------------- | --------- | --------------------------------- |
| `POST /api/jobs`      | 你 / CI    | **下单**：创建任务，status=`queued`       |
| `POST /api/jobs/next` | **Agent** | **领任务**：取最早一条 queued，改为 `running` |


`/next` 不会自己跑测试，只是把任务交给 Agent。

## 3. 为什么 Agent 要把结果 POST 回平台，而不是只在终端打印？

结果要**存进平台**，Swagger / 看板 / 其他人才能看到 `result`，而不只是 Agent 终端里一闪而过。

## 4. 本次实操：Agent 跑通后的终端输出 + GET 任务详情摘要

```text
领取任务 #5，执行: pytest tests/test_network.py -q
已回传 #5: passed=3 failed=0 total=3

```

