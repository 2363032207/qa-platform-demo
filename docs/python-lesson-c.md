# 补课 C 笔记（请用自己的话补全）

## 1. class 和 def 函数有什么区别？

class是类，一种工具模板，可以将函数这种工具打包在一起，def是函数，算是一种特定的工具，每次使用就是在使用他的方法

## 2. self 是什么？为什么方法里第一个参数要写 self？

self是当前的对象，为了接收传进来的对象，在定义函数时，就必须在第一个位置留个坑位。

## 3. `api_client = HttpClient()` 这行代码发生了什么？

调用 `HttpClient()` 时会执行 `__init__`：读 config，把 `base_url`、`timeout`、`session` 挂到这只 client 上。

## 4. 运行 learn/lesson_c_practice.py 的输出

```text
旺财: 汪汪！
小黑: 汪汪！
GET https://postman-echo.com/get (timeout=10s)
POST https://postman-echo.com/post (timeout=10s, data={'key': 'value'})
补课 C 练习通过！
```

