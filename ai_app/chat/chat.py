# -*- coding: utf-8 -*-
"""
Created on 2025/8/6 16:15

@Project -> File: PythonProject -> chat.py

@Author: ouzhihui

@Describe: 
"""
from ai_app.service.call_llm import lang_call_llm

system_content = "You are a helpful assistant."
model = 'deepseek-v3'
api_key = 'sk-c6163e4f30ab457db6fae9678430c451'
base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'

async def get_ai_response(user_message: str):
    user_content = user_message
    async for chunk in lang_call_llm(system_content, user_content, model, api_key, base_url):
        yield chunk

