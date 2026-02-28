import os
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from utils.search_tool import web_search
from graphs.state import SearchGameNewsInput, SearchGameNewsOutput


def search_game_news_node(state: SearchGameNewsInput, config: RunnableConfig, runtime: Runtime[Context]) -> SearchGameNewsOutput:
    """
    title: 搜索游戏资讯
    desc: 搜索单个FPS游戏的最新资讯，包括活动、更新、赛事等
    integrations: duckduckgo-search
    """
    ctx = runtime.context

    # 获取当前日期
    current_date = datetime.now().strftime("%Y年%m月%d日")

    # 构建搜索查询（明确指定今日日期）
    query = f"{state.game_name} {current_date} 今日资讯 更新 活动 赛事 新闻"
    response = web_search(
        query=query,
        max_results=5,
        need_summary=True
    )

    # 整理搜索结果
    search_results_text = ""
    if response.get("web_items"):
        search_results_text += f"关于《{state.game_name}》在{current_date}的资讯:\n\n"
        for i, item in enumerate(response["web_items"], 1):
            search_results_text += f"{i}. {item['title']}\n"
            search_results_text += f"   来源: {item['site_name']}\n"
            search_results_text += f"   URL: {item['url']}\n"
            if item.get("snippet"):
                search_results_text += f"   摘要: {item['snippet']}\n"
            search_results_text += "\n"
    else:
        search_results_text = f"未搜索到《{state.game_name}》在{current_date}的相关资讯"

    return SearchGameNewsOutput(
        game_name=state.game_name,
        news_search_results=search_results_text
    )
