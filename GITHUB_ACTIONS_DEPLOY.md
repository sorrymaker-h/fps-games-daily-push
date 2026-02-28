# GitHub Actions 部署指南

## 🎯 快速开始（3分钟搞定）

### 步骤 1：配置 GitHub Secrets

1. **进入 GitHub 仓库**
   - 打开你的 GitHub 仓库
   - 点击「Settings」标签

2. **添加 Secrets**
   - 左侧菜单点击「Secrets and variables」→「Actions」
   - 点击「New repository secret」按钮

3. **填写 Secret 信息**
   - **Name**: `COZE_API_TOKEN`
   - **Value**: 粘贴你的 Coze API Token（刚才提供的那个 JWT Token）
   - 点击「Add secret」

### 步骤 2：推送代码到 GitHub

```bash
git add .github/workflows/fps-games-daily.yml
git commit -m "feat: 添加 GitHub Actions 自动化部署"
git push
```

### 步骤 3：验证工作流

1. **进入 Actions 页面**
   - 在 GitHub 仓库中点击「Actions」标签
   - 找到「FPS Games Daily Newsletter」工作流

2. **手动触发测试**
   - 点击「Run workflow」按钮
   - 选择分支（通常是 main 或 master）
   - 点击「Run workflow」按钮

3. **查看执行结果**
   - 等待工作流执行完成（约 1-2 分钟）
   - 查看执行日志
   - 检查钉钉群是否收到消息

### 步骤 4：等待自动化运行

工作流将在每天北京时间 **10:00** 自动运行，无需手动触发！

---

## 📊 工作流说明

### 执行流程

```
GitHub Actions 触发
    ↓
调用 Coze 工作流 API
    ↓
Coze 执行工作流（搜索游戏 → 提取榜单 → 汇总资讯）
    ↓
发送消息到钉钉群
    ↓
GitHub Actions 显示执行结果
```

### 定时规则

- **Cron 表达式**: `0 2 * * *`
- **触发时间**: 每天 UTC 2:00（北京时间 10:00）
- **时区说明**: GitHub Actions 使用 UTC 时间，北京时间 = UTC + 8 小时

### 手动触发

你也可以手动触发工作流：
1. 进入 GitHub 仓库的「Actions」页面
2. 点击「Run workflow」
3. 选择分支并运行

---

## 🔍 查看执行日志

### 方法 1：GitHub Actions 页面

1. 进入「Actions」标签
2. 点击最近一次执行记录
3. 点击「Call Coze Workflow API」步骤
4. 查看详细日志

### 日志示例

```
🚀 调用 Coze 工作流 API...
HTTP 状态码: 200
响应内容:
{
  "status": "success",
  "message": "FPS游戏榜单推送成功（钉钉）",
  "run_id": "8df20872-a3ca-4da5-b5a6-e94ce96a89f9"
}
✅ 工作流调用成功！
🎉 FPS 游戏日报推送成功！
```

---

## ⚠️ 常见问题

### Q1: 工作流执行失败，提示 401 Unauthorized

**原因**: API Token 配置错误或已过期

**解决方法**:
1. 检查 GitHub Secrets 中的 `COZE_API_TOKEN` 是否正确
2. 在 Coze 平台重新生成 API Token
3. 更新 GitHub Secrets

### Q2: 工作流执行成功，但钉钉群没有收到消息

**原因**: Coze 工作流内部执行失败

**解决方法**:
1. 查看 GitHub Actions 日志中的 API 响应内容
2. 在 Coze 平台查看工作流执行日志
3. 检查钉钉机器人 Webhook 是否正确

### Q3: 如何修改推送时间？

**修改 Cron 表达式**:
1. 编辑 `.github/workflows/fps-games-daily.yml`
2. 修改 `schedule` 部分：
   ```yaml
   schedule:
     - cron: '0 2 * * *'  # UTC 时间
   ```
3. 提交并推送代码

**常用 Cron 表达式**:
| 时间 | Cron 表达式 | 说明 |
|------|------------|------|
| 每天 08:00 | `0 0 * * *` | UTC 0:00 = 北京时间 08:00 |
| 每天 10:00 | `0 2 * * *` | UTC 2:00 = 北京时间 10:00 |
| 每天 18:00 | `0 10 * * *` | UTC 10:00 = 北京时间 18:00 |
| 每天 22:00 | `0 14 * * *` | UTC 14:00 = 北京时间 22:00 |

### Q4: 工作流没有自动触发？

**可能原因**:
1. 代码还没有推送到 GitHub
2. 工作流文件路径错误
3. Cron 表达式配置错误

**解决方法**:
1. 确认 `.github/workflows/fps-games-daily.yml` 文件存在
2. 确认文件路径正确（注意前面有点）
3. 手动触发一次工作流测试
4. 查看工作流文件语法是否正确

### Q5: 如何查看 Coze 工作流的执行日志？

**方法**:
1. 进入 Coze 平台
2. 打开工作流项目
3. 点击「执行记录」或「日志」
4. 查看详细的执行日志

---

## 🔧 高级配置

### 添加环境变量

如果 Coze 工作流需要额外的环境变量：

```yaml
env:
  COZE_API_TOKEN: ${{ secrets.COZE_API_TOKEN }}
  CUSTOM_VAR: ${{ secrets.CUSTOM_VAR }}
```

### 添加超时设置

```yaml
jobs:
  run-fps-news:
    runs-on: ubuntu-latest
    timeout-minutes: 10  # 10 分钟超时
```

### 添加失败重试

```yaml
- name: Call Coze Workflow API
  uses: nick-invision/retry@v2
  with:
    timeout_minutes: 5
    max_attempts: 3
    retry_on: error
    command: |
      curl -X POST "https://zky2h3482d.coze.site/run" ...
```

---

## 📞 技术支持

### 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Cron 表达式生成器](https://crontab.guru/)
- [Coze 平台文档](https://www.coze.cn/docs)

### 联系方式

如有问题，请查看：
1. GitHub Actions 执行日志
2. Coze 平台工作流日志
3. 本项目 AGENTS.md 文件

---

**版本**: 1.0.0
**更新时间**: 2025-01-20
