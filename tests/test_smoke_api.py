"""第 2–3 课：接口冒烟（经 HttpClient + config）"""


def test_echo_get_should_return_200(api_client):
    """正常：GET 回显接口应返回 200，且响应里能看到 url"""
    response = api_client.get("/get")

    assert response.status_code == 200
    body = response.json()
    assert "url" in body


def test_echo_status_404_should_return_404(api_client):
    """异常：主动请求 status/404，应拿到 404"""
    response = api_client.get("/status/404")

    assert response.status_code == 404


def test_echo_get_with_query_foo(api_client):
    """S2：查询参数回显"""
    response = api_client.get("/get", params={"foo": "bar"})

    assert response.status_code == 200
    assert response.json()["args"]["foo"] == "bar"


def test_echo_post_json(api_client):
    """POST JSON 回显"""
    response = api_client.post("/post", json={"name": "ling"})

    assert response.status_code == 200
    assert response.json()["json"]["name"] == "ling"
