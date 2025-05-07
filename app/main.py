#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from dotenv import load_dotenv  # 用於本地開發載入 .env 檔案中的環境變數

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

# 導入LINE SDK模組
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3 import (
    WebhookHandler
)
# 導入OpenAI SDK模組
from openai import OpenAI
from openai import APIConnectionError, RateLimitError, APIStatusError

# 載入環境變數，用於本地開發
load_dotenv()

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 獲取環境變數
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- LINE Bot SDK 設定 ---
if not LINE_CHANNEL_SECRET:
    logger.error("LINE_CHANNEL_SECRET 未設定")
    # 在實際應用中，你可能想要拋出錯誤或退出
    # 為了此範例，我們允許應用程式啟動，但 webhook 會失敗
if not LINE_CHANNEL_ACCESS_TOKEN:
    logger.error("LINE_CHANNEL_ACCESS_TOKEN 未設定")
    # 與 LINE_CHANNEL_SECRET 類似，適當處理

# 使用LINE_CHANNEL_ACCESS_TOKEN初始化LINE SDK配置
configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
# 注意：我們在請求範圍外創建API客戶端和處理程序以重用
# 客戶端需要管理，例如在上下文管理器或依賴注入中
# 為了簡單起見，我們將使用類似全局的方法，但對於FastAPI，依賴注入更好

# 創建Messaging API客戶端和Webhook處理程序
line_bot_api = MessagingApi(ApiClient(configuration))
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# --- OpenAI SDK 設定 ---
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY 未設定")
    # 適當處理

# 創建OpenAI客戶端
# 為了簡化，在同步WebhookHandler調度中使用同步客戶端
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# --- FastAPI 應用程式 ---
app = FastAPI()

# --- Webhook 端點 ---
@app.post("/callback")
async def callback(request: Request):
    """
    處理LINE webhook事件。
    驗證簽章並將事件分發給已註冊的處理程序。
    """
    # 獲取LINE的簽章，用於驗證請求的真實性
    signature = request.headers.get("X-Line-Signature", "")
    # 獲取請求的原始內容
    body = await request.body()
    body_text = body.decode()  # WebhookHandler需要字符串主體

    logger.info(f"請求主體: {body_text}")
    logger.info(f"請求簽章: {signature}")

    # 處理webhook主體
    try:
        # WebhookHandler.handle是一個同步方法
        handler.handle(body_text, signature)
    except InvalidSignatureError:
        logger.error("無效簽章。請檢查您的channel access token/channel secret。")
        raise HTTPException(status_code=400, detail="無效簽章")
    except Exception as e:
        logger.error(f"處理webhook時發生錯誤: {e}")
        # 根據錯誤，你可能想要返回500
        raise HTTPException(status_code=500, detail="內部服務器錯誤")

    return 'OK'  # LINE期望快速返回200 OK響應


# --- LINE事件處理程序 ---
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event: MessageEvent):
    """
    處理傳入的文字消息。
    調用OpenAI LLM並回覆生成的回應。
    """
    # 獲取用戶輸入的文本
    user_input = event.message.text
    # 獲取回覆令牌，用於發送回覆消息
    reply_token = event.reply_token
    # 從事件源獲取用戶ID
    user_id = event.source.user_id

    logger.info(f"收到來自用戶 {user_id} 的消息，內容為: {user_input}")

    # 默認錯誤回覆文本
    llm_response_text = "抱歉，處理您的請求時發生錯誤。"

    try:
        # 調用OpenAI LLM
        logger.info(f"為用戶 {user_id} 調用OpenAI")
        # 創建聊天完成請求
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # 選擇您偏好的模型，例如 "gpt-4o", "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "你是一個樂於助人的AI助手，請用繁體中文回覆。每次回覆我時，都是小奶狗狀態！要先說寶寶～～"},  # 系統消息，指導LLM行為
                {"role": "user", "content": user_input},
            ],
            timeout=30.0,  # 為API調用設置超時
        )
        # 從回應中提取LLM生成的回覆文本
        llm_response_text = completion.choices[0].message.content
        logger.info(f"收到來自OpenAI對用戶 {user_id} 的回應: {llm_response_text}")

    except (APIConnectionError, RateLimitError, APIStatusError) as e:
        # 處理OpenAI API特定錯誤
        logger.error(f"用戶 {user_id} 的OpenAI API錯誤: {e}", exc_info=True)
        if isinstance(e, RateLimitError):
            llm_response_text = "目前請求過多，請稍後再試。"
        else:
            llm_response_text = "AI服務暫時無法使用，請稍後再試。"
    except Exception as e:
        # 處理其他未預期的錯誤
        logger.error(f"為用戶 {user_id} 調用OpenAI時發生未預期的錯誤: {e}", exc_info=True)
        llm_response_text = "處理您的請求時發生未知錯誤，請聯繫管理員。"

    # 通過LINE Messaging API回覆用戶
    try:
        logger.info(f"回覆用戶 {user_id} 的消息: {llm_response_text}")
        # 創建回覆請求並發送
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=llm_response_text)]
            )
        )
        logger.info(f"成功回覆用戶 {user_id}。")

    except Exception as e:
        # 處理LINE API回覆錯誤
        logger.error(f"回覆用戶 {user_id} 時發生LINE API錯誤: {e}", exc_info=True)


# 可選：添加其他事件類型的處理程序或默認處理程序
@handler.default()
def default(event):
    """處理未被特定處理程序處理的事件"""
    logger.info(f"收到未處理的事件: {event}")
    # 你可以選擇用默認消息回覆或忽略


# 添加根端點用於健康檢查（可選但推薦用於部署）
@app.get("/")
async def root():
    """基本健康檢查端點"""
    return {"message": "LINE Bot 正在運行。"}

# 關於async/sync：WebhookHandler.handle是同步的。
# 被裝飾的處理函數（@handler.add，@handler.default）也是由handler.handle同步調用的。
# 因此，handle_message中的LINE和OpenAI API調用使用的是它們的同步客戶端。
# 對於非常高的吞吐量，你可能需要探索替代的webhook解析或
# 將API調用分派到後台任務（例如，使用FastAPI的run_in_threadpool或外部隊列）。 