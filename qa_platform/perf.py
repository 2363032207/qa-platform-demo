"""性能基线对比（第 12 课）。

门禁认功能用例计数；本模块认场景指标是否压过基线。
录入的数据通常来自 PerfDog / 自研采样，平台只做入库与对比。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

_BASELINE_PATH = Path(__file__).resolve().parent.parent / "config" / "perf_baseline.yaml"


@dataclass
class CheckItem:
    name: str
    actual: float | None
    limit: float | None
    ok: bool
    detail: str


@dataclass
class PerfEvaluateResult:
    passed: bool
    reason: str
    scenario: str
    checks: list[CheckItem] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "reason": self.reason,
            "scenario": self.scenario,
            "checks": [
                {
                    "name": c.name,
                    "actual": c.actual,
                    "limit": c.limit,
                    "ok": c.ok,
                    "detail": c.detail,
                }
                for c in self.checks
            ],
        }


def load_baseline(path: Path | None = None) -> dict[str, Any]:
    cfg_path = path or _BASELINE_PATH
    with cfg_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if "defaults" not in data:
        raise ValueError("perf_baseline.yaml 缺少 defaults")
    return data


def resolve_thresholds(scenario: str, baseline: dict[str, Any] | None = None) -> dict[str, float]:
    """合并 defaults 与场景覆盖。"""
    data = baseline or load_baseline()
    thresholds = dict(data.get("defaults") or {})
    scenarios = data.get("scenarios") or {}
    if scenario in scenarios:
        for key, value in scenarios[scenario].items():
            if key == "description":
                continue
            thresholds[key] = value
    return thresholds


def evaluate_metrics(
    scenario: str,
    *,
    avg_fps: float,
    min_fps: float,
    frame_time_p95_ms: float,
    avg_cpu_pct: float | None = None,
    max_temp_c: float | None = None,
    baseline: dict[str, Any] | None = None,
) -> PerfEvaluateResult:
    """对比单次采样与基线。缺省可选指标（CPU/温度）不参与判定。"""
    thresholds = resolve_thresholds(scenario, baseline)
    checks: list[CheckItem] = []

    def _min_ok(name: str, actual: float, limit_key: str) -> None:
        limit = float(thresholds[limit_key])
        ok = actual >= limit
        checks.append(
            CheckItem(
                name=name,
                actual=actual,
                limit=limit,
                ok=ok,
                detail=f"{actual} >= {limit}" if ok else f"{actual} < {limit}",
            )
        )

    def _max_ok(name: str, actual: float, limit_key: str) -> None:
        limit = float(thresholds[limit_key])
        ok = actual <= limit
        checks.append(
            CheckItem(
                name=name,
                actual=actual,
                limit=limit,
                ok=ok,
                detail=f"{actual} <= {limit}" if ok else f"{actual} > {limit}",
            )
        )

    _min_ok("avg_fps", avg_fps, "avg_fps_min")
    _min_ok("min_fps", min_fps, "min_fps_min")
    _max_ok("frame_time_p95_ms", frame_time_p95_ms, "frame_time_p95_ms_max")

    if avg_cpu_pct is not None and "avg_cpu_pct_max" in thresholds:
        _max_ok("avg_cpu_pct", avg_cpu_pct, "avg_cpu_pct_max")
    if max_temp_c is not None and "max_temp_c_max" in thresholds:
        _max_ok("max_temp_c", max_temp_c, "max_temp_c_max")

    failed = [c for c in checks if not c.ok]
    if not failed:
        return PerfEvaluateResult(
            passed=True,
            reason=f"场景 {scenario} 性能达标（相对基线）",
            scenario=scenario,
            checks=checks,
        )
    names = ", ".join(c.name for c in failed)
    return PerfEvaluateResult(
        passed=False,
        reason=f"场景 {scenario} 未达基线：{names}",
        scenario=scenario,
        checks=checks,
    )
