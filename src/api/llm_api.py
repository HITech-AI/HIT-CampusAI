# src/api/llm_api.py
import os
import requests
from dotenv import load_dotenv

# 加载环境变量（将API密钥存放在项目根目录的 .env 文件中）
load_dotenv()
API_KEY = os.getenv("HIT_AI_API_KEY")
API_URL = os.getenv("HIT_AI_API_URL")

def hit_llm_inference(prompt: str) -> str:
    """
    调用哈工大AI平台大模型进行推理
    :param prompt: 输入给模型的提示词
    :return: 模型的回复文本
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json().get("response", "抱歉，我暂时无法回答这个问题。")
    else:
        return f"调用大模型失败，错误码：{response.status_code}"