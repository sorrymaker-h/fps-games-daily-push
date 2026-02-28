## 项目概述
- **名称**: FPS Games Daily Newsletter
- **功能**: 每天自动搜索全网热门PC端FPS游戏，区分国服和外服Top5榜单，并汇总当日资讯推送到钉钉群

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| search_fps_games | `nodes/search_fps_games_node.py` | task | 搜索热门FPS游戏 | - | - |
| extract_top5 | `nodes/extract_top5_node.py` | agent | 提取国服和外服Top5游戏 | - | `config/extract_top5_cfg.json` |
| search_game_news | `nodes/search_game_news_node.py` | task | 搜索单个游戏的资讯 | - | - |
| extract_news | `nodes/extract_news_node.py` | agent | 提取游戏的当日资讯 | - | `config/extract_news_cfg.json` |
| summarize_news | `nodes/summarize_news_node.py` | agent | 汇总所有游戏的资讯 | - | `config/summarize_news_cfg.json` |
| send_dingtalk | `nodes/send_dingtalk_node.py` | task | 发送消息到钉钉群 | - | - |

**类型说明**: task(任务节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 子图清单
| 子图名 | 文件位置 | 功能描述 | 被调用节点 |
|-------|---------|------|---------|-----------|
| news_loop_graph | `graphs/loop_graph.py` | 循环处理每个游戏的资讯 | extract_top5 |

## 技能使用
- **Coze Coding SDK**: 
  - 搜索功能: `search_fps_games_node`、`search_game_news_node`
  - LLM 功能: `extract_top5_node`、`extract_news_node`、`summarize_news_node`
- **钉钉机器人**: `send_dingtalk_node`

## 部署方式
- **Coze Coding 平台**: 使用平台内置的定时任务功能
- **环境变量**:
  - `DINGTALK_WEBHOOK_URL`: 钉钉机器人 Webhook URL（已内置在代码中）

## 技术栈
- **工作流引擎**: LangGraph 1.0
- **LLM**: Coze Coding SDK（豆包/DeepSeek 等模型）
- **搜索引擎**: Coze Coding SDK
- **Python 版本**: 3.12

## 钉钉机器人配置
- **Webhook URL**: `https://oapi.dingtalk.com/robot/send?access_token=5f30c823eb6bf1a6c16fae13f002d068b6b39bc7857e6eb651f3bfc56e8a85f3`
- **配置位置**: `src/graphs/nodes/send_dingtalk_node.py`
