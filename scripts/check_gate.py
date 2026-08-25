"""
质量门禁 CLI：根据 junit 报告判定是否放行。

用法：
  python scripts/check_gate.py reports/junit.xml

退出码：
  0 = 门禁通过
  1 = 门禁未通过
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from qa_platform.gate import evaluate_junit


def main() -> int:
    parser = argparse.ArgumentParser(description="QA quality gate checker")
    parser.add_argument(
        "junit",
        nargs="?",
        default="reports/junit.xml",
        help="junit xml path",
    )
    parser.add_argument("--json", action="store_true", help="print JSON result")
    args = parser.parse_args()

    result = evaluate_junit(args.junit)
    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        status = "PASS" if result.passed else "FAIL"
        print(f"[GATE {status}] {result.reason}")
        print(
            f"counts: passed={result.passed_count} "
            f"failed={result.failed_count} total={result.total}"
        )
        print(f"rule: {result.rule} （ai_summary 不参与判定）")

    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
