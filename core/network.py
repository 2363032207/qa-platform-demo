"""网络模拟：断网、离线开关（测试用）。"""


class NetworkOfflineError(ConnectionError):
    """模拟网络不可用。"""


class NetworkSimulator:
    """在测试或 Debug 构建中模拟断网。"""

    force_offline: bool = False

    @classmethod
    def is_offline(cls) -> bool:
        return cls.force_offline

    @classmethod
    def set_offline(cls, offline: bool = True) -> None:
        cls.force_offline = offline
