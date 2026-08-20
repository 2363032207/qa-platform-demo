"""测试任务 CRUD（SQLite）。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from qa_platform.database import get_connection
from qa_platform.schemas import JobCreate, JobDetailOut, JobOut, JobResultCreate, JobResultOut


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_job(payload: JobCreate) -> JobOut:
    now = _now()
    conn = get_connection()
    cursor = conn.execute(
        """
        INSERT INTO jobs (status, runner_type, params, created_at, updated_at)
        VALUES ('queued', ?, ?, ?, ?)
        """,
        (payload.runner_type, json.dumps(payload.params), now, now),
    )
    job_id = cursor.lastrowid
    conn.commit()
    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    conn.close()
    return _row_to_job(row)


def list_jobs(limit: int = 20) -> list[JobOut]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM jobs ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    conn.close()
    return [_row_to_job(row) for row in rows]


def list_job_details(limit: int = 20) -> list[JobDetailOut]:
    """任务列表 + 结果，供看板使用。"""
    jobs = list_jobs(limit=limit)
    details: list[JobDetailOut] = []
    for job in jobs:
        detail = get_job(job.id)
        if detail is not None:
            details.append(detail)
    return details


def claim_next_job() -> JobOut | None:
    """领取最早一条 queued 任务，状态改为 running（供 Agent 使用）。"""
    conn = get_connection()
    row = conn.execute(
        """
        SELECT * FROM jobs
        WHERE status = 'queued'
        ORDER BY id ASC
        LIMIT 1
        """
    ).fetchone()
    if row is None:
        conn.close()
        return None

    now = _now()
    conn.execute(
        "UPDATE jobs SET status = 'running', updated_at = ? WHERE id = ? AND status = 'queued'",
        (now, row["id"]),
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM jobs WHERE id = ?", (row["id"],)).fetchone()
    conn.close()
    return _row_to_job(updated)


def get_job(job_id: int) -> JobDetailOut | None:
    conn = get_connection()
    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        conn.close()
        return None

    result_row = conn.execute(
        "SELECT * FROM job_results WHERE job_id = ?",
        (job_id,),
    ).fetchone()
    conn.close()

    job = _row_to_job(row)
    result = _row_to_result(result_row) if result_row else None
    return JobDetailOut(**job.model_dump(), result=result)


def submit_result(job_id: int, payload: JobResultCreate) -> JobResultOut | None:
    conn = get_connection()
    job = conn.execute("SELECT id FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if job is None:
        conn.close()
        return None

    now = _now()
    status = "success" if payload.failed == 0 else "failed"
    conn.execute(
        """
        INSERT INTO job_results (job_id, passed, failed, total, message, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(job_id) DO UPDATE SET
            passed=excluded.passed,
            failed=excluded.failed,
            total=excluded.total,
            message=excluded.message,
            created_at=excluded.created_at
        """,
        (job_id, payload.passed, payload.failed, payload.total, payload.message, now),
    )
    conn.execute(
        "UPDATE jobs SET status = ?, updated_at = ? WHERE id = ?",
        (status, now, job_id),
    )
    conn.commit()
    row = conn.execute(
        "SELECT * FROM job_results WHERE job_id = ?",
        (job_id,),
    ).fetchone()
    conn.close()
    return _row_to_result(row)


def _row_to_job(row: Any) -> JobOut:
    return JobOut(
        id=row["id"],
        status=row["status"],
        runner_type=row["runner_type"],
        params=json.loads(row["params"] or "{}"),
        created_at=row["created_at"],
        updated_at=row["updated_at"],
    )


def _row_to_result(row: Any) -> JobResultOut:
    return JobResultOut(
        job_id=row["job_id"],
        passed=row["passed"],
        failed=row["failed"],
        total=row["total"],
        message=row["message"] or "",
        created_at=row["created_at"],
    )
