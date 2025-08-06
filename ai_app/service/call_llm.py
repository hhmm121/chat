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

sys.path.append('../../')

# -*- coding: utf-8 -*-
"""
Created on 2025/7/23 9:37

@Project -> File: valuescan-extract-social-media-information-online -> call_llm.py

@Author: ouzhihui

@Describe: 
"""
import sys

from openai import OpenAI, AsyncOpenAI
from langchain_openai import ChatOpenAI


sys.path.append('../../')

def format_tokens_auto(tokens):
    if tokens < 1000:
        return str(tokens)
    elif tokens < 1_000_000:
        k_tokens = tokens / 1000
        # 如果小数部分为 0，则省略（如 "2K" 而不是 "2.0K"）
        return f"{int(k_tokens)}K" if k_tokens.is_integer() else f"{k_tokens:.1f}K"
    else:
        m_tokens = tokens / 1_000_000
        return f"{m_tokens:.1f}M"  # 百万级单位

def call_llm(system_content, user_content, model, api_key, base_url, _logger):
    """
    调用大模型
    :param system_content: 角色定义，确定任务
    :param api_model: 调用的模型名称
    :param api_key: 访问密钥
    :param base_url: 访问路径
    :return: 最终生成的结果
    """
    _logger.info(f'==> 开始调用大模型')
    client = OpenAI(api_key=api_key, base_url=base_url)
    messages = [
        {"role": "system", "content": f"{system_content}"},
        {"role": "user", "content": f"{user_content}"},
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        temperature=0.5
    )
    response_content = response.choices[0].message.content

    return response_content


async def async_call_llm(system_content, user_content, model, api_key, base_url, _logger):
    _logger.info(f'==> 异步调用大模型开始')

    client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    messages = [
        {"role": "system", "content": f"{system_content}"},
        {"role": "user", "content": f"{user_content}"},
    ]
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
        temperature=0.5
    )
    response_content = response.choices[0].message.content

    return response_content


async def lang_call_llm(system_content, user_content, model, api_key, base_url):
    llm = ChatOpenAI(model=model, api_key= api_key, base_url=base_url)
    # 构建对话链
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}]

    # 执行调用
    # response = await llm.ainvoke(messages)
    async for chunk in llm.astream(messages):
        if chunk.content is not None:  # 确保内容不为空
            yield chunk.content
    # response_content = response.content
    # return response_content


if __name__ == '__main__':
    system_content = "You are a helpful assistant."
    user_content = "你是谁？"
    model = 'deepseek-v3'

    base_url = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    response =asyncio.run(lang_call_llm(system_content, user_content, model, api_key, base_url))
    print(response)

