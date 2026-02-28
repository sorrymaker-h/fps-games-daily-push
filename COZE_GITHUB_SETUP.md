# GitHub Actions 自动化部署指南

## 概述
本工作流使用 GitHub Actions 实现每天北京时间 10:00 自动推送 FPS 游戏资讯到钉钉群。

## 配置步骤

### 1. 获取 DeepSeek API Key
1. 访问 [DeepSeek 开放平台](https://platform.deepseek.com/)
2. 注册/登录账号
3. 进入「API Keys」页面
4. 创建新的 API Key
5. 复制 API Key（格式：`sk-xxxxxxxxxxxxx`）

### 2. 获取钉钉机器人 Webhook URL
1. 在钉钉群中添加自定义机器人
2. 安全设置选择「自定义关键词」或「加签」
3. 复制 Webhook URL（格式：`https://oapi.dingtalk.com/robot/send?access_token=xxxxx`）

### 3. 配置 GitHub Secrets
1. 进入 GitHub 仓库的「Settings」页面
2. 点击左侧「Secrets and variables」→「Actions」
3. 点击「New repository secret」
4. 添加以下两个密钥：

| Name | Value | 说明 |
|------|-------|------|
| `DEEPSEEK_API_KEY` | `sk-xxxxxxxxxxxxx` | DeepSeek API 密钥 |
| `DINGTALK_WEBHOOK_URL` | `https://oapi.dingtalk.com/robot/send?access_token=xxxxx` | 钉钉机器人 Webhook |

### 4. 启用 GitHub Actions
1. 将代码推送到 GitHub 仓库
2. 进入仓库的「Actions」页面
3. 确认工作流已启用（首次运行需要手动触发一次）

### 5. 手动测试工作流
1. 进入「Actions」页面
2. 选择「FPS Games Daily Newsletter」工作流
3. 点击「Run workflow」按钮
4. 选择分支，点击「Run workflow」

### 6. 验证自动化
工作流将在每天北京时间 10:00 自动运行，无需人工干预。

## 工作流说明

### 定时触发
- Cron 表达式：`0 2 * * *`
- 触发时间：每天 UTC 2:00（北京时间 10:00）

### 执行流程
1. 检出代码
2. 安装 Python 3.12
3. 安装依赖（requirements-github.txt）
4. 运行工作流（调用 `src/main.py`）

### 环境变量
- `LLM_API_KEY`：DeepSeek API 密钥
- `DINGTALK_WEBHOOK_URL`：钉钉机器人 Webhook

## 故障排查

### 问题 1：工作流执行失败
**解决方案**：
1. 查看 Actions 日志，检查报错信息
2. 确认 GitHub Secrets 是否正确配置
3. 确认依赖包是否正确安装

### 问题 2：DeepSeek API 调用失败
**解决方案**：
1. 确认 API Key 是否正确
2. 检查 DeepSeek 账户是否有免费额度
3. 查看是否有调用次数限制

### 问题 3：钉钉消息发送失败
**解决方案**：
1. 确认 Webhook URL 是否正确
2. 检查钉钉机器人安全设置（关键词/加签）
3. 确认机器人未被群管理员禁用

## 其他说明

### 本地运行
如果需要在本地运行工作流，需要设置环境变量：
```bash
export LLM_API_KEY="your-deepseek-api-key"
export DINGTALK_WEBHOOK_URL="your-dingtalk-webhook-url"
python src/main.py
```

### 修改推送时间
修改 `.github/workflows/fps-games-daily.yml` 中的 cron 表达式：
```yaml
schedule:
  - cron: '0 2 * * *'  # UTC 时间
```

时间转换：北京时间 = UTC 时间 + 8 小时

## 技术支持
如有问题，请检查：
1. GitHub Actions 日志
2. DeepSeek API 控制台
3. 钉钉机器人管理页面
