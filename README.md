# LINE Bot with ChatGPT Integration

一個使用FastAPI框架開發的LINE機器人，整合了OpenAI的LLM功能。

## 功能特色

- 接收用戶的LINE文字訊息
- 使用OpenAI的GPT模型生成回應
- 將AI生成的回應傳送回LINE用戶

## 開發環境設置

### 前置需求

- Python 3.8+
- LINE Developer帳號
- OpenAI API金鑰

### 安裝步驟

1. 克隆此專案
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. 建立虛擬環境
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # 在Windows上使用: .\venv\Scripts\activate
   ```

3. 安裝依賴
   ```bash
   pip install -r requirements.txt
   ```

4. 配置環境變數
   - 複製`.env.example`為`.env`
   - 填入你的LINE Channel Secret、Channel Access Token和OpenAI API Key

### 運行應用

```bash
cd app
python run.py
```

應用將在 http://localhost:8000 上運行。

## 部署指南

1. 在你選擇的雲平台上部署應用
2. 確保設置環境變數
3. 在LINE Developer Console中更新Webhook URL為你的部署URL + `/callback`
4. 啟用Webhook功能

## 注意事項

- 此應用使用OpenAI API，可能產生費用
- 確保LINE Bot的Webhook URL使用HTTPS
- 在生產環境中不要使用`reload=True`

## 授權條款

MIT License 