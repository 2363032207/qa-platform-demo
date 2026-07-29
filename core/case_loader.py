"""从 YAML 加载数据驱动用例。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_CASES_PATH = Path(__file__).resolve().parent.parent / "config" / "smoke_cases.yaml"


def load_smoke_cases() -> list[dict[str, Any]]:
    with _CASES_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    cases = data.get("cases", [])
    if not cases:
        raise ValueError(f"未找到用例，请检查 {_CASES_PATH}")

    for case in cases:
        if "id" not in case or "method" not in case or "path" not in case:
            raise ValueError(f"用例字段不完整: {case}")

    return cases


def get_json_value(body: dict[str, Any], json_path: str) -> Any:
    """按点号路径取值，例如 args.foo -> body['args']['foo']"""
    value: Any = body
    for key in json_path.split("."):
        value = value[key]
    return value
