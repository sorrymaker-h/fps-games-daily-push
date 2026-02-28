#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coze API 客户端
用于替代 coze-coding-dev-sdk，直接调用 Coze API
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any


class CozeAPIClient:
    """Coze API 客户端"""

    # Coze API 基础 URL
    BASE_URL = "https://api.coze.cn"
    SEARCH_API_URL = f"{BASE_URL}/v3/search"
    CHAT_API_URL = f"{BASE_URL}/v3/chat"
    MESSAGE_API_URL = f"{BASE_URL}/v3/chat/message"

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 Coze API 客户端

        Args:
            api_key: Coze API Key，如果为 None 则从环境变量读取
        """
        self.api_key = api_key or os.getenv("COZE_API_KEY")
        if not self.api_key:
            raise ValueError("COZE_API_KEY 未设置，请配置环境变量或传入 api_key")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def web_search(
        self,
        query: str,
        top_k: int = 5,
        search_service: str = "web_search"
    ) -> Dict[str, Any]:
        """
        网络搜索

        Args:
            query: 搜索查询
            top_k: 返回结果数量
            search_service: 搜索服务类型

        Returns:
            搜索结果
        """
        payload = {
            "query": query,
            "search_service": search_service,
            "top_k": top_k
        }

        response = requests.post(
            self.SEARCH_API_URL,
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()

    def create_chat(
        self,
        bot_id: str,
        user_id: str,
        query: str,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        创建聊天对话

        Args:
            bot_id: Bot ID
            user_id: 用户 ID
            query: 用户输入
            stream: 是否流式返回

        Returns:
            聊天响应
        """
        payload = {
            "bot_id": bot_id,
            "user_id": user_id,
            "query": query,
            "stream": stream
        }

        response = requests.post(
            self.CHAT_API_URL,
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()

    def send_message(
        self,
        conversation_id: str,
        bot_id: str,
        user_id: str,
        query: str
    ) -> Dict[str, Any]:
        """
        发送消息到现有对话

        Args:
            conversation_id: 对话 ID
            bot_id: Bot ID
            user_id: 用户 ID
            query: 用户输入

        Returns:
            消息响应
        """
        payload = {
            "conversation_id": conversation_id,
            "bot_id": bot_id,
            "user_id": user_id,
            "query": query,
            "stream": False
        }

        response = requests.post(
            self.MESSAGE_API_URL,
            headers=self.headers,
            json=payload
        )

        response.raise_for_status()
        return response.json()

    def call_llm(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        调用大语言模型

        Args:
            model: 模型 ID
            messages: 消息列表
            temperature: 温度参数
            max_tokens: 最大生成 token 数

        Returns:
            LLM 响应
        """
        # Coze API 不直接支持 LLM 调用，需要通过 Bot 来实现
        # 这里我们提供一个简化的接口，实际需要使用 Bot ID
        raise NotImplementedError(
            "Coze API 不直接支持 LLM 调用，请使用 create_chat 或 send_message"
        )


class CozeAPIClientWithBot(CozeAPIClient):
    """使用 Bot 的 Coze API 客户端"""

    def __init__(self, api_key: str, bot_id: str):
        """
        初始化 Coze API 客户端（带 Bot ID）

        Args:
            api_key: Coze API Key
            bot_id: Bot ID
        """
        super().__init__(api_key)
        self.bot_id = bot_id

    def chat(
        self,
        user_id: str,
        query: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        与 Bot 对话

        Args:
            user_id: 用户 ID
            query: 用户输入
            conversation_id: 对话 ID（可选，用于继续对话）

        Returns:
            对话响应
        """
        if conversation_id:
            return self.send_message(conversation_id, self.bot_id, user_id, query)
        else:
            response = self.create_chat(self.bot_id, user_id, query)
            return response
