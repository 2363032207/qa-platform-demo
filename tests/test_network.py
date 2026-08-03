"""第 5 课：网络异常（断网模拟、超时、重试）"""

from unittest.mock import MagicMock

import pytest
import requests

from core.http_client import HttpClient
from core.network import NetworkOfflineError, NetworkSimulator


@pytest.fixture(autouse=True)
def reset_network_simulator():
    NetworkSimulator.set_offline(False)
    yield
    NetworkSimulator.set_offline(False)


def test_offline_should_raise_network_offline_error():
    NetworkSimulator.set_offline(True)
    client = HttpClient(retry=0)

    with pytest.raises(NetworkOfflineError, match="网络不可用"):
        client.get("/get")


def test_retry_should_succeed_on_second_attempt(monkeypatch):
    client = HttpClient(retry=1)
    mock_request = MagicMock()
    mock_request.side_effect = [
        requests.Timeout("模拟超时"),
        MagicMock(status_code=200),
    ]
    monkeypatch.setattr(client.session, "request", mock_request)

    response = client.get("/get")

    assert response.status_code == 200
    assert mock_request.call_count == 2


def test_retry_exhausted_should_raise_timeout(monkeypatch):
    client = HttpClient(retry=1)
    mock_request = MagicMock(side_effect=requests.Timeout("模拟超时"))
    monkeypatch.setattr(client.session, "request", mock_request)

    with pytest.raises(requests.Timeout):
        client.get("/get")

    assert mock_request.call_count == 2
