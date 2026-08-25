# 性能基线说明（第 12 课）

## 一句话

**基线 = 同一场景、同一档机型上，可接受的性能下限/上限。**  
平台负责**入库 + 对比**；真机指标仍来自 PerfDog / 自研采样，本课不替代真机采集。

## 和功能门禁的区别

| | 功能质量门禁 | 性能基线 |
|--|--------------|----------|
| 输入 | pytest `failed/total` | 场景 FPS / FrameTime / CPU / 温度 |
| 规则文件 | `gate.py` 固定规则 | `config/perf_baseline.yaml` |
| 失败含义 | 用例挂了，默认禁止合入 | 场景相对基线变差，需跟优化或放宽阈值 |
| AI 摘要 | 不参与 | 不参与 |

## 默认指标（演示）

见 `config/perf_baseline.yaml`：

- `avg_fps` / `min_fps`：越高越好（≥ 阈值）
- `frame_time_p95_ms`：越低越好（≤ 阈值）
- `avg_cpu_pct` / `max_temp_c`：可选；有值才参与判定

场景示例：`combat_dense`、`lobby`、`chapter_load`。

## 怎么用

### 只评估、不入库

`POST /api/perf/evaluate`

### 录入一次采样（自动评估）

`POST /api/perf/runs`

```json
{
  "scenario": "combat_dense",
  "device": "SM-G9880",
  "build": "1.0.0-dev.12",
  "metrics": {
    "avg_fps": 52.0,
    "min_fps": 41.0,
    "frame_time_p95_ms": 42.0,
    "avg_cpu_pct": 68.0,
    "max_temp_c": 41.0
  },
  "note": "PerfDog 战斗 5 分钟"
}
```

### 看板

打开 `/`，下方「性能基线采样」表会显示最近结果。

## 和 PerfDog 的对应关系

| 平台字段 | PerfDog 常见来源 |
|----------|------------------|
| avg_fps | FPS 平均值 |
| min_fps | FPS 最低值（或低分位） |
| frame_time_p95_ms | FrameTime 高分位 / 卡顿相关 |
| avg_cpu_pct | AppCPU 平均 |
| max_temp_c | Temperature 峰值 |

**定基线前先固定：** 机型、包体、亮度、网络、场景脚本、时长。变量不齐，数字不可比。

## 护栏

1. 一次采样不代表基线；基线应来自多轮稳定结果后再写进 yaml  
2. 性能 FAIL 与功能门禁分开看（本课不自动拦截 CI；需要时可后续接）  
3. 改阈值要留记录：为什么放宽 / 为什么收紧
