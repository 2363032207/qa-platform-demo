"""补课 C：class 和 self 练习模块。"""


class Dog:
    """最简单的类：狗会叫。"""

    def __init__(self, name: str):
        # self 代表「这只狗自己」
        self.name = name

    def bark(self):
        print(f"{self.name}: 汪汪！")


class MiniHttpClient:
    """简化版 HttpClient，帮助理解 self.base_url 是什么意思。"""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str) -> str:
        # 真实项目里这里会发网络请求；练习里只返回拼好的 URL
        full_url = self._url(path)
        return f"GET {full_url} (timeout={self.timeout}s)"

    def post(self, path: str, data: dict) -> str:
        full_url = self._url(path)
        return f"POST {full_url} (timeout={self.timeout}s, data={data})"

