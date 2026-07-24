# learn/lesson_a_practice.py

# 练习 1：变量
name = "ling"
status_code = 200
print("名字:", name)
print("状态码:", status_code)

# 练习 2：字典（模拟接口返回）
body = {
    "url": "https://postman-echo.com/get",
    "args": {"foo": "bar"}
}
print("url =", body["url"])
print("foo =", body["args"]["foo"])

# 练习 3：assert（故意留一题给你改）
assert status_code == 200
assert "url" in body
assert body["args"]["foo"] == "bar"

# 练习 4：故意失败一次（取消下面注释，看报错，再注释回去）
# assert status_code == 404

print("全部练习通过！")

test_zhuoye={
    "code": 0, "msg": "ok", "data": {"token": "abc123"}
}

assert test_zhuoye["code"]==0 and test_zhuoye["data"]["token"]=="abc123"

print("作业通过！")