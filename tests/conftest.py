"""pytest 公共 fixture。"""

import logging

import pytest

from core.http_client import HttpClient


@pytest.fixture(scope="session")
def api_client() -> HttpClient:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    return HttpClient()
