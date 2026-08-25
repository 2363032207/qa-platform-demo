"""平台 API 请求/响应模型。"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

JobStatus = Literal["queued", "running", "success", "failed"]


class JobCreate(BaseModel):
    runner_type: str = Field(default="pytest", examples=["pytest"])
    params: dict[str, Any] = Field(default_factory=dict)


class JobOut(BaseModel):
    id: int
    status: JobStatus
    runner_type: str
    params: dict[str, Any]
    created_at: str
    updated_at: str


class JobResultCreate(BaseModel):
    passed: int = Field(ge=0)
    failed: int = Field(ge=0)
    total: int = Field(ge=0)
    message: str = ""


class JobResultOut(BaseModel):
    job_id: int
    passed: int
    failed: int
    total: int
    message: str
    ai_summary: str = ""
    created_at: str


class JobDetailOut(JobOut):
    result: JobResultOut | None = None
