"""看板：汇总任务状态与通过率。"""

from __future__ import annotations

from qa_platform.schemas import JobDetailOut


def build_summary(jobs: list[JobDetailOut]) -> dict:
    total = len(jobs)
    success = sum(1 for j in jobs if j.status == "success")
    failed = sum(1 for j in jobs if j.status == "failed")
    pending = sum(1 for j in jobs if j.status in ("queued", "running"))

    passed_cases = sum(j.result.passed for j in jobs if j.result)
    total_cases = sum(j.result.total for j in jobs if j.result)
    if total_cases > 0:
        pass_rate = f"{round(passed_cases / total_cases * 100, 1)}%"
    else:
        pass_rate = "—"

    return {
        "total": total,
        "success": success,
        "failed": failed,
        "pending": pending,
        "pass_rate": pass_rate,
    }
