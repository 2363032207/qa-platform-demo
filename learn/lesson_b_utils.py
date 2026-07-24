"""补课 B 小工具模块：演示 import 怎么用。"""


def build_url(base_url: str, path: str) -> str:
    """把 base_url 和 path 拼成完整 URL。"""
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def check_status(actual: int, expected: int) -> bool:
    """检查状态码是否符合预期。"""
    if actual != expected:
        raise ValueError(f"状态码不对：期望 {expected}，实际 {actual}")
    return True

def get_timeout_or_default(data: dict, default: int = 10) -> int:
    """从字典 data 取 timeout，没有就返回 default。"""
    # 你来写：提示用 data.get("timeout", default)
    return data.get("timeout", default)