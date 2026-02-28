#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM 调用工具类
使用 OpenAI 兼容的 API（支持 Coze、OpenAI 等）
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any


class LLMClient:
    """大语言模型客户端（OpenAI 兼容）"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "gpt-3.5-turbo"
    ):
        """
        初始化 LLM 客户端

        Args:
            api_key: API Key
            base_url: API 基础 URL
            model: 模型名称
        """
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        self.model = model

        if not self.api_key:
            raise ValueError("LLM_API_KEY 未设置，请配置环境变量或传入 api_key")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_p: float = 1.0
    ) -> Dict[str, Any]:
        """
        调用聊天完成接口

        Args:
            messages: 消息列表，格式 [{"role": "user", "content": "..."}]
            temperature: 温度参数（0-1）
            max_tokens: 最大生成 token 数
            top_p: top-p 采样参数

        Returns:
            API 响应
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=self.headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()
        return response.json()

    def extract_text(self, response: Dict[str, Any]) -> str:
        """
        从 API 响应中提取文本

        Args:
            response: API 响应

        Returns:
            生成的文本
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            return ""
