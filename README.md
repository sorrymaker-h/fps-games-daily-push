# PC端FPS游戏榜单推送工作流

## 项目简介

这是一个自动化工作流，每天早上10点自动推送PC端FPS游戏的当日资讯到微信企业群。

## 功能特性

- ✅ **智能筛选**: 自动搜索全网热门PC端FPS游戏
- ✅ **国服外服区分**: 区分国服Top5和外服Top5，共10个游戏
- ✅ **当日资讯**: 只推送当天的游戏资讯（活动、更新、赛事等）
- ✅ **定时推送**: 每天早上10点自动推送
- ✅ **钉钉发送**: 通过钉钉机器人发送到指定群组（已内置配置）
- ✅ **格式美观**: 按国服和外服两个板块组织，清晰易读

## 快速开始

### 方式1：GitHub Actions 自动化（推荐）🌟

**优势**：
- ✅ 完全免费
- ✅ 完全云端，不需要服务器
- ✅ 每天10点自动推送
- ✅ 可视化监控执行记录

**配置步骤**（5分钟搞定）：

1. **推送到GitHub**
   ```bash
   # 参考 GITHUB_PUSH_GUIDE.md
   git add .
   git commit -m "Add FPS games workflow"
   git push
   ```

2. **配置Secrets**
   - 进入仓库 Settings → Secrets → Actions
   - 添加 `DINGTALK_WEBHOOK_URL`
   - Value: `https://oapi.dingtalk.com/robot/send?access_token=5f30c823eb6bf1a6c16fae13f002d068b6b39bc7857e6eb651f3bfc56e8a85f3`

3. **测试工作流**
   - 进入仓库 Actions 页面
   - 点击 Run workflow 手动测试

4. **完成！** 每天10点自动推送 🎉

详细配置指南：[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)

---

### 方式2：本地定时任务（cron）

**适用场景**：有本地服务器或24小时运行的电脑

配置步骤请参考：[DEPLOYMENT.md](DEPLOYMENT.md)

---

### 方式3：手动执行（测试用）

```bash
# 立即执行一次，用于测试
python scripts/schedule_fps_games.py --manual
```

## 工作流流程

```
1. 搜索热门PC端FPS游戏
   ↓
2. 提取国服Top5 + 外服Top5（共10个游戏）
   ↓
3. 合并游戏列表
   ↓
4. 循环搜索每款游戏的当日资讯
   ├─ 搜索：游戏名 + 今日日期 + 关键词
   └─ 提取：过滤非当日资讯
   ↓
5. 按国服和外服汇总资讯
   ├─ 国服板块（5款游戏）
   └─ 外服板块（5款游戏）
   ↓
6. 发送微信消息到群组
```

## 项目结构

```
.
├── src/
│   ├── graphs/
│   │   ├── state.py                    # 状态定义
│   │   ├── graph.py                    # 主图编排
│   │   ├── loop_graph.py               # 子图（循环搜索资讯）
│   │   └── nodes/                      # 节点实现
│   │       ├── search_fps_games_node.py      # 搜索FPS游戏
│   │       ├── extract_top5_node.py          # 提取Top5
│   │       ├── search_game_news_node.py      # 搜索游戏资讯
│   │       ├── extract_news_node.py          # 提取关键资讯
│   │       ├── summarize_news_node.py        # 汇总资讯
│   │       └── send_wechat_node.py           # 发送微信
│   └── ...
├── config/                              # 配置文件
│   ├── extract_top5_llm_cfg.json        # Top5提取配置
│   ├── extract_news_llm_cfg.json        # 资讯提取配置
│   └── summarize_news_llm_cfg.json      # 资讯汇总配置
├── scripts/
│   ├── schedule_fps_games.py            # 定时任务脚本
│   └── test_wechat_bot.py               # 微信机器人测试
├── WECHAT_BOT_SETUP.md                  # 微信机器人配置指南
├── AGENTS.md                            # 工作流详细文档
└── README.md                            # 本文件
```

## 配置说明

### 钉钉机器人配置

**已内置配置（无需设置）：**
项目已内置钉钉机器人Webhook，可以直接使用！

**自定义配置：**
如果需要使用自己的钉钉机器人，设置环境变量：
```bash
export DINGTALK_WEBHOOK_URL=你的webhook_url
```

详细配置指南：[DINGTALK_BOT_SETUP.md](DINGTALK_BOT_SETUP.md)

### 模型配置

所有模型配置文件位于 `config/` 目录下：

- `extract_top5_llm_cfg.json`: 提取国服和外服Top5游戏的配置
- `extract_news_llm_cfg.json`: 提取当日资讯的配置
- `summarize_news_llm_cfg.json`: 按板块汇总资讯的配置

可以根据需要调整模型参数（temperature、max_tokens等）。

## 输出示例

```
🎮 PC端FPS游戏今日资讯（2026年2月27日）

🇨🇳 国服游戏板块

1. 无畏契约
   📅 今日活动：周末双倍经验活动开启
   🔄 版本更新：新角色「幻影」上线
   🏆 赛事信息：无畏契约大师赛直播中

2. CS2
   📅 今日活动：限时皮肤折扣
   🔄 版本更新：平衡性调整
...

🌍 外服游戏板块

1. Apex英雄
   📅 今日活动：新通行证第3赛季
   🏆 赛事信息：ALGS全球总决赛
...

---
生成时间：2026年2月27日 10:00:00
```

## 常见问题

### Q1: 提示 "发送失败"
**A**: 检查：
1. Webhook URL是否正确
2. 钉钉群中机器人是否还存在
3. 机器人是否有权限发送消息
4. 是否触发了关键词过滤（如敏感词）

### Q2: 测试通过但工作流发送失败
**A**: 检查：
1. webhook URL是否正确
2. 网络连接是否正常
3. 钉钉群中机器人权限是否正常
4. 消息内容是否触发安全过滤

### Q3: 资讯不是当天的
**A**: 工作流会自动获取当前日期并搜索当日资讯，如果仍显示旧资讯，可能是：
1. 搜索结果中确实没有当日资讯
2. 游戏官方未发布今日资讯

### Q4: 想要修改推送时间
**A**: 编辑 `scripts/schedule_fps_games.py`，修改 `schedule.every().day.at("10:00")` 中的时间

### Q5: 如何使用自己的钉钉机器人
**A**: 设置环境变量：
```bash
export DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=你的access_token
```

## 技术栈

- **工作流引擎**: LangGraph
- **网络搜索**: coze-coding-dev-sdk (web-search)
- **大语言模型**: coze-coding-dev-sdk (LLM)
- **消息推送**: 企业微信机器人 API
- **定时任务**: schedule 库

## 依赖安装

```bash
pip install schedule requests
```

## 开发说明

### 添加新的游戏类别

修改 `config/extract_top5_llm_cfg.json` 中的系统提示词，添加新的分类规则。

### 修改推送格式

修改 `config/summarize_news_llm_cfg.json` 中的输出格式说明。

### 添加更多资讯类型

修改 `config/extract_news_llm_cfg.json`，添加新的资讯类别。

## 文档

- [AGENTS.md](AGENTS.md): 详细的工作流技术文档
- [DINGTALK_BOT_SETUP.md](DINGTALK_BOT_SETUP.md): 钉钉机器人配置指南

## 许可证

MIT License

## 联系方式

如有问题，请查看文档或提交Issue。
