from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput,
    LoopNewsNodeInput,
    LoopNewsNodeOutput
)
from graphs.nodes.search_fps_games_node import search_fps_games_node
from graphs.nodes.extract_top5_node import extract_top5_node
from graphs.nodes.summarize_news_node import summarize_news_node
from graphs.nodes.send_wechat_node import send_wechat_node


# 调用子图的节点
def loop_news_node(state: LoopNewsNodeInput, config: RunnableConfig, runtime: Runtime[Context]) -> LoopNewsNodeOutput:
    """
    title: 循环搜索游戏资讯
    desc: 循环搜索Top5游戏的资讯
    """
    ctx = runtime.context
    
    # 动态导入子图
    from graphs.loop_graph import LoopGraphInput, subgraph
    
    # 调用子图
    input_state = LoopGraphInput(top5_games=state.top5_games)
    output = subgraph.invoke(input_state)
    
    # 处理输出，可能是 Pydantic 模型或 dict
    if isinstance(output, dict):
        game_news_list = output.get("game_news_list", [])
    else:
        game_news_list = output.game_news_list if hasattr(output, 'game_news_list') else []
    
    return LoopNewsNodeOutput(game_news_list=game_news_list)


# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("search_games", search_fps_games_node)
builder.add_node("extract_top5", extract_top5_node, metadata={"type": "agent", "llm_cfg": "config/extract_top5_llm_cfg.json"})
builder.add_node("loop_news", loop_news_node, metadata={"type": "looparray"})
builder.add_node("summarize_news", summarize_news_node, metadata={"type": "agent", "llm_cfg": "config/summarize_news_llm_cfg.json"})
builder.add_node("send_wechat", send_wechat_node)

# 设置入口点
builder.set_entry_point("search_games")

# 添加边
builder.add_edge("search_games", "extract_top5")
builder.add_edge("extract_top5", "loop_news")
builder.add_edge("loop_news", "summarize_news")
builder.add_edge("summarize_news", "send_wechat")
builder.add_edge("send_wechat", END)

# 编译图
main_graph = builder.compile()
