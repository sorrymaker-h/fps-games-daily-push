# Coze Coding 平台部署指南

## 📋 概述
本工作流使用 Coze Coding 平台的内置能力，无需配置额外的 API Key，只需在平台中设置定时任务即可实现每天自动推送。

## ✅ 钉钉机器人配置

### 已配置信息
- **Webhook URL**: `https://oapi.dingtalk.com/robot/send?access_token=5f30c823eb6bf1a6c16fae13f002d068b6b39bc7857e6eb651f3bfc56e8a85f3`
- **配置位置**: `src/graphs/nodes/send_dingtalk_node.py`

### 如何修改 Webhook URL
如果需要更换钉钉机器人，请修改 `src/graphs/nodes/send_dingtalk_node.py` 文件中的 `get_dingtalk_webhook()` 函数：

```python
def get_dingtalk_webhook():
    """获取钉钉机器人webhook URL"""
    # 优先从环境变量读取
    webhook_url = os.getenv("DINGTALK_WEBHOOK_URL")
    if webhook_url:
        return webhook_url
    
    # 如果环境变量没有，使用默认配置
    default_url = "YOUR_DINGTALK_WEBHOOK_URL_HERE"  # 修改这里
    return default_url
```

## 🚀 Coze Coding 平台部署步骤

### 1. 创建或打开项目
1. 登录 [Coze Coding 平台](https://coze.cn/)
2. 打开或创建新的项目
3. 上传代码到项目

### 2. 配置定时任务
在 Coze Coding 平台中，找到「定时任务」或「Cron 任务」设置：

#### 方法 1：使用平台 UI 配置
1. 进入项目的「设置」页面
2. 找到「定时任务」或「自动化」选项
3. 点击「新建定时任务」
4. 配置如下：
   - **任务名称**: FPS 游戏日报推送
   - **触发时间**: 每天 10:00
   - **执行命令**: `python src/main.py`
   - **输入参数**: `{"trigger_type": "scheduled"}`

#### 方法 2：使用 Cron 表达式
如果平台支持 Cron 表达式，使用以下配置：
```cron
0 10 * * *
```
- `0`: 第 0 分钟
- `10`: 第 10 小时
- `*`: 每天
- `*`: 每月
- `*`: 每周

### 3. 启用定时任务
1. 保存配置
2. 启用定时任务
3. 确认状态为「运行中」

### 4. 测试定时任务
1. 点击「手动触发」按钮
2. 查看执行日志
3. 确认钉钉群收到消息

## 📊 工作流架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     FPS 游戏日报工作流                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. 搜索热门FPS游戏                                              │
│     ↓                                                           │
│  2. 提取国服/外服 Top5 游戏                                      │
│     ↓                                                           │
│  3. 循环搜索每个游戏的资讯                                       │
│     ├─ 搜索单个游戏的资讯                                        │
│     ├─ 提取当日资讯                                             │
│     └─ 添加到资讯列表                                           │
│     ↓                                                           │
│  4. 汇总所有游戏的资讯                                          │
│     ↓                                                           │
│  5. 发送到钉钉群                                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 🔍 测试工作流

### 本地测试
```bash
# 安装依赖
pip install -r requirements.txt

# 运行工作流
python src/main.py --input '{"trigger_type": "manual"}'
```

### 平台测试
1. 进入 Coze Coding 平台
2. 找到工作流
3. 点击「运行」按钮
4. 查看输出结果

## 📝 输出示例

工作流将生成类似以下的日报消息：

```
🎮 FPS 游戏日报 - 2025年01月20日

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【国服热门 Top 5】

1. 反恐精英：全球攻势
   - 今日资讯: ...

2. 绝地求生
   - 今日资讯: ...

...

【外服热门 Top 5】

1. 瓦罗兰特
   - 今日资讯: ...

2. Apex 英雄
   - 今日资讯: ...

...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
发送时间: 2025-01-20 10:00:00
```

## ⚙️ 配置文件

### LLM 配置
- `config/extract_top5_cfg.json`: 提取 Top5 游戏的 LLM 配置
- `config/extract_news_cfg.json`: 提取资讯的 LLM 配置
- `config/summarize_news_cfg.json`: 汇总资讯的 LLM 配置

### 修改 LLM 配置
如果需要更换模型，修改配置文件中的 `model` 字段：
```json
{
  "config": {
    "model": "doubao-seed-1-8-251228",  // 修改这里
    "temperature": 0.7,
    "max_completion_tokens": 2000
  }
}
```

## 🐛 故障排查

### 问题 1: 工作流执行失败
**解决方案**:
1. 查看执行日志
2. 检查网络连接
3. 确认 Coze Coding SDK 正确配置

### 问题 2: 钉钉消息未发送
**解决方案**:
1. 确认 Webhook URL 正确
2. 检查钉钉机器人安全设置
3. 确认机器人未被禁用

### 问题 3: 搜索结果为空
**解决方案**:
1. 检查网络连接
2. 确认搜索关键词正确
3. 尝试修改搜索查询

### 问题 4: 定时任务未触发
**解决方案**:
1. 确认定时任务已启用
2. 检查 Cron 表达式是否正确
3. 查看平台定时任务状态

## 📞 技术支持

如有问题，请联系：
- Coze Coding 平台客服
- 查看 Coze Coding 平台文档
- 查看 AGENTS.md 了解项目结构

---

**版本**: 1.0.0
**更新时间**: 2025-01-20
