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

# 启动命令，使用uvicorn启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 