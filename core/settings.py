"""从 config.yaml 加载配置，支持环境变量覆盖。"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.yaml"


def load_settings() -> dict[str, Any]:
    with _CONFIG_PATH.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    base_url = os.environ.get("QA_BASE_URL", data.get("base_url", "")).rstrip("/")
    timeout = int(os.environ.get("QA_TIMEOUT", data.get("timeout", 10)))

    if not base_url:
        raise ValueError("base_url 未配置，请检查 config/config.yaml 或 QA_BASE_URL")

    return {"base_url": base_url, "timeout": timeout}
