#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uvicorn

if __name__ == "__main__":
    # 啟動 uvicorn 服務器，用於運行 FastAPI 應用
    uvicorn.run("main:app", 
                host="0.0.0.0",  # 監聽所有網絡接口
                port=8000,       # 在端口 8000 上運行
                reload=True      # 在開發模式中啟用重新加載功能
               ) 