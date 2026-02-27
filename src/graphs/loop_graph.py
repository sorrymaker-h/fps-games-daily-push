from typing import List, Dict, Any
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import LoopNewsInput, LoopNewsOutput
from graphs.nodes.search_game_news_node import search_game_news_node
from graphs.nodes.extract_news_node import extract_news_node


# 子图的全局状态
class LoopGlobalState(BaseModel):
    """循环资讯子图的全局状态"""
    top5_games: List[Dict[str, Any]] = Field(default=[], description="Top5热门FPS游戏列表")
    current_index: int = Field(default=0, description="当前处理的游戏索引")
    game_name: str = Field(default="", description="当前游戏名称")
    game_description: str = Field(default="", description="当前游戏描述")
    news_search_results: str = Field(default="", description="当前游戏资讯搜索结果")
    game_news_list: List[Dict[str, Any]] = Field(default=[], description="已处理的游戏资讯列表")


# 子图的输入输出
class LoopGraphInput(BaseModel):
    """子图输入"""
    top5_games: List[Dict[str, Any]] = Field(..., description="Top5热门FPS游戏列表")


class LoopGraphOutput(BaseModel):
    """子图输出"""
    game_news_list: List[Dict[str, Any]] = Field(..., description="每款游戏的资讯列表")


# 准备当前游戏信息的节点
def prepare_current_game_node(state: LoopGlobalState, config: RunnableConfig, runtime: Runtime[Context]) -> Dict[str, Any]:
    """
    title: 准备当前游戏
    desc: 从列表中获取当前需要处理的游戏信息
    """
    ctx = runtime.context
    
    if state.current_index < len(state.top5_games):
        current_game = state.top5_games[state.current_index]
        game_name = current_game.get("name", "")
        game_description = current_game.get("description", "")
        
        return {
            "game_name": game_name,
            "game_description": game_description
        }
    else:
        return {
            "game_name": "",
            "game_description": ""
        }


# 搜索单个游戏资讯（节点2）
def search_news_in_loop_node(state: LoopGlobalState, config: RunnableConfig, runtime: Runtime[Context]) -> Dict[str, Any]:
    """
    title: 搜索游戏资讯
    desc: 搜索当前游戏的资讯
    """
    ctx = runtime.context
    
    # 调用节点函数
    from graphs.nodes.search_game_news_node import SearchGameNewsInput, SearchGameNewsOutput
    
    input_state = SearchGameNewsInput(
        game_name=state.game_name,
        game_description=state.game_description
    )
    
    output_state = search_game_news_node(input_state, config, runtime)
    
    return {
        "news_search_results": output_state.news_search_results
    }


# 提取关键资讯（节点3）
def extract_news_in_loop_node(state: LoopGlobalState, config: RunnableConfig, runtime: Runtime[Context]) -> Dict[str, Any]:
    """
    title: 提取关键资讯
    desc: 从搜索结果中提取关键资讯
    """
    ctx = runtime.context
    
    # 调用节点函数
    from graphs.nodes.extract_news_node import ExtractNewsInput, ExtractNewsOutput
    
    input_state = ExtractNewsInput(
        game_name=state.game_name,
        news_search_results=state.news_search_results
    )
    
    output_state = extract_news_node(input_state, config, runtime)
    
    # 将提取的资讯添加到列表
    news_list = state.game_news_list.copy()
    news_list.append({
        "game_name": output_state.game_name,
        "extracted_news": output_state.extracted_news
    })
    
    # 增加索引
    next_index = state.current_index + 1
    
    return {
        "game_news_list": news_list,
        "current_index": next_index
    }


# 条件判断：是否还有游戏需要处理
def has_more_games(state: LoopGlobalState) -> str:
    """
    title: 判断是否还有游戏
    desc: 判断是否还有游戏需要处理
    """
    if state.current_index < len(state.top5_games):
        return "继续处理"
    else:
        return "结束循环"


# 构建子图
def build_loop_graph():
    """构建循环资讯子图"""
    
    # 创建状态图
    builder = StateGraph(
        LoopGlobalState,
        input_schema=LoopGraphInput,
        output_schema=LoopGraphOutput
    )
    
    # 添加节点
    builder.add_node("prepare_game", prepare_current_game_node)
    builder.add_node("search_news", search_news_in_loop_node)
    builder.add_node("extract_news", extract_news_in_loop_node, metadata={"type": "agent", "llm_cfg": "config/extract_news_llm_cfg.json"})
    
    # 设置入口点
    builder.set_entry_point("prepare_game")
    
    # 添加边
    builder.add_edge("prepare_game", "search_news")
    builder.add_edge("search_news", "extract_news")
    
    # 添加条件分支
    builder.add_conditional_edges(
        source="extract_news",
        path=has_more_games,
        path_map={
            "继续处理": "prepare_game",
            "结束循环": END
        }
    )
    
    # 编译子图
    return builder.compile()


# 创建子图实例
subgraph = build_loop_graph()
