#!/usr/bin/env python3
"""测试 DeepSeek API 连接"""

import os
import sys
import requests

# 设置 API Key
os.environ["LLM_API_KEY"] = "sk-51c19c924e9c489a9acbf135ba44d47d"

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from utils.llm_client import LLMClient

def test_deepseek_api():
    """测试 DeepSeek API"""
    print("🧪 开始测试 DeepSeek API...")

    try:
        # 创建客户端
        client = LLMClient(model="deepseek-chat")
        print(f"✅ 客户端创建成功，模型: {client.model}")

        # 发送测试消息
        messages = [
            {"role": "system", "content": "你是一个有用的助手。"},
            {"role": "user", "content": "请用一句话介绍你自己。"}
        ]

        print("📤 发送测试消息...")
        response = client.chat_completion(
            messages=messages,
            temperature=0.7,
            max_tokens=200
        )

        # 提取响应文本
        text = client.extract_text(response)
        print(f"📥 收到响应:")
        print("-" * 50)
        print(text)
        print("-" * 50)
        print("✅ DeepSeek API 测试成功！")

        return True

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP 错误: {e}")
        if e.response is not None:
            print(f"状态码: {e.response.status_code}")
            print(f"响应内容: {e.response.text}")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_deepseek_api()
    sys.exit(0 if success else 1)
