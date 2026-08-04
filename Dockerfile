FROM python:3.10-slim

WORKDIR /app

# 先装依赖，利用 Docker 层缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 默认跑全部测试；CI 可覆盖此命令
ENV QA_BASE_URL=https://postman-echo.com
ENV PYTHONUNBUFFERED=1
# 让 Python 能 import core、learn 等顶层包（Docker / 部分环境需要）
ENV PYTHONPATH=/app

RUN mkdir -p reports

CMD ["python", "-m", "pytest", "-v", "--tb=short", "--junitxml=reports/junit.xml"]
