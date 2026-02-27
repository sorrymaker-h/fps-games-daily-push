import os
import json
import re
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_workload_identity import Client
from cozeloop.decorator import observe
from graphs.state import SendWechatInput, SendWechatOutput


def get_webhook_key():
    """获取微信机器人webhook key"""
    client = Client()
    wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
    webhook_key = json.loads(wechat_bot_credential)["webhook_key"]
    if "https" in webhook_key:
        webhook_key = re.search(r"key=([a-zA-Z0-9-]+)", webhook_key).group(1)
    return webhook_key


@observe
def send_wechat_message(message: str) -> dict:
    """
    发送微信文本消息
    
    :param message: 消息内容
    :return: 发送结果
    """
    webhook_key = get_webhook_key()
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    headers = {"Content-Type": "application/json"}
    
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    
    import requests
    response = requests.post(url, json=payload, headers=headers, timeout=15)
    response.raise_for_status()
    data = response.json()
    
    if data.get("errcode", 0) != 0:
        raise Exception(f"发送失败: {data}")
    
    return data


def send_wechat_node(state: SendWechatInput, config: RunnableConfig, runtime: Runtime[Context]) -> SendWechatOutput:
    """
    title: 发送微信消息
    desc: 将汇总后的资讯通过微信机器人发送到指定群组
    integrations: wechat-bot
    """
    ctx = runtime.context
    
    try:
        # 发送微信消息
        result = send_wechat_message(state.summarized_news)
        
        return SendWechatOutput(
            send_result=f"发送成功: {result}",
            status="success",
            message="FPS游戏榜单推送成功"
        )
    except Exception as e:
        return SendWechatOutput(
            send_result=f"发送失败: {str(e)}",
            status="failed",
            message=f"FPS游戏榜单推送失败: {str(e)}"
        )
