"""性能采样入库（第 12 课）。"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from qa_platform.database import get_connection
from qa_platform.perf import evaluate_metrics
from qa_platform.schemas import PerfRunCreate, PerfRunOut


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_perf_run(payload: PerfRunCreate) -> PerfRunOut:
    m = payload.metrics
    result = evaluate_metrics(
        payload.scenario,
        avg_fps=m.avg_fps,
        min_fps=m.min_fps,
        frame_time_p95_ms=m.frame_time_p95_ms,
        avg_cpu_pct=m.avg_cpu_pct,
        max_temp_c=m.max_temp_c,
    )
    now = _now()
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO perf_runs (
            scenario, device, build,
            avg_fps, min_fps, frame_time_p95_ms, avg_cpu_pct, max_temp_c,
            passed, reason, note, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            payload.scenario,
            payload.device,
            payload.build,
            m.avg_fps,
            m.min_fps,
            m.frame_time_p95_ms,
            m.avg_cpu_pct,
            m.max_temp_c,
            1 if result.passed else 0,
            result.reason,
            payload.note,
            now,
        ),
    )
    run_id = cursor.lastrowid
    conn.commit()
    row = conn.execute("SELECT * FROM perf_runs WHERE id = ?", (run_id,)).fetchone()
    conn.close()
    return _row_to_perf_run(row)


def list_perf_runs(limit: int = 20) -> list[PerfRunOut]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM perf_runs ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [_row_to_perf_run(row) for row in rows]


def _row_to_perf_run(row: Any) -> PerfRunOut:
    return PerfRunOut(
        id=row["id"],
        scenario=row["scenario"],
        device=row["device"] or "",
        build=row["build"] or "",
        avg_fps=row["avg_fps"],
        min_fps=row["min_fps"],
        frame_time_p95_ms=row["frame_time_p95_ms"],
        avg_cpu_pct=row["avg_cpu_pct"],
        max_temp_c=row["max_temp_c"],
        passed=bool(row["passed"]),
        reason=row["reason"] or "",
        note=row["note"] or "",
        created_at=row["created_at"],
    )
