"""FastAPI 入口。"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from qa_platform.database import init_db
from qa_platform.repository import create_job, get_job, list_jobs, submit_result
from qa_platform.schemas import JobCreate, JobDetailOut, JobOut, JobResultCreate, JobResultOut


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="QA Platform Demo",
    description="迷你测试平台 API（第 7 课）",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/jobs", response_model=JobOut)
def api_create_job(payload: JobCreate) -> JobOut:
    return create_job(payload)


@app.get("/api/jobs", response_model=list[JobOut])
def api_list_jobs(limit: int = 20) -> list[JobOut]:
    return list_jobs(limit=limit)


@app.get("/api/jobs/{job_id}", response_model=JobDetailOut)
def api_get_job(job_id: int) -> JobDetailOut:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job


@app.post("/api/jobs/{job_id}/result", response_model=JobResultOut)
def api_submit_result(job_id: int, payload: JobResultCreate) -> JobResultOut:
    result = submit_result(job_id, payload)
    if result is None:
        raise HTTPException(status_code=404, detail="job not found")
    return result
