"""第 7 课：测试平台 API 用例。"""

import pytest
from fastapi.testclient import TestClient

from qa_platform.database import init_db
from qa_platform.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """每个测试使用独立临时数据库。"""
    db_file = tmp_path / "test_platform.db"
    monkeypatch.setattr("qa_platform.database.DB_PATH", db_file)
    init_db()
    with TestClient(app) as test_client:
        yield test_client
    if db_file.exists():
        db_file.unlink()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_and_get_job(client):
    create_resp = client.post(
        "/api/jobs",
        json={"runner_type": "pytest", "params": {"tags": "smoke"}},
    )
    assert create_resp.status_code == 200
    job = create_resp.json()
    assert job["status"] == "queued"
    assert job["runner_type"] == "pytest"
    assert job["params"]["tags"] == "smoke"

    get_resp = client.get(f"/api/jobs/{job['id']}")
    assert get_resp.status_code == 200
    detail = get_resp.json()
    assert detail["id"] == job["id"]
    assert detail["result"] is None


def test_submit_result_updates_status(client):
    job = client.post("/api/jobs", json={}).json()

    result_resp = client.post(
        f"/api/jobs/{job['id']}/result",
        json={"passed": 12, "failed": 0, "total": 12, "message": "all green"},
    )
    assert result_resp.status_code == 200
    body = result_resp.json()
    assert body["passed"] == 12
    assert body["failed"] == 0

    detail = client.get(f"/api/jobs/{job['id']}").json()
    assert detail["status"] == "success"
    assert detail["result"]["message"] == "all green"


def test_list_jobs(client):
    client.post("/api/jobs", json={})
    client.post("/api/jobs", json={})
    rows = client.get("/api/jobs").json()
    assert len(rows) >= 2


def test_get_job_not_found(client):
    response = client.get("/api/jobs/99999")
    assert response.status_code == 404
