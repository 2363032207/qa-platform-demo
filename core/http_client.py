"""HTTP 驱动层：统一发请求、记日志、带超时。"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

from core.settings import load_settings

logger = logging.getLogger(__name__)


class HttpClient:
    def __init__(self, base_url: str | None = None, timeout: int | None = None) -> None:
        settings = load_settings()
        self.base_url = (base_url or settings["base_url"]).rstrip("/")
        self.timeout = timeout if timeout is not None else settings["timeout"]
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = self._url(path)
        timeout = kwargs.pop("timeout", self.timeout)
        started = time.perf_counter()

        response = self.session.request(method, url, timeout=timeout, **kwargs)
        elapsed_ms = (time.perf_counter() - started) * 1000

        logger.info(
            "%s %s -> %s (%.1f ms)",
            method,
            url,
            response.status_code,
            elapsed_ms,
        )
        return response

    def test_echo_post_json(api_client):
        response = api_client.post("/post", json={"name": "ling"})

        assert response.status_code == 200
        assert response.json()["json"]["name"] == "ling"
