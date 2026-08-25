"""第 12 课：性能基线。"""

import pytest
from fastapi.testclient import TestClient

from qa_platform.database import init_db
from qa_platform.main import app
from qa_platform.perf import evaluate_metrics, load_baseline, resolve_thresholds


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_platform.db"
    monkeypatch.setattr("qa_platform.database.DB_PATH", db_file)
    init_db()
    with TestClient(app) as test_client:
        yield test_client


def test_resolve_thresholds_merges_scenario():
    baseline = load_baseline()
    combat = resolve_thresholds("combat_dense", baseline)
    lobby = resolve_thresholds("lobby", baseline)
    assert combat["avg_fps_min"] == 50
    assert lobby["avg_fps_min"] == 55
    assert combat["avg_cpu_pct_max"] == baseline["defaults"]["avg_cpu_pct_max"]


def test_perf_pass_when_within_baseline():
    result = evaluate_metrics(
        "combat_dense",
        avg_fps=52,
        min_fps=42,
        frame_time_p95_ms=40,
        avg_cpu_pct=70,
        max_temp_c=42,
    )
    assert result.passed is True
    assert all(c.ok for c in result.checks)


def test_perf_fail_when_fps_low():
    result = evaluate_metrics(
        "combat_dense",
        avg_fps=30,
        min_fps=20,
        frame_time_p95_ms=80,
    )
    assert result.passed is False
    assert "avg_fps" in result.reason or "min_fps" in result.reason


def test_optional_metrics_skipped_when_absent():
    result = evaluate_metrics(
        "lobby",
        avg_fps=58,
        min_fps=52,
        frame_time_p95_ms=30,
    )
    names = {c.name for c in result.checks}
    assert "avg_cpu_pct" not in names
    assert "max_temp_c" not in names
    assert result.passed is True


def test_api_evaluate_and_store(client):
    dry = client.post(
        "/api/perf/evaluate",
        json={
            "scenario": "combat_dense",
            "metrics": {
                "avg_fps": 55,
                "min_fps": 45,
                "frame_time_p95_ms": 35,
                "avg_cpu_pct": 60,
                "max_temp_c": 40,
            },
        },
    )
    assert dry.status_code == 200
    assert dry.json()["passed"] is True

    created = client.post(
        "/api/perf/runs",
        json={
            "scenario": "combat_dense",
            "device": "SM-G9880",
            "build": "demo-1",
            "metrics": {
                "avg_fps": 30,
                "min_fps": 20,
                "frame_time_p95_ms": 80,
            },
            "note": "故意压低 FPS",
        },
    )
    assert created.status_code == 200
    body = created.json()
    assert body["passed"] is False
    assert body["device"] == "SM-G9880"

    listed = client.get("/api/perf/runs")
    assert listed.status_code == 200
    assert len(listed.json()) >= 1


def test_dashboard_shows_perf_section(client):
    client.post(
        "/api/perf/runs",
        json={
            "scenario": "lobby",
            "device": "SM-G9880",
            "build": "demo-1",
            "metrics": {"avg_fps": 58, "min_fps": 55, "frame_time_p95_ms": 30},
        },
    )
    page = client.get("/")
    assert page.status_code == 200
    assert "性能基线采样" in page.text
    assert "lobby" in page.text
