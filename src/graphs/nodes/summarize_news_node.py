import os
import json
from typing import Dict, Any
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from utils.llm_client import LLMClient as DeepSeekLLMClient
from datetime import datetime
from graphs.state import SummarizeNewsInput, SummarizeNewsOutput


def summarize_news_node(state: SummarizeNewsInput, config: RunnableConfig, runtime: Runtime[Context]) -> SummarizeNewsOutput:
    """
    title: 汇总资讯
    desc: 将所有游戏的资讯汇总成一份完整的报告
    integrations: deepseek-llm
    """
    ctx = runtime.context

    # 读取配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    # 创建 DeepSeek LLM 客户端
    client = DeepSeekLLMClient(
        api_key=os.getenv("LLM_API_KEY"),
        model="deepseek-chat"
    )

    # 准备游戏资讯列表文本
    news_list_text = ""
    for idx, game_news in enumerate(state.game_news_list, 1):
        game_name = game_news.get("game_name", "未知游戏")
        extracted_news = game_news.get("extracted_news", "暂无资讯")
        news_list_text += f"\n\n### 第{idx}款游戏：{game_name}\n{extracted_news}"

    # 获取当前日期
    current_date = datetime.now().strftime("%Y年%m月%d日")

    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt = up_tpl.render({
        "current_date": current_date,
        "news_list": news_list_text
    })

    # 构建消息
    messages = [
        {"role": "system", "content": sp},
        {"role": "user", "content": user_prompt}
    ]

    # 调用大模型
    response = client.chat_completion(
        messages=messages,
        temperature=llm_config.get("temperature", 0.7),
        max_tokens=llm_config.get("max_completion_tokens", 4000)
    )

    # 获取响应文本
    response_text = client.extract_text(response)

    return SummarizeNewsOutput(summarized_news=response_text)
