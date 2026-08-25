"""FastAPI 入口。"""

from __future__ import annotations

from contextlib import asynccontextmanager

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from qa_platform.dashboard import build_summary
from qa_platform.database import init_db
from qa_platform.repository import (
    claim_next_job,
    create_job,
    get_job,
    list_job_details,
    list_jobs,
    submit_result,
)
from qa_platform.schemas import JobCreate, JobDetailOut, JobOut, JobResultCreate, JobResultOut


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="QA Platform Demo",
    description="迷你测试平台 API（第 7～10 课）",
    version="0.4.0",
    lifespan=lifespan,
)

_TEMPLATES = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    jobs = list_job_details(limit=50)
    return _TEMPLATES.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "jobs": jobs,
            "summary": build_summary(jobs),
        },
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


@app.post("/api/jobs/next", response_model=JobOut)
def api_claim_next_job() -> JobOut:
    """Agent 领取下一个排队任务（queued → running）。"""
    job = claim_next_job()
    if job is None:
        raise HTTPException(status_code=404, detail="no queued job")
    return job


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
