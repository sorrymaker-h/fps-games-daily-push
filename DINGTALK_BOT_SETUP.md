# 钉钉机器人配置指南

## 方式1：使用环境变量配置（推荐）

### 步骤1：获取钉钉机器人Webhook URL

1. 在钉钉群聊中，点击右上角 "..."
2. 选择 "智能群助手" -> "添加机器人" -> "自定义"
3. 创建机器人后，会获得一个Webhook地址，格式如下：
   ```
   https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 步骤2：设置环境变量

**临时设置（当前会话有效）：**
```bash
export DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=你的access_token
```

**永久设置：**

在 `.coze` 文件中添加环境变量：
```bash
echo "export DINGTALK_WEBHOOK_URL=https://oapi.dingtalk.com/robot/send?access_token=你的access_token" >> .coze
source .coze
```

### 步骤3：验证配置

运行测试脚本：
```bash
python scripts/test_dingtalk_bot.py
```

## 方式2：使用内置Webhook（已配置）

当前项目已内置了你提供的钉钉Webhook：
```
https://oapi.dingtalk.com/robot/send?access_token=5f30c823eb6bf1a6c16fae13f002d068b6b39bc7857e6eb651f3bfc56e8a85f3
```

**无需配置，直接使用！**

## 测试Webhook是否正常

可以使用以下命令测试webhook是否有效：

```bash
curl -X POST "https://oapi.dingtalk.com/robot/send?access_token=你的access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "这是一条测试消息"
    }
  }'
```

如果返回 `{"errcode":0,"errmsg":"ok"}`，说明配置正确。

## 运行工作流

配置完成后（或使用内置webhook），运行工作流：

```bash
# 手动测试
python scripts/schedule_fps_games.py --manual

# 定时运行（每天早上10点）
python scripts/schedule_fps_games.py
```

## 常见问题

### Q1: 提示 "发送失败"
**A**: 检查：
1. Webhook URL是否正确
2. 钉钉群中机器人是否还存在
3. 机器人是否有权限发送消息

### Q2: 消息发送成功但群内没收到
**A**: 可能原因：
1. 机器人被群主禁言
2. 群成员消息过多，机器人消息被折叠
3. Webhook URL已失效

### Q3: 想要使用自己的钉钉机器人
**A**: 
1. 按照方式1配置环境变量 `DINGTALK_WEBHOOK_URL`
2. 环境变量优先级高于内置配置

## 安全建议

1. **不要泄露Webhook URL**: Webhook URL是机器人发送消息的唯一凭证
2. **定期更换**: 如果发现异常，可以重新创建机器人获取新的Webhook URL
3. **限制机器人权限**: 在钉钉群设置中限制机器人的操作权限

## 钉钉机器人特性

### 支持的消息类型
- ✅ 文本消息
- ✅ Markdown消息
- ✅ 链接消息
- ✅ ActionCard消息
- ✅ FeedCard消息

当前工作流使用文本消息，如需支持其他类型，可以修改 `send_dingtalk_node.py`。

### 机器人限制
- 每个机器人每分钟最多发送20条消息
- 每个机器人每天最多发送500条消息

如需更高的发送频率，请联系钉钉管理员申请。
