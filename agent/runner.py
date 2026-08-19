"""
Agent：领取任务 → 本地跑 pytest → 回传结果。

用法（先启动 API：.\\scripts\\run_api.ps1）：
  .\\.venv\\Scripts\\python.exe -m agent.runner --once
  .\\.venv\\Scripts\\python.exe -m agent.runner --loop --interval 5
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BASE_URL = "http://127.0.0.1:8000"
DEFAULT_PYTEST_ARGS = ["tests/test_network.py", "-q"]


def claim_job(base_url: str) -> dict | None:
    response = requests.post(f"{base_url.rstrip('/')}/api/jobs/next", timeout=10)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def run_pytest(pytest_args: list[str], report_path: Path) -> tuple[int, int, int, str]:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        *pytest_args,
        f"--junitxml={report_path}",
    ]
    completed = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    passed, failed, total = parse_junit(report_path)
    message = (completed.stdout or "")[-500:]
    if completed.returncode != 0 and failed == 0 and total == 0:
        # 未能解析报告时，用退出码兜底
        failed = 1
        total = max(total, 1)
        message = (completed.stderr or completed.stdout or "pytest failed")[-500:]
    return passed, failed, total, message.strip()


def parse_junit(report_path: Path) -> tuple[int, int, int]:
    if not report_path.exists():
        return 0, 0, 0
    root = ET.parse(report_path).getroot()
    # pytest 可能生成 testsuites 或 testsuite
    if root.tag == "testsuites":
        suites = list(root)
    else:
        suites = [root]

    total = failures = errors = skipped = 0
    for suite in suites:
        total += int(suite.attrib.get("tests", 0))
        failures += int(suite.attrib.get("failures", 0))
        errors += int(suite.attrib.get("errors", 0))
        skipped += int(suite.attrib.get("skipped", 0))

    failed = failures + errors
    passed = max(total - failed - skipped, 0)
    return passed, failed, total


def submit_result(
    base_url: str,
    job_id: int,
    passed: int,
    failed: int,
    total: int,
    message: str,
) -> dict:
    response = requests.post(
        f"{base_url.rstrip('/')}/api/jobs/{job_id}/result",
        json={
            "passed": passed,
            "failed": failed,
            "total": total,
            "message": message,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def resolve_pytest_args(job: dict) -> list[str]:
    params = job.get("params") or {}
    args = params.get("pytest_args")
    if isinstance(args, list) and args:
        return [str(x) for x in args]
    return list(DEFAULT_PYTEST_ARGS)


def process_one(base_url: str) -> bool:
    """领取并执行一个任务。有任务返回 True，无任务返回 False。"""
    job = claim_job(base_url)
    if job is None:
        print("没有排队中的任务（queued）")
        return False

    job_id = job["id"]
    pytest_args = resolve_pytest_args(job)
    print(f"领取任务 #{job_id}，执行: pytest {' '.join(pytest_args)}")

    report_path = PROJECT_ROOT / "reports" / f"agent-job-{job_id}.xml"
    passed, failed, total, message = run_pytest(pytest_args, report_path)
    result = submit_result(base_url, job_id, passed, failed, total, message)
    print(
        f"已回传 #{job_id}: passed={result['passed']} "
        f"failed={result['failed']} total={result['total']}"
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="QA Platform Agent")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--once", action="store_true", help="只处理一个任务后退出")
    parser.add_argument("--loop", action="store_true", help="循环领取任务")
    parser.add_argument("--interval", type=int, default=5, help="空闲时轮询秒数")
    args = parser.parse_args()

    if not args.once and not args.loop:
        args.once = True

    if args.once:
        process_one(args.base_url)
        return

    print(f"Agent 循环模式，interval={args.interval}s，Ctrl+C 退出")
    while True:
        try:
            had_job = process_one(args.base_url)
            if not had_job:
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nAgent 已停止")
            break
        except requests.RequestException as exc:
            print(f"请求平台失败: {exc}")
            time.sleep(args.interval)


if __name__ == "__main__":
    main()
