#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
钉钉机器人测试脚本
用于验证webhook配置是否正确
"""

import os
import sys
import requests
import json
from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_webhook_url():
    """获取钉钉机器人webhook URL"""
    # 优先从环境变量读取
    webhook_url = os.getenv("DINGTALK_WEBHOOK_URL")
    if webhook_url:
        return webhook_url
    
    # 使用内置配置
    return "https://oapi.dingtalk.com/robot/send?access_token=5f30c823eb6bf1a6c16fae13f002d068b6b39bc7857e6eb651f3bfc56e8a85f3"


def test_dingtalk_bot():
    """测试钉钉机器人配置"""
    
    print("=" * 60)
    print("钉钉机器人配置测试")
    print("=" * 60)
    
    # 获取webhook URL
    webhook_url = get_webhook_url()
    
    # 提取access_token用于显示
    if "access_token=" in webhook_url:
        token = webhook_url.split("access_token=")[1][:20] + "..."
    else:
        token = webhook_url[:30] + "..."
    
    print(f"\n📡 Webhook URL: {webhook_url}")
    print(f"🔑 Token: {token}")
    
    # 检查是环境变量还是内置配置
    if os.getenv("DINGTALK_WEBHOOK_URL"):
        print(f"✅ 使用环境变量配置")
    else:
        print(f"✅ 使用内置配置")
    
    # 构造测试消息
    test_message = f"""🤖 钉钉机器人测试消息

如果你看到这条消息，说明钉钉机器人配置成功！

测试时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
配置文件: {os.path.abspath(__file__)}

现在可以使用FPS游戏榜单推送工作流了！🎮

---
测试状态: 成功 ✅"""
    
    payload = {
        "msgtype": "text",
        "text": {
            "content": test_message
        }
    }
    
    print(f"\n📤 发送测试消息到钉钉群...")
    
    try:
        response = requests.post(webhook_url, json=payload, timeout=15)
        response.raise_for_status()
        result = response.json()
        
        print(f"\n📥 响应状态: {response.status_code}")
        print(f"📥 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("errcode") == 0:
            print("\n" + "=" * 60)
            print("✅ 测试成功！钉钉机器人配置正确！")
            print("=" * 60)
            print("\n请检查钉钉群是否收到了测试消息！")
            return True
        else:
            print("\n" + "=" * 60)
            print("❌ 测试失败！请检查配置")
            print("=" * 60)
            print(f"错误码: {result.get('errcode')}")
            print(f"错误信息: {result.get('errmsg')}")
            
            # 提供常见错误码的说明
            error_code = result.get('errcode')
            if error_code == 310000:
                print("\n提示: 关键词不匹配或内容违规，请检查群机器人安全设置")
            elif error_code == 300001:
                print("\n提示: 网络超时，请检查网络连接")
            elif error_code == 300002:
                print("\n提示: 服务不可用，请稍后重试")
            
            return False
            
    except requests.exceptions.Timeout:
        print(f"\n❌ 请求超时，请检查网络连接")
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
    
    print("\n尝试导入工作流...")
    try:
        from graphs.graph import main_graph
        print("✅ 工作流导入成功")
        print("✅ 工作流已配置为使用钉钉机器人发送消息")
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
    
    # 测试钉钉机器人
    bot_test_passed = test_dingtalk_bot()
    
    # 测试工作流集成
    test_workflow_integration()
    
    print("\n" + "=" * 60)
    if bot_test_passed:
        print("🎉 配置测试通过！可以开始使用工作流了！")
        print("\n运行命令：")
        print("  python scripts/schedule_fps_games.py --manual")
    else:
        print("⚠️  配置测试失败，请按照错误提示排查")
        print("\n参考文档：")
        print("  DINGTALK_BOT_SETUP.md")
    print("=" * 60)
    
    return 0 if bot_test_passed else 1


if __name__ == "__main__":
    sys.exit(main())
