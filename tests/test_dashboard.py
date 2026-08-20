"""第 9 课：结果看板。"""

import pytest
from fastapi.testclient import TestClient

from qa_platform.dashboard import build_summary
from qa_platform.database import init_db
from qa_platform.main import app
from qa_platform.schemas import JobDetailOut, JobResultOut


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_platform.db"
    monkeypatch.setattr("qa_platform.database.DB_PATH", db_file)
    init_db()
    with TestClient(app) as test_client:
        yield test_client


def test_build_summary_empty():
    summary = build_summary([])
    assert summary["total"] == 0
    assert summary["pass_rate"] == "—"


def test_build_summary_with_results():
    jobs = [
        JobDetailOut(
            id=1,
            status="success",
            runner_type="pytest",
            params={},
            created_at="t",
            updated_at="t",
            result=JobResultOut(
                job_id=1,
                passed=3,
                failed=0,
                total=3,
                message="ok",
                created_at="t",
            ),
        ),
        JobDetailOut(
            id=2,
            status="failed",
            runner_type="pytest",
            params={},
            created_at="t",
            updated_at="t",
            result=JobResultOut(
                job_id=2,
                passed=1,
                failed=1,
                total=2,
                message="fail",
                created_at="t",
            ),
        ),
        JobDetailOut(
            id=3,
            status="queued",
            runner_type="pytest",
            params={},
            created_at="t",
            updated_at="t",
            result=None,
        ),
    ]
    summary = build_summary(jobs)
    assert summary["total"] == 3
    assert summary["success"] == 1
    assert summary["failed"] == 1
    assert summary["pending"] == 1
    assert summary["pass_rate"] == "80.0%"


def test_dashboard_page(client):
    job = client.post("/api/jobs", json={}).json()
    client.post(
        f"/api/jobs/{job['id']}/result",
        json={"passed": 3, "failed": 0, "total": 3, "message": "ok"},
    )
    response = client.get("/")
    assert response.status_code == 200
    html = response.text
    assert "QA Platform" in html
    assert "#1" in html or str(job["id"]) in html
    assert "success" in html
    assert "3 / 0 / 3" in html
