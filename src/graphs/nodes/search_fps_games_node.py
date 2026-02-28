import os
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from graphs.state import SearchGamesInput, SearchGamesOutput


def search_fps_games_node(state: SearchGamesInput, config: RunnableConfig, runtime: Runtime[Context]) -> SearchGamesOutput:
    """
    title: 搜索热门FPS游戏
    desc: 使用网络搜索功能搜索全网热门的FPS游戏
    integrations: web-search
    """
    ctx = runtime.context

    # 创建搜索客户端
    search_ctx = new_context(method="search_fps_games")
    client = SearchClient(ctx=search_ctx)

    # 搜索热门FPS游戏（仅限PC端）
    query = "热门PC端FPS游戏排行 2024 2025 电脑射击游戏 Steam平台"
    response = client.web_search(
        query=query,
        count=10,
        need_summary=True
    )

    # 整理搜索结果
    search_results_text = ""
    if response.web_items:
        search_results_text += f"搜索到 {len(response.web_items)} 个结果:\n\n"
        for i, item in enumerate(response.web_items, 1):
            search_results_text += f"{i}. {item.title}\n"
            search_results_text += f"   来源: {item.site_name}\n"
            search_results_text += f"   URL: {item.url}\n"
            if item.snippet:
                search_results_text += f"   摘要: {item.snippet}\n"
            if item.summary:
                search_results_text += f"   AI摘要: {item.summary}\n"
            search_results_text += "\n"
    else:
        search_results_text = "未搜索到相关结果"

    return SearchGamesOutput(search_results=search_results_text)
