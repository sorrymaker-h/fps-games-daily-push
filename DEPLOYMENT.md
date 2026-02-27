# 自动化部署方案

## 方案1：使用系统定时任务（cron）- 推荐用于本地服务器

### 优点
- ✅ 不需要持续运行进程
- ✅ 系统原生支持，稳定可靠
- ✅ 执行完自动退出
- ✅ 日志自动记录

### 配置步骤

#### Linux/Mac

```bash
# 1. 编辑crontab
crontab -e

# 2. 添加以下行（根据你的路径修改）
0 10 * * * cd /path/to/your/project && /usr/bin/python3 scripts/schedule_fps_games.py --manual >> /tmp/fps_games.log 2>&1

# 3. 保存退出
```

#### 参数说明
```
0 10 * * * 
│ │ │ │ │
│ │ │ │ └─ 星期几（0-6，0是周日）
│ │ │ └─── 月份（1-12）
│ │ └───── 日期（1-31）
│ └─────── 小时（0-23）
└───────── 分钟（0-59）
```

#### 查看日志
```bash
tail -f /tmp/fps_games.log
```

#### 验证配置
```bash
# 查看当前的定时任务
crontab -l

# 测试执行（立即执行一次）
cd /path/to/your/project && python3 scripts/schedule_fps_games.py --manual
```

### Windows系统

使用任务计划程序：
1. 打开"任务计划程序"
2. 创建基本任务
3. 触发器：每天 10:00
4. 操作：启动程序
5. 程序：`python.exe`
6. 参数：`C:\path\to\project\scripts\schedule_fps_games.py --manual`
7. 起始于：`C:\path\to\project`

---

## 方案2：使用GitHub Actions - 推荐用于云端

### 优点
- ✅ 完全免费
- ✅ 不需要自己的服务器
- ✅ 自动执行
- ✅ 执行记录可视化
- ✅ 支持手动触发

### 配置步骤

#### 1. 创建GitHub Actions配置文件

创建文件 `.github/workflows/fps-games-daily.yml`：

```yaml
name: FPS Games Daily Push

on:
  schedule:
    # UTC时间2点 = 北京时间10点
    - cron: '0 2 * * *'
  workflow_dispatch:  # 允许手动触发

jobs:
  push-games-news:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install schedule requests python-dotenv
      
      - name: Run FPS games workflow
        env:
          DINGTALK_WEBHOOK_URL: ${{ secrets.DINGTALK_WEBHOOK_URL }}
        run: |
          python scripts/schedule_fps_games.py --manual
      
      - name: Upload logs
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: workflow-logs
          path: /tmp/fps_games.log
```

#### 2. 配置Secrets

1. 进入GitHub仓库
2. Settings → Secrets and variables → Actions
3. New repository secret
4. Name: `DINGTALK_WEBHOOK_URL`
5. Value: `https://oapi.dingtalk.com/robot/send?access_token=你的token`

#### 3. 推送到GitHub

```bash
git add .
git commit -m "Add GitHub Actions workflow"
git push
```

#### 4. 查看执行记录

访问：`https://github.com/你的用户名/你的仓库/actions`

#### 5. 手动触发测试

访问Actions页面，选择"FPS Games Daily Push"工作流，点击"Run workflow"

---

## 方案3：使用云函数（阿里云/腾讯云）- 企业级

### 优点
- ✅ 按需付费，几乎免费
- ✅ 完全自动化
- ✅ 不需要管理服务器
- ✅ 高可用性

### 阿里云函数计算配置

#### 1. 创建函数

登录阿里云控制台，创建函数：
- 运行时：Python 3
- 代码上传方式：直接上传

#### 2. 函数代码（index.py）

```python
import json
import os
import sys

# 添加项目路径
sys.path.insert(0, '/code')

from graphs.graph import main_graph
from graphs.state import GraphInput

def handler(event, context):
    """函数入口"""
    try:
        # 设置环境变量
        os.environ['DINGTALK_WEBHOOK_URL'] = os.getenv('DINGTALK_WEBHOOK_URL')
        
        # 执行工作流
        workflow_input = GraphInput(trigger_type="scheduled")
        result = main_graph.invoke(workflow_input)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": result.status,
                "message": result.message
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
```

#### 3. 配置环境变量

在函数配置中添加：
- Key: `DINGTALK_WEBHOOK_URL`
- Value: `https://oapi.dingtalk.com/robot/send?access_token=你的token`

#### 4. 配置定时触发器

- 触发方式：定时触发
- Cron表达式：`0 10 * * *`

#### 5. 测试函数

点击"测试函数"按钮，手动触发一次。

---

## 方案对比

| 方案 | 成本 | 复杂度 | 稳定性 | 适用场景 |
|------|------|--------|--------|----------|
| cron | 免费 | ⭐⭐ | ⭐⭐⭐⭐⭐ | 本地服务器 |
| GitHub Actions | 免费 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 代码仓库自动化 |
| 云函数 | 几乎免费 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 企业生产环境 |

---

## 推荐方案选择

### 个人/小团队
**推荐：GitHub Actions**
- 完全免费
- 配置简单
- 可视化监控

### 本地服务器
**推荐：cron**
- 系统原生
- 无需额外服务
- 稳定可靠

### 企业生产环境
**推荐：云函数**
- 高可用性
- 弹性扩展
- 企业级监控

---

## 注意事项

### 时区问题
- cron使用系统时区
- GitHub Actions使用UTC时间
- 云函数使用配置的时区

### 日志记录
- 建议配置日志输出到文件
- 定期清理旧日志
- 监控执行失败情况

### 失败重试
- 建议配置失败重试机制
- 设置告警通知
- 记录失败原因

### 成本控制
- 免费额度通常足够
- 监控使用量
- 及时优化代码
