## 项目概述
- **名称**: PC端FPS游戏榜单推送工作流（国服+外服）
- **功能**: 每天早上10点自动筛选全网热门PC端FPS游戏，区分国服和外服两个板块，各给出top5榜单（共10个游戏），并总结对应每一款游戏的当日资讯（活动、更新、赛事等），通过钉钉机器人发送到指定群组

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| search_games | `nodes/search_fps_games_node.py` | task | 搜索热门PC端FPS游戏 | - | - |
| extract_top5 | `nodes/extract_top5_node.py` | agent | 提取国服和外服Top5游戏 | - | `config/extract_top5_llm_cfg.json` |
| prepare_loop | `graph.py` | task | 准备循环游戏列表（合并国服和外服） | - | - |
| loop_news | `graph.py` | looparray | 循环搜索10个游戏的资讯 | - | - |
| summarize_news | `nodes/summarize_news_node.py` | agent | 按国服和外服汇总资讯 | - | `config/summarize_news_llm_cfg.json` |
| send_dingtalk | `nodes/send_dingtalk_node.py` | task | 发送钉钉消息 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
| 子图名 | 文件位置 | 功能描述 | 被调用节点 |
|-------|---------|------|---------|-----------|
| game_news_loop_graph | `graphs/loop_graph.py` | 循环处理每款游戏的资讯（搜索+提取） | loop_news |

### 子图内部节点
| 节点名 | 类型 | 功能描述 | 配置文件 |
|-------|------|---------|---------|
| prepare_game | task | 准备当前游戏信息 | - |
| search_news | task | 搜索游戏资讯 | - |
| extract_news | agent | 提取关键资讯 | `config/extract_news_llm_cfg.json` |

## 技能使用
- **web-search**: 节点 `search_games`、子图节点 `search_news` 使用，用于搜索热门FPS游戏和每款游戏的资讯
- **llm**: 节点 `extract_top5`、`summarize_news`、子图节点 `extract_news` 使用，用于分析和整理游戏信息
- **dingtalk-bot**: 节点 `send_dingtalk` 使用，用于发送钉钉消息到群组

## 配置文件说明
- `config/extract_top5_llm_cfg.json`: 提取Top5游戏的模型配置
- `config/extract_news_llm_cfg.json`: 提取游戏资讯的模型配置
- `config/summarize_news_llm_cfg.json`: 汇总资讯的模型配置

## 定时任务
- **文件**: `scripts/schedule_fps_games.py`
- **功能**: 每天早上10点自动执行工作流
- **运行方式**:
  - 定时模式: `python scripts/schedule_fps_games.py`
  - 手动测试: `python scripts/schedule_fps_games.py --manual`

## 工作流流程
1. **搜索热门PC端FPS游戏**: 使用网络搜索获取热门PC端FPS游戏信息（排除手游）
2. **提取国服和外服Top5**: 使用大模型分析搜索结果，区分国服和外服游戏，各提取排名前5的PC端FPS游戏（共10个）
3. **准备循环**: 合并国服和外服游戏列表，准备循环处理
4. **循环搜索资讯**: 对每款游戏执行：
   - 搜索该游戏的当日资讯（活动、更新、赛事等）
   - 提取关键资讯
5. **汇总资讯**: 将所有游戏的资讯按国服和外服两个板块整理成一份完整的报告
6. **发送微信**: 通过微信机器人将报告发送到指定群组

## 注意事项
- **钉钉机器人配置**：项目已内置钉钉Webhook，可直接使用
  - 如需自定义，设置环境变量：`export DINGTALK_WEBHOOK_URL=你的webhook_url`
  - 使用 `scripts/test_dingtalk_bot.py` 测试配置
  - 参考 `DINGTALK_BOT_SETUP.md` 文件
- 工作流执行时间可能较长（需要多次网络搜索和大模型调用）
- 建议在测试时使用 `--manual` 参数手动执行

## 快速开始

### 1. 测试钉钉机器人（可选）
```bash
# 测试内置配置
python scripts/test_dingtalk_bot.py

# 或使用自定义配置
export DINGTALK_WEBHOOK_URL=你的webhook_url
python scripts/test_dingtalk_bot.py
```

### 2. 运行工作流
```bash
# 手动测试
python scripts/schedule_fps_games.py --manual

# 定时运行（每天早上10点）
python scripts/schedule_fps_games.py
```
