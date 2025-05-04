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
   source venv/bin/activate  # 在Windows上使用: .\\venv\\Scripts\\activate
   ```

3. 安裝依賴
   ```bash
   pip install -r requirements.txt
   ```

4. 配置環境變數
   - 建立`.env`文件，添加以下內容：
     ```
     # LINE Bot 配置
     LINE_CHANNEL_SECRET=your_line_channel_secret
     LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
     
     # OpenAI 配置
     OPENAI_API_KEY=your_openai_api_key
     
     # 應用配置 
     DEBUG=false
     ```
   - 將各項替換為實際的值

### 運行應用

```bash
python app/main.py
```

應用將在 http://localhost:8000 上運行。

## Docker 部署

本項目支持使用Docker進行部署，這種方式更加簡便且易於在不同環境中運行。

### 使用Docker部署

1. 構建Docker鏡像
   ```bash
   docker build -t linebot .
   ```

2. 運行Docker容器
   ```bash
   docker run -p 8000:8000 --env-file .env linebot
   ```

### 使用Docker Compose部署

1. 確保已安裝Docker和Docker Compose

2. 運行容器
   ```bash
   docker-compose up -d
   ```

3. 查看日誌
   ```bash
   docker-compose logs -f
   ```

## 雲平台部署

### Zeabur部署

Zeabur提供了簡單便捷的部署方式：

1. 註冊並登錄[Zeabur](https://zeabur.com)
2. 創建一個新項目
3. 將代碼部署到GitHub
4. 在Zeabur中選擇"從GitHub導入"
5. 選擇您的倉庫
6. 設置環境變數：
   - `LINE_CHANNEL_SECRET`: LINE頻道密鑰
   - `LINE_CHANNEL_ACCESS_TOKEN`: LINE頻道訪問令牌
   - `OPENAI_API_KEY`: OpenAI API金鑰
7. 部署完成後，獲取分配的URL
8. 在LINE Developer Console設置Webhook URL為`您的域名/callback`

#### Zeabur部署疑難排解

如果在Zeabur部署中遇到`python: can't open file '/app/main.py'`錯誤：

1. 確保Dockerfile中的CMD命令正確指向主應用文件：
   ```
   CMD ["python", "app/main.py"]
   ```

2. 您也可以在Zeabur的服務設置中修改啟動命令為：
   ```
   python app/main.py
   ```

## 注意事項

- 此應用使用OpenAI API，可能產生費用
- 確保LINE Bot的Webhook URL使用HTTPS
- 在生產環境中不要使用調試模式

## 授權條款

MIT License 