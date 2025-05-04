FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 启动命令：使用 Gunicorn 和 Uvicorn worker
# -w 4: 啟動 4 個 worker 進程 (可以根據需要調整)
# -k uvicorn.workers.UvicornWorker: 指定使用 Uvicorn worker
# app.main:app: 指向您的 FastAPI 應用實例
# -b 0.0.0.0:8000: 綁定監聽的地址和端口
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "-b", "0.0.0.0:8000"] 