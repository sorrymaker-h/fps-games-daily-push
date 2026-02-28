import os
import json
from typing import Dict, Any, List
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from langchain_core.messages import SystemMessage, HumanMessage
from graphs.state import ExtractTop5Input, ExtractTop5Output


def extract_top5_node(state: ExtractTop5Input, config: RunnableConfig, runtime: Runtime[Context]) -> ExtractTop5Output:
    """
    title: 提取Top5游戏
    desc: 从搜索结果中提取出排名前5的FPS游戏
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
    
    # 渲染用户提示词
    up_tpl = Template(up)
    user_prompt = up_tpl.render({"search_results": state.search_results})
    
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
    
    # 解析 JSON 结果
    try:
        result = json.loads(response_text)
        domestic_top5 = result.get("domestic_top5", [])
        foreign_top5 = result.get("foreign_top5", [])
    except json.JSONDecodeError:
        # 如果解析失败，使用默认值
        domestic_top5 = []
        foreign_top5 = []
    
    return ExtractTop5Output(
        domestic_top5=domestic_top5,
        foreign_top5=foreign_top5
    )
