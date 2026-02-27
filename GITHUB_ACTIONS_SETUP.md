# GitHub Actions 自动化部署指南

## 快速开始（5分钟配置）

### 第一步：推送到GitHub

1. 确保你的项目已经在GitHub上
2. 如果还没有，创建一个新仓库并推送代码

```bash
# 初始化git仓库（如果还没有）
git init

# 添加所有文件
git add .

# 提交
git commit -m "Add FPS games daily push workflow"

# 推送到GitHub（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

### 第二步：配置Secrets

1. 进入你的GitHub仓库
2. 点击 **Settings**（设置）
3. 在左侧菜单找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**
5. 填写：
   - **Name**: `DINGTALK_WEBHOOK_URL`
   - **Value**: `https://oapi.dingtalk.com/robot/send?access_token=5f30c823eb6bf1a6c16fae13f002d068b6b39bc7857e6eb651f3bfc56e8a85f3`
6. 点击 **Add secret**

### 第三步：测试工作流

1. 进入仓库的 **Actions** 页面
2. 在左侧选择 **FPS Games Daily Push**
3. 点击 **Run workflow** 按钮
4. 选择分支，点击绿色 **Run workflow** 按钮
5. 等待执行完成（约2-5分钟）
6. 查看执行日志，确认成功

### 第四步：检查钉钉群

查看钉钉群是否收到了测试消息！✅

---

## 配置说明

### 定时执行时间

当前配置：每天 **北京时间10:00** 自动执行

```yaml
schedule:
  - cron: '0 2 * * *'  # UTC时间2点 = 北京时间10点
```

**修改时间**：
- UTC时间 = 北京时间 - 8小时
- 例如：北京时间8:00 → UTC时间0:00 → `cron: '0 0 * * *'`
- 例如：北京时间14:00 → UTC时间6:00 → `cron: '0 6 * * *'`

### 手动触发

工作流支持手动触发，可以随时测试：

1. 进入 **Actions** 页面
2. 选择 **FPS Games Daily Push**
3. 点击 **Run workflow**

---

## 功能特性

### ✅ 完全免费
- GitHub Actions每月免费2000分钟
- 每次执行约2-5分钟，远低于免费额度

### ✅ 完全自动化
- 每天自动执行，无需人工干预
- 不需要你的服务器或电脑
- 即使关机也能正常推送

### ✅ 可视化监控
- 查看每次执行的详细日志
- 执行状态一目了然
- 失败自动记录日志

### ✅ 安全可靠
- 使用Secrets存储敏感信息
- 钉钉Webhook URL不会泄露
- 每次执行都有记录

---

## 查看执行记录

### 方式1：GitHub网页查看

1. 进入仓库的 **Actions** 页面
2. 查看所有工作流运行记录
3. 点击某次运行查看详细日志

### 方式2：手机查看

1. 打开GitHub手机App
2. 进入你的仓库
3. 点击 **Actions** 标签
4. 查看执行状态

---

## 常见问题

### Q1: 为什么北京时间10点没有收到消息？

**A**: 可能原因：
1. 检查Actions页面，工作流是否执行
2. 查看执行日志，是否有错误
3. 确认Secrets是否正确配置
4. 检查钉钉群机器人是否正常

### Q2: 如何修改推送时间？

**A**: 编辑 `.github/workflows/fps-games-daily.yml`：
```yaml
schedule:
  - cron: '0 2 * * *'  # 修改这里的cron表达式
```
然后提交并推送：
```bash
git add .
git commit -m "Update schedule time"
git push
```

### Q3: 工作流执行失败了怎么办？

**A**:
1. 进入Actions页面
2. 查看失败的工作流
3. 点击查看详细日志
4. 根据错误信息排查问题
5. 修复后重新推送代码

### Q4: 如何知道执行是否成功？

**A**:
1. 查看钉钉群是否收到消息
2. 查看GitHub Actions页面
3. ✅ 绿色表示成功，❌ 红色表示失败

### Q5: 可以每天推送多次吗？

**A**: 可以！添加多个cron表达式：
```yaml
schedule:
  - cron: '0 2 * * *'  # 10:00
  - cron: '0 14 * * *' # 22:00
```

---

## 时区对照表

| 北京时间 | UTC时间 | Cron表达式 |
|---------|---------|-----------|
| 8:00 | 0:00 | `0 0 * * *` |
| 10:00 | 2:00 | `0 2 * * *` |
| 12:00 | 4:00 | `0 4 * * *` |
| 14:00 | 6:00 | `0 6 * * *` |
| 16:00 | 8:00 | `0 8 * * *` |
| 18:00 | 10:00 | `0 10 * * *` |
| 20:00 | 12:00 | `0 12 * * *` |
| 22:00 | 14:00 | `0 14 * * *` |

---

## 高级配置

### 修改执行环境

如果需要使用不同版本的Python：

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # 修改版本号
```

### 添加环境变量

在工作流中添加更多环境变量：

```yaml
- name: Run FPS games workflow
  env:
    DINGTALK_WEBHOOK_URL: ${{ secrets.DINGTALK_WEBHOOK_URL }}
    CUSTOM_VAR: ${{ secrets.CUSTOM_VAR }}
  run: |
    python scripts/schedule_fps_games.py --manual
```

### 发送成功/失败通知

可以添加钉钉通知步骤：

```yaml
- name: Notify on success
  if: success()
  run: |
    echo "工作流执行成功！"

- name: Notify on failure
  if: failure()
  run: |
    echo "工作流执行失败！"
```

---

## 成本说明

### GitHub Actions 免费额度

| 账户类型 | 每月免费分钟数 |
|---------|--------------|
| 公共仓库 | 无限制 |
| 私有仓库（Free） | 2000分钟 |
| 私有仓库（Pro） | 3000分钟 |
| 私有仓库（Team） | 10000分钟 |

### 本工作流成本估算

- 每次执行约2-5分钟
- 每天1次 = 每月约90-150分钟
- **完全在免费额度内**

---

## 维护建议

1. **定期查看执行记录**：确保工作流正常运行
2. **监控钉钉消息**：确认每天收到推送
3. **更新依赖**：定期更新Python依赖包
4. **备份配置**：重要配置做好备份

---

## 技术支持

遇到问题？
1. 查看 [GitHub Actions 文档](https://docs.github.com/en/actions)
2. 查看 [Cron 表达式生成器](https://crontab.guru/)
3. 查看项目Issues

---

## 总结

✅ **5分钟配置完成**
✅ **每天自动推送**
✅ **完全免费**
✅ **不需要服务器**
✅ **可视化监控**

配置完成后，你什么都不用做，每天10点自动推送FPS游戏资讯到钉钉群！🎉
