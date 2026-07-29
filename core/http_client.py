"""HTTP 驱动层：统一发请求、记日志、带超时。"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

from core.settings import load_settings

logger = logging.getLogger(__name__)


class HttpClient:
    """HTTP 客户端"""
    def __init__(self, base_url: str | None = None, timeout: int | None = None) -> None:
        """初始化 HTTP 客户端"""
        settings = load_settings()
        self.base_url = (base_url or settings["base_url"]).rstrip("/")
        self.timeout = timeout if timeout is not None else settings["timeout"]
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        """构建 URL"""
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        """发送 GET 请求"""
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        """发送 POST 请求"""
        return self._request("POST", path, **kwargs)

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        """发送请求"""
        url = self._url(path)
        timeout = kwargs.pop("timeout", self.timeout)
        started = time.perf_counter()
        
        response = self.session.request(method, url, timeout=timeout, **kwargs)
        elapsed_ms = (time.perf_counter() - started) * 1000
        #记录日志
        logger.info(
            "%s %s -> %s (%.1f ms)",
            method,
            url,
            response.status_code,
            elapsed_ms,
        )
        return response
