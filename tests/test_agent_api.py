"""第 8 课：Agent 领取任务 + junit 解析。"""

from pathlib import Path

from agent.runner import parse_junit
from qa_platform.database import init_db
from qa_platform.main import app

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_platform.db"
    monkeypatch.setattr("qa_platform.database.DB_PATH", db_file)
    init_db()
    with TestClient(app) as test_client:
        yield test_client


def test_claim_next_job_and_submit(client):
    created = client.post(
        "/api/jobs",
        json={"runner_type": "pytest", "params": {"pytest_args": ["tests/test_network.py", "-q"]}},
    ).json()
    assert created["status"] == "queued"

    claim = client.post("/api/jobs/next")
    assert claim.status_code == 200
    job = claim.json()
    assert job["id"] == created["id"]
    assert job["status"] == "running"

    empty = client.post("/api/jobs/next")
    assert empty.status_code == 404

    result = client.post(
        f"/api/jobs/{job['id']}/result",
        json={"passed": 3, "failed": 0, "total": 3, "message": "agent ok"},
    )
    assert result.status_code == 200

    detail = client.get(f"/api/jobs/{job['id']}").json()
    assert detail["status"] == "success"
    assert detail["result"]["passed"] == 3


def test_claim_next_when_empty(client):
    response = client.post("/api/jobs/next")
    assert response.status_code == 404


def test_parse_junit(tmp_path: Path):
    xml = tmp_path / "junit.xml"
    xml.write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<testsuite name="pytest" tests="3" failures="1" errors="0" skipped="0">
  <testcase classname="t" name="a" time="0.1"/>
  <testcase classname="t" name="b" time="0.1">
    <failure message="boom">boom</failure>
  </testcase>
  <testcase classname="t" name="c" time="0.1"/>
</testsuite>
""",
        encoding="utf-8",
    )
    passed, failed, total = parse_junit(xml)
    assert total == 3
    assert failed == 1
    assert passed == 2
