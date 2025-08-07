# -*- coding: utf-8 -*-
"""
Created on 2025/8/6 14:49

@Project -> File: PythonProject -> call_llm.py

@Author: ouzhihui

@Describe: 
"""
import asyncio
import sys
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


async def lang_call_llm_stream(system_content, user_content, model, api_key, base_url):

    llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)
    # 构建对话链
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

    async for chunk in llm.astream(messages):
        if chunk.content is not None:
            yield chunk.content

async def lang_call_llm(system_content, user_content, model, api_key, base_url):

    llm = ChatOpenAI(model=model, api_key=api_key, base_url=base_url)
    # 构建对话链
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

    response = await llm.ainvoke(messages)

    return response.content


if __name__ == '__main__':
    from ai_app.cfg.settings import api_key

    system_content = "You are a helpful assistant."
    user_content = "你是谁？"
    model = 'deepseek-v3'

    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    response =asyncio.run(lang_call_llm(system_content, user_content, model, api_key, base_url))
    print(response)

