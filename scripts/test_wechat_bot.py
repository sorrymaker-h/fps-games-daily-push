#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信机器人测试脚本
用于验证webhook配置是否正确
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_wechat_bot():
    """测试微信机器人配置"""
    
    print("=" * 60)
    print("微信机器人配置测试")
    print("=" * 60)
    
    # 读取webhook key
    webhook_key = os.getenv("WECHAT_BOT_WEBHOOK_KEY")
    
    if not webhook_key:
        print("\n❌ 错误：未找到 WECHAT_BOT_WEBHOOK_KEY 环境变量")
        print("\n请按照以下步骤配置：")
        print("1. 在企业微信群中添加机器人")
        print("2. 获取 webhook URL")
        print("3. 提取 key 参数")
        print("4. 设置环境变量：export WECHAT_BOT_WEBHOOK_KEY=你的key")
        print("\n或者参考 WECHAT_BOT_SETUP.md 文件")
        return False
    
    print(f"\n✅ Webhook Key: {webhook_key}")
    
    # 构造测试消息
    url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    test_message = f"""
🤖 微信机器人测试消息

如果你看到这条消息，说明webhook配置成功！

测试时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
配置文件: {os.path.abspath(__file__)}

现在可以使用FPS游戏榜单推送工作流了！🎮
    """.strip()
    
    payload = {
        "msgtype": "text",
        "text": {
            "content": test_message
        }
    }
    
    print(f"\n📤 发送测试消息到: {url}")
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n📥 响应状态: {response.status_code}")
        print(f"📥 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("errcode") == 0:
            print("\n" + "=" * 60)
            print("✅ 测试成功！微信机器人配置正确！")
            print("=" * 60)
            return True
        else:
            print("\n" + "=" * 60)
            print("❌ 测试失败！请检查配置")
            print("=" * 60)
            print(f"错误码: {result.get('errcode')}")
            print(f"错误信息: {result.get('errmsg')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ 网络请求失败: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        return False


def test_workflow_integration():
    """测试工作流集成"""
    print("\n\n" + "=" * 60)
    print("工作流集成测试")
    print("=" * 60)
    
    webhook_key = os.getenv("WECHAT_BOT_WEBHOOK_KEY")
    
    if not webhook_key:
        print("\n❌ 跳过工作流集成测试（webhook未配置）")
        return
    
    print("\n尝试导入工作流...")
    try:
        from graphs.graph import main_graph
        print("✅ 工作流导入成功")
    except Exception as e:
        print(f"❌ 工作流导入失败: {e}")
        return
    
    print("\n工作流集成测试完成！")
    print("可以使用以下命令运行工作流：")
    print("  python scripts/schedule_fps_games.py --manual")


def main():
    """主函数"""
    # 加载.env文件（如果存在）
    load_dotenv()
    
    # 测试微信机器人
    bot_test_passed = test_wechat_bot()
    
    # 测试工作流集成
    test_workflow_integration()
    
    print("\n" + "=" * 60)
    if bot_test_passed:
        print("🎉 配置测试通过！可以开始使用工作流了！")
        print("\n运行命令：")
        print("  python scripts/schedule_fps_games.py --manual")
    else:
        print("⚠️  配置测试失败，请按照上述步骤重新配置")
        print("\n参考文档：")
        print("  WECHAT_BOT_SETUP.md")
    print("=" * 60)
    
    return 0 if bot_test_passed else 1


if __name__ == "__main__":
    sys.exit(main())
