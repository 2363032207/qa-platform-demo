# 补课 B 笔记（请用自己的话补全）

## 1. 函数 def 解决什么问题？

可以避免重复编写代码，在需要的时候调用就可以

## 2. import 是干什么的？

使用其他文件里的代码

## 3. settings.py 里 load_settings() 做了哪几步？

1. 打开并读取 `config.yaml` → 得到字典 `data`
2. 取 `base_url`（环境变量优先，否则用 yaml）
3. 取 `timeout`（同样逻辑，转成整数）
4. 没有 `base_url` 就报错；否则 `return {"base_url": ..., "timeout": ...}`

`docs/python-lesson-b.md` 第 4 题输出里可以补上 `timeout: 5` 那一行，和实际一致。

## 4. 运行 learn/lesson_b_practice.py 的输出

```text
完整地址: https://postman-echo.com/get
检查结果: True
补课 B 练习通过！
```

