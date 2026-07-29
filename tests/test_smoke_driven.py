"""第 4 课：数据驱动冒烟（用例来自 config/smoke_cases.yaml）"""

import pytest

from core.case_loader import get_json_value, load_smoke_cases

SMOKE_CASES = load_smoke_cases()


@pytest.mark.parametrize("case", SMOKE_CASES, ids=[c["id"] for c in SMOKE_CASES])
def test_smoke_from_yaml(api_client, case):
    method = case["method"].upper()
    path = case["path"]
    kwargs = {}

    if "params" in case:
        kwargs["params"] = case["params"]
    if "json_body" in case:
        kwargs["json"] = case["json_body"]

    if method == "GET":
        response = api_client.get(path, **kwargs)
    elif method == "POST":
        response = api_client.post(path, **kwargs)
    else:
        raise ValueError(f"暂不支持的 method: {method}")

    assert response.status_code == case["expected_status"]

    if "json_contains_key" in case:
        body = response.json()
        assert case["json_contains_key"] in body

    if "json_path" in case:
        actual = get_json_value(response.json(), case["json_path"])
        assert actual == case["expected_value"]
