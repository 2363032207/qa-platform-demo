"""第 2 课：接口冒烟用例（使用公开练习接口 postman-echo.com）"""

import requests

BASE_URL = "https://postman-echo.com"


def test_echo_get_should_return_200():
    """正常：GET 回显接口应返回 200，且响应里能看到 url"""
    response = requests.get(f"{BASE_URL}/get", timeout=10)

    assert response.status_code == 200
    body = response.json()
    assert "url" in body


def test_echo_status_404_should_return_404():
    """异常：主动请求 status/404，应拿到 404（练习断言失败状态码）"""
    response = requests.get(f"{BASE_URL}/status/404", timeout=10)

    assert response.status_code == 404

def test_echo_get_with_query_foo():
    response = requests.get(f"{BASE_URL}/get", params={"foo": "bar"}, timeout=10)
    assert response.status_code == 200
    assert response.json()["args"]["foo"] == "bar"