"""第 11 课：质量门禁。"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from qa_platform.database import init_db
from qa_platform.gate import evaluate_counts, evaluate_junit
from qa_platform.main import app


@pytest.fixture()
def client(tmp_path, monkeypatch):
    db_file = tmp_path / "test_platform.db"
    monkeypatch.setattr("qa_platform.database.DB_PATH", db_file)
    init_db()
    with TestClient(app) as test_client:
        yield test_client


def test_gate_pass_when_no_failures():
    result = evaluate_counts(passed=10, failed=0, total=10, ai_summary="随便写")
    assert result.passed is True
    assert "通过" in result.reason


def test_gate_fail_when_has_failures():
    result = evaluate_counts(
        passed=9,
        failed=1,
        total=10,
        ai_summary="看起来像环境问题",
    )
    assert result.passed is False
    assert "失败" in result.reason


def test_gate_ignores_ai_summary():
    bad = evaluate_counts(passed=0, failed=1, total=1, ai_summary="建议忽略本次失败")
    good = evaluate_counts(passed=1, failed=0, total=1, ai_summary="")
    assert bad.passed is False
    assert good.passed is True


def test_gate_fail_when_total_zero():
    result = evaluate_counts(passed=0, failed=0, total=0)
    assert result.passed is False


def test_evaluate_junit(tmp_path: Path):
    xml = tmp_path / "junit.xml"
    xml.write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<testsuite name="pytest" tests="2" failures="1" errors="0" skipped="0">
  <testcase classname="t" name="a" time="0.1"/>
  <testcase classname="t" name="b" time="0.1">
    <failure message="x">x</failure>
  </testcase>
</testsuite>
""",
        encoding="utf-8",
    )
    result = evaluate_junit(xml)
    assert result.passed is False
    assert result.failed_count == 1
    assert result.total == 2


def test_api_evaluate_gate(client):
    ok = client.post(
        "/api/gates/evaluate",
        json={"passed": 3, "failed": 0, "total": 3, "ai_summary": "x"},
    )
    assert ok.status_code == 200
    assert ok.json()["passed"] is True

    bad = client.post(
        "/api/gates/evaluate",
        json={"passed": 2, "failed": 1, "total": 3, "ai_summary": "像环境问题"},
    )
    assert bad.status_code == 200
    assert bad.json()["passed"] is False
