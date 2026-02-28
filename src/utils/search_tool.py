#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
搜索工具类
使用 DuckDuckGo 进行网络搜索（无需 API Key）
"""

from typing import List, Dict, Optional
from duckduckgo_search import DDGS


def web_search(
    query: str,
    max_results: int = 10,
    need_summary: bool = False
) -> Dict[str, any]:
    """
    网络搜索（使用 DuckDuckGo）

    Args:
        query: 搜索查询
        max_results: 最大结果数量
        need_summary: 是否需要 AI 摘要（暂不支持）

    Returns:
        搜索结果，格式：
        {
            "web_items": [
                {
                    "title": "标题",
                    "url": "链接",
                    "snippet": "摘要",
                    "site_name": "网站名称"
                },
                ...
            ]
        }
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=max_results))

        web_items = []
        for result in results:
            item = {
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", ""),
                "site_name": _extract_site_name(result.get("href", ""))
            }
            web_items.append(item)

        return {
            "web_items": web_items
        }

    except Exception as e:
        # 如果搜索失败，返回空结果
        print(f"搜索失败: {e}")
        return {
            "web_items": []
        }


def _extract_site_name(url: str) -> str:
    """
    从 URL 中提取网站名称

    Args:
        url: URL

    Returns:
        网站名称
    """
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc
    except:
        return "未知来源"
