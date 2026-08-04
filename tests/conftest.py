"""pytest 公共 fixture。"""

import logging
import sys
from pathlib import Path

import pytest

# 保证项目根目录在 import 路径中（Docker / 不同启动方式下更稳）
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from core.http_client import HttpClient


@pytest.fixture(scope="session")
def api_client() -> HttpClient:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return HttpClient()
