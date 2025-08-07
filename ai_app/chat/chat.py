# -*- coding: utf-8 -*-
"""
Created on 2025/8/6 16:15

@Project -> File: PythonProject -> chat.py

@Author: ouzhihui

@Describe: 
"""
from ai_app.cfg.settings import model, api_key, base_url
from ai_app.service.call_llm import lang_call_llm_stream

system_content = "You are a helpful assistant."


async def get_ai_response(user_message: str):

    user_content = user_message
    async for chunk in lang_call_llm_stream(system_content, user_content, model, api_key, base_url):
        if chunk is not None:
            yield chunk

