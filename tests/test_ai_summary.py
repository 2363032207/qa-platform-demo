"""第 10 课：失败摘要。"""

import pytest
from fastapi.testclient import TestClient

from qa_platform.ai_summary import summarize_failure
from qa_platform.database import init_db
from qa_platform.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_platform.db"
    monkeypatch.setattr("qa_platform.database.DB_PATH", db_file)
    init_db()
    with TestClient(app) as test_client:
        yield test_client


def test_rule_summary_extracts_failed_lines():
    text = summarize_failure(
        job_id=9,
        passed=2,
        failed=1,
        total=3,
        message=(
            "FAILED tests/test_smoke_driven.py::test_smoke_from_yaml[S5]\n"
            "E       assert 500 == 501\n"
        ),
    )
    assert "任务 #9" in text
    assert "FAILED" in text
    assert "assert 500 == 501" in text
    assert "[推测]" in text


def test_summary_skipped_when_no_failure():
    text = summarize_failure(
        job_id=1,
        passed=3,
        failed=0,
        total=3,
        message="all green",
    )
    assert text == ""


def test_submit_result_writes_ai_summary(client):
    job = client.post("/api/jobs", json={}).json()
    response = client.post(
        f"/api/jobs/{job['id']}/result",
        json={
            "passed": 2,
            "failed": 1,
            "total": 3,
            "message": "FAILED tests/demo.py::test_x\nE       assert 1 == 2\n",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["failed"] == 1
    assert body["ai_summary"]
    assert "任务 #" in body["ai_summary"]

    detail = client.get(f"/api/jobs/{job['id']}").json()
    assert detail["status"] == "failed"
    assert detail["result"]["ai_summary"]


def test_dashboard_shows_ai_summary(client):
    job = client.post("/api/jobs", json={}).json()
    client.post(
        f"/api/jobs/{job['id']}/result",
        json={
            "passed": 0,
            "failed": 1,
            "total": 1,
            "message": "FAILED tests/a.py::test_a\nE       assert False\n",
        },
    )
    html = client.get("/").text
    assert "失败摘要" in html
    assert "任务 #" in html
