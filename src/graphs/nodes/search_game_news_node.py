import os
from datetime import datetime
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from graphs.state import SearchGameNewsInput, SearchGameNewsOutput


def search_game_news_node(state: SearchGameNewsInput, config: RunnableConfig, runtime: Runtime[Context]) -> SearchGameNewsOutput:
    """
    title: 搜索游戏资讯
    desc: 搜索单个FPS游戏的最新资讯，包括活动、更新、赛事等
    integrations: web-search
    """
    ctx = runtime.context

    # 获取当前日期
    current_date = datetime.now().strftime("%Y年%m月%d日")
    current_year = datetime.now().strftime("%Y")
    current_month = datetime.now().strftime("%m")

    # 创建搜索客户端
    search_ctx = new_context(method="search_game_news")
    client = SearchClient(ctx=search_ctx)

    # 构建搜索查询，明确指定当前年月，优先搜索最新资讯
    query = f"{state.game_name} {current_year}年{current_month} 更新 活动 赛事 新闻 Steam"
    response = client.web_search(
        query=query,
        count=5,
        need_summary=True
    )

    # 整理搜索结果
    search_results_text = ""
    if response.web_items:
        search_results_text += f"关于《{state.game_name}》的资讯（优先展示{current_year}年{current_month}的内容）:\n\n"
        for i, item in enumerate(response.web_items, 1):
            search_results_text += f"{i}. {item.title}\n"
            search_results_text += f"   来源: {item.site_name}\n"
            search_results_text += f"   URL: {item.url}\n"
            # 必须包含时间信息
            if item.publish_time:
                search_results_text += f"   发布时间: {item.publish_time}\n"
            else:
                search_results_text += f"   发布时间: 未标注\n"
            if item.snippet:
                search_results_text += f"   摘要: {item.snippet}\n"
            if item.summary:
                search_results_text += f"   AI摘要: {item.summary}\n"
            search_results_text += "\n"
    else:
        search_results_text = f"未搜索到《{state.game_name}》的相关资讯"

    return SearchGameNewsOutput(
        game_name=state.game_name,
        news_search_results=search_results_text
    )
