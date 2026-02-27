#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度脚本
每天早上10点自动执行FPS游戏榜单推送任务
"""

import schedule
import time
import logging
import sys
from datetime import datetime

# 添加项目根目录到 Python 路径
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graphs.graph import main_graph
from graphs.state import GraphInput

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_fps_games_workflow():
    """
    执行FPS游戏榜单推送工作流
    """
    try:
        logger.info("=" * 60)
        logger.info("开始执行FPS游戏榜单推送任务")
        logger.info(f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 60)
        
        # 准备输入
        workflow_input = GraphInput(trigger_type="scheduled")
        
        # 执行工作流
        result = main_graph.invoke(workflow_input)
        
        # 输出结果
        logger.info("=" * 60)
        logger.info("工作流执行完成")
        logger.info(f"状态: {result.status}")
        logger.info(f"消息: {result.message}")
        logger.info("=" * 60)
        
        if result.status == "success":
            logger.info("✅ FPS游戏榜单推送任务执行成功")
        else:
            logger.error(f"❌ FPS游戏榜单推送任务执行失败: {result.message}")
            
    except Exception as e:
        logger.error(f"执行工作流时发生异常: {str(e)}", exc_info=True)


def schedule_job():
    """
    定时任务调度
    """
    # 每天早上10点执行
    schedule.every().day.at("10:00").do(run_fps_games_workflow)
    
    logger.info("定时任务已启动")
    logger.info("下次执行时间: " + str(schedule.next_run()))
    logger.info("等待执行中...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


def manual_run():
    """
    手动执行（用于测试）
    """
    logger.info("手动执行模式")
    run_fps_games_workflow()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="FPS游戏榜单推送定时任务")
    parser.add_argument(
        "--manual",
        action="store_true",
        help="手动执行一次任务（用于测试）"
    )
    
    args = parser.parse_args()
    
    if args.manual:
        # 手动执行模式
        manual_run()
    else:
        # 定时执行模式
        schedule_job()
