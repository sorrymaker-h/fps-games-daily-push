from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class GlobalState(BaseModel):
    """全局状态定义"""
    search_results: str = Field(default="", description="热门FPS游戏搜索结果")
    domestic_top3: List[Dict[str, Any]] = Field(default=[], description="国服Top3热门FPS游戏列表")
    foreign_top2: List[Dict[str, Any]] = Field(default=[], description="外服Top2热门FPS游戏列表")
    game_news_list: List[Dict[str, Any]] = Field(default=[], description="每款游戏的资讯列表")
    summarized_news: str = Field(default="", description="汇总后的游戏资讯")
    send_result: str = Field(default="", description="微信发送结果")


class GraphInput(BaseModel):
    """工作流的输入"""
    trigger_type: str = Field(default="scheduled", description="触发类型：scheduled=定时触发, manual=手动触发")


class GraphOutput(BaseModel):
    """工作流的输出"""
    status: str = Field(..., description="执行状态：success/failed")
    message: str = Field(..., description="执行消息")


class SearchGamesInput(BaseModel):
    """搜索热门FPS游戏节点的输入"""
    trigger_type: str = Field(default="scheduled", description="触发类型")


class SearchGamesOutput(BaseModel):
    """搜索热门FPS游戏节点的输出"""
    search_results: str = Field(..., description="热门FPS游戏搜索结果")


class ExtractTop5Input(BaseModel):
    """提取Top5游戏节点的输入"""
    search_results: str = Field(..., description="热门FPS游戏搜索结果")


class ExtractTop5Output(BaseModel):
    """提取Top5游戏节点的输出"""
    domestic_top3: List[Dict[str, Any]] = Field(..., description="国服Top3热门FPS游戏列表，每个元素包含name(游戏名)、description(描述)、heat_score(热度分数)等")
    foreign_top2: List[Dict[str, Any]] = Field(..., description="外服Top2热门FPS游戏列表，每个元素包含name(游戏名)、description(描述)、heat_score(热度分数)等")


class LoopNewsInput(BaseModel):
    """循环搜索游戏资讯子图的输入"""
    games_list: List[Dict[str, Any]] = Field(..., description="游戏列表（包含国服和外服）")


class LoopNewsOutput(BaseModel):
    """循环搜索游戏资讯子图的输出"""
    game_news_list: List[Dict[str, Any]] = Field(..., description="每款游戏的资讯列表")


class SearchGameNewsInput(BaseModel):
    """搜索单个游戏资讯节点的输入"""
    game_name: str = Field(..., description="游戏名称")
    game_description: str = Field(default="", description="游戏描述")


class SearchGameNewsOutput(BaseModel):
    """搜索单个游戏资讯节点的输出"""
    game_name: str = Field(..., description="游戏名称")
    news_search_results: str = Field(..., description="该游戏的资讯搜索结果")


class ExtractNewsInput(BaseModel):
    """提取游戏关键资讯节点的输入"""
    game_name: str = Field(..., description="游戏名称")
    news_search_results: str = Field(..., description="资讯搜索结果")


class ExtractNewsOutput(BaseModel):
    """提取游戏关键资讯节点的输出"""
    game_name: str = Field(..., description="游戏名称")
    extracted_news: str = Field(..., description="提取后的关键资讯")


class SummarizeNewsInput(BaseModel):
    """汇总资讯节点的输入"""
    game_news_list: List[Dict[str, Any]] = Field(..., description="每款游戏的资讯列表")


class SummarizeNewsOutput(BaseModel):
    """汇总资讯节点的输出"""
    summarized_news: str = Field(..., description="汇总后的游戏资讯")


class SendWechatInput(BaseModel):
    """发送微信消息节点的输入"""
    summarized_news: str = Field(..., description="汇总后的游戏资讯")


class SendWechatOutput(BaseModel):
    """发送微信消息节点的输出"""
    send_result: str = Field(..., description="微信发送结果")
    status: str = Field(default="success", description="执行状态：success/failed")
    message: str = Field(default="", description="执行消息")


class LoopNewsNodeInput(BaseModel):
    """循环搜索资讯节点的输入"""
    games_list: List[Dict[str, Any]] = Field(..., description="游戏列表（包含国服和外服共10个游戏）")


class LoopNewsNodeOutput(BaseModel):
    """循环搜索资讯节点的输出"""
    game_news_list: List[Dict[str, Any]] = Field(..., description="每款游戏的资讯列表")


class PrepareLoopInput(BaseModel):
    """准备循环节点的输入"""
    domestic_top5: List[Dict[str, Any]] = Field(..., description="国服Top5游戏列表")
    foreign_top5: List[Dict[str, Any]] = Field(..., description="外服Top5游戏列表")


class PrepareLoopOutput(BaseModel):
    """准备循环节点的输出"""
    games_list: List[Dict[str, Any]] = Field(..., description="合并后的游戏列表（共10个）")

