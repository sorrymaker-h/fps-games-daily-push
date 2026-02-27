import os
import json
import requests
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import SendWechatInput, SendWechatOutput


def get_dingtalk_webhook():
    """获取钉钉机器人webhook URL"""
    # 优先从环境变量读取
    webhook_url = os.getenv("DINGTALK_WEBHOOK_URL")
    if webhook_url:
        return webhook_url
    
    # 如果环境变量没有，使用默认配置
    default_url = "https://oapi.dingtalk.com/robot/send?access_token=5f30c823eb6bf1a6c16fae13f002d068b6b39bc7857e6eb651f3bfc56e8a85f3"
    return default_url


def send_dingtalk_message(message: str) -> dict:
    """
    发送钉钉文本消息
    
    :param message: 消息内容
    :return: 发送结果
    """
    webhook_url = get_dingtalk_webhook()
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    
    response = requests.post(webhook_url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    if data.get("errcode", 0) != 0:
        raise Exception(f"发送失败: {data}")
    
    return data


def send_dingtalk_node(state: SendWechatInput, config: RunnableConfig, runtime: Runtime[Context]) -> SendWechatOutput:
    """
    title: 发送钉钉消息
    desc: 将汇总后的资讯通过钉钉机器人发送到指定群组
    """
    ctx = runtime.context
    
    try:
        # 发送钉钉消息
        result = send_dingtalk_message(state.summarized_news)
        
        return SendWechatOutput(
            send_result=f"发送成功: {result}",
            status="success",
            message="FPS游戏榜单推送成功（钉钉）"
        )
    except Exception as e:
        return SendWechatOutput(
            send_result=f"发送失败: {str(e)}",
            status="failed",
            message=f"FPS游戏榜单推送失败（钉钉）: {str(e)}"
        )
