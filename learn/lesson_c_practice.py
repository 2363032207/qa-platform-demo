# 补课 C：class + self 练习
# 运行：.\.venv\Scripts\python.exe -m learn.lesson_c_practice

from learn.lesson_c_models import Dog, MiniHttpClient


def main():
    # 练习 1：创建对象（实例）
    dog1 = Dog("旺财")
    dog2 = Dog("小黑")
    dog1.bark()  # 旺财: 汪汪！
    dog2.bark()  # 小黑: 汪汪！

    # 练习 2：每只狗有自己的 name（self 保存各自的数据）
    assert dog1.name == "旺财"
    assert dog2.name == "小黑"

    # 练习 3：MiniHttpClient 类比真实 HttpClient
    client = MiniHttpClient("https://postman-echo.com", timeout=10)
    msg = client.get("/get")
    print(msg)
    msg1 = client.post("/post", {"key": "value"})
    print(msg1)
    assert "https://postman-echo.com/get" in msg
    assert "timeout=10s" in msg
    assert "https://postman-echo.com/post" in msg1

    # 练习 4：两个 client 互不影响
    client_fast = MiniHttpClient("https://a.com", timeout=3)
    client_slow = MiniHttpClient("https://b.com", timeout=30)
    assert client_fast.timeout == 3
    assert client_slow.timeout == 30

    print("补课 C 练习通过！")


if __name__ == "__main__":
    main()
