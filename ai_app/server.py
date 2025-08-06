# -*- coding: utf-8 -*-
"""
Created on 2025/8/6 15:22

@Project -> File: PythonProject -> server.py

@Author: ouzhihui

@Describe: 
"""
from fastapi import FastAPI
from pydantic import BaseModel
import random
import time

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from ai_app.chat.chat import get_ai_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者指定你的前端地址，如 "http://localhost:3000"
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法，包括 OPTIONS
    allow_headers=["*"],
    expose_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # ai_reply = await get_ai_response(request.message)
    # return ChatResponse(reply=ai_reply)
    reply = get_ai_response(request.message)
    return StreamingResponse(
        reply,
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # 禁用Nginx缓冲
        }
    )


@app.get("/")
async def root():
    return {"status": "running", "message": "Chat API is ready"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run('server:app', host="192.168.51.2", port=8002)