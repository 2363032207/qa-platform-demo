# 补课 B：函数 + import 练习
# 运行方式（在项目根目录）：
#   .\.venv\Scripts\python.exe -m learn.lesson_b_practice

from learn.lesson_b_utils import build_url, check_status, get_timeout_or_default

def main():
    # 练习 1：调用自己写的函数
    url = build_url("https://postman-echo.com", "/get")
    print("完整地址:", url)
    assert url == "https://postman-echo.com/get"

    # 练习 2：用函数做断言检查
    result = check_status(200, expected=200)
    print("检查结果:", result)
    assert result is True

    # 练习 3：故意失败一次（看完报错后注释掉）
    #check_status(404, expected=200)
    #print("检测结果：", result)
    #assert result is False

    # 练习4：用函数获取 timeout，默认 10 秒
    data = {
        "timeout": 5,
    }
    timeout = get_timeout_or_default(data)
    print("timeout:", timeout)
    assert timeout == 5

    print("补课 B 练习通过！")


if __name__ == "__main__":
    main()
