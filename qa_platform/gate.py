"""质量门禁：根据真实测试结果判定是否放行。

护栏：
- AI 摘要（ai_summary）绝不改变门禁结论
- 仅以 passed / failed / total（或 junit）为准
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from agent.runner import parse_junit


@dataclass
class GateResult:
    passed: bool
    reason: str
    passed_count: int
    failed_count: int
    total: int
    rule: str = "failed == 0"

    def to_dict(self) -> dict:
        return asdict(self)


def evaluate_counts(
    *,
    passed: int,
    failed: int,
    total: int,
    ai_summary: str = "",
) -> GateResult:
    """按用例计数判定门禁。ai_summary 仅作备注，不参与判定。"""
    _ = ai_summary  # 显式忽略，防止误用

    if total <= 0:
        return GateResult(
            passed=False,
            reason="门禁未通过：没有执行任何用例（total=0）",
            passed_count=passed,
            failed_count=failed,
            total=total,
        )

    if failed > 0:
        return GateResult(
            passed=False,
            reason=f"门禁未通过：存在 {failed} 条失败用例，禁止合入/放行",
            passed_count=passed,
            failed_count=failed,
            total=total,
        )

    return GateResult(
        passed=True,
        reason=f"门禁通过：全部 {total} 条用例通过",
        passed_count=passed,
        failed_count=failed,
        total=total,
    )


def evaluate_junit(report_path: str | Path) -> GateResult:
    path = Path(report_path)
    if not path.exists():
        return GateResult(
            passed=False,
            reason=f"门禁未通过：找不到报告文件 {path}",
            passed_count=0,
            failed_count=0,
            total=0,
        )

    passed, failed, total = parse_junit(path)
    return evaluate_counts(passed=passed, failed=failed, total=total)
