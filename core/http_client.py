"""HTTP 驱动层：统一发请求、记日志、带超时与网络重试。"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

from core.network import NetworkOfflineError, NetworkSimulator
from core.settings import load_settings

logger = logging.getLogger(__name__)


class HttpClient:
    """HTTP 客户端"""

    def __init__(self, base_url: str | None = None, timeout: int | None = None, retry: int | None = None) -> None:
        settings = load_settings()
        self.base_url = (base_url or settings["base_url"]).rstrip("/")
        self.timeout = timeout if timeout is not None else settings["timeout"]
        self.retry = retry if retry is not None else settings["retry"]
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
        if NetworkSimulator.is_offline():
            raise NetworkOfflineError("网络不可用（NetworkSimulator.force_offline=True）")

        url = self._url(path)
        timeout = kwargs.pop("timeout", self.timeout)
        max_retries = kwargs.pop("max_retries", self.retry)

        last_error: Exception | None = None
        for attempt in range(max_retries + 1):
            started = time.perf_counter()
            try:
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
            except (requests.Timeout, requests.ConnectionError) as exc:
                last_error = exc
                elapsed_ms = (time.perf_counter() - started) * 1000
                logger.warning(
                    "%s %s 网络异常 (%.1f ms, attempt=%s/%s): %s",
                    method,
                    url,
                    elapsed_ms,
                    attempt + 1,
                    max_retries + 1,
                    exc,
                )
                if attempt >= max_retries:
                    raise

        if last_error:
            raise last_error
        raise RuntimeError("请求失败，但未捕获到异常")
