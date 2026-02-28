import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
from graphs.state import ExtractNewsInput, ExtractNewsOutput


def extract_news_node(state: ExtractNewsInput, config: RunnableConfig, runtime: Runtime[Context]) -> ExtractNewsOutput:
    """
    title: 提取资讯
    desc: 从搜索结果中提取出当日相关资讯
    integrations: 大语言模型
    """
    ctx = runtime.context

    # 读取配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r', encoding='utf-8') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    # 创建 LLM 客户端
    client = LLMClient(ctx=ctx)

    # 获取当前日期
    current_date = datetime.now().strftime("%Y年%m月%d日")

    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt = up_tpl.render({
        "current_date": current_date,
        "game_name": state.game_name,
        "news_search_results": state.news_search_results
    })

    # 构建消息
    messages = [
        SystemMessage(content=sp),
        HumanMessage(content=user_prompt)
    ]

    # 调用大模型
    response = client.invoke(
        messages=messages,
        model=llm_config.get("model", "doubao-seed-1-8-251228"),
        temperature=llm_config.get("temperature", 0.7),
        max_completion_tokens=llm_config.get("max_completion_tokens", 2000)
    )

    # 获取响应文本
    response_text = response.content
    if isinstance(response_text, list):
        response_text = str(response_text)

    return ExtractNewsOutput(
        game_name=state.game_name,
        extracted_news=response_text
    )
