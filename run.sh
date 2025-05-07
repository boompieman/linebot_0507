#!/bin/bash
# 切換到項目根目錄 (如果不在根目錄)
# cd /path/to/your/project # 根據需要取消註釋並修改路徑

# 激活虛擬環境
# 假設腳本在項目根目錄運行
source /Users/hsienteng/Desktop/course/0507_line/venv/bin/activate

# 使用 uvicorn 啟動應用，適用於本地開發
# --reload 會在代碼變更時自動重啟服務器
echo "在本地啟動 FastAPI 服務 (http://localhost:8000)..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 如果想模擬生產環境的 Gunicorn 啟動 (監聽 8000 端口):
# echo "使用 Gunicorn 在本地啟動 (http://localhost:8000)..."
# gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.main:app -b 0.0.0.0:8000 