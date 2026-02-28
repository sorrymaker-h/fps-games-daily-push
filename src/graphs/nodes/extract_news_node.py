import os
import json
from typing import Dict, Any
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from utils.llm_client import LLMClient as DeepSeekLLMClient
from graphs.state import ExtractNewsInput, ExtractNewsOutput


def extract_news_node(state: ExtractNewsInput, config: RunnableConfig, runtime: Runtime[Context]) -> ExtractNewsOutput:
    """
    title: 提取关键资讯
    desc: 从搜索结果中提取游戏的关键资讯，包括活动、更新、赛事等
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

    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt = up_tpl.render({
        "game_name": state.game_name,
        "news_search_results": state.news_search_results
    })

    # 构建消息
    messages = [
        {"role": "system", "content": sp},
        {"role": "user", "content": user_prompt}
    ]

    # 调用大模型
    response = client.chat_completion(
        messages=messages,
        temperature=llm_config.get("temperature", 0.3),
        max_tokens=llm_config.get("max_completion_tokens", 2000)
    )

    # 获取响应文本
    response_text = client.extract_text(response)

    return ExtractNewsOutput(
        game_name=state.game_name,
        extracted_news=response_text
    )
