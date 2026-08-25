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


class GateEvaluateIn(BaseModel):
    passed: int = Field(ge=0)
    failed: int = Field(ge=0)
    total: int = Field(ge=0)
    ai_summary: str = ""


class GateEvaluateOut(BaseModel):
    passed: bool
    reason: str
    passed_count: int
    failed_count: int
    total: int
    rule: str


class PerfMetricsIn(BaseModel):
    avg_fps: float = Field(ge=0, examples=[57.2])
    min_fps: float = Field(ge=0, examples=[46.0])
    frame_time_p95_ms: float = Field(ge=0, examples=[38.5])
    avg_cpu_pct: float | None = Field(default=None, ge=0, examples=[62.0])
    max_temp_c: float | None = Field(default=None, ge=0, examples=[41.0])


class PerfEvaluateIn(BaseModel):
    scenario: str = Field(examples=["combat_dense"])
    metrics: PerfMetricsIn


class PerfCheckOut(BaseModel):
    name: str
    actual: float | None
    limit: float | None
    ok: bool
    detail: str


class PerfEvaluateOut(BaseModel):
    passed: bool
    reason: str
    scenario: str
    checks: list[PerfCheckOut]


class PerfRunCreate(BaseModel):
    scenario: str = Field(examples=["combat_dense"])
    device: str = Field(default="", examples=["SM-G9880"])
    build: str = Field(default="", examples=["1.0.0-dev.12"])
    metrics: PerfMetricsIn
    note: str = ""


class PerfRunOut(BaseModel):
    id: int
    scenario: str
    device: str
    build: str
    avg_fps: float
    min_fps: float
    frame_time_p95_ms: float
    avg_cpu_pct: float | None
    max_temp_c: float | None
    passed: bool
    reason: str
    note: str
    created_at: str
