# 微信机器人配置指南

## 方式1：通过环境变量配置（推荐）

### 步骤1：获取企业微信机器人Webhook URL

1. 在企业微信群聊中，点击右上角 "..."
2. 选择 "添加群机器人"
3. 创建机器人后，会获得一个Webhook地址，格式如下：
   ```
   https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   ```

### 步骤2：提取Webhook Key

从上面的URL中提取 `key=` 后面的部分，例如：
```
WECHAT_BOT_WEBHOOK_KEY=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### 步骤3：设置环境变量

**临时设置（当前会话有效）：**
```bash
export WECHAT_BOT_WEBHOOK_KEY=你的webhook_key
```

**永久设置：**

在 `.coze` 文件中添加环境变量：
```bash
# 在项目根目录创建或编辑 .coze 文件
echo "export WECHAT_BOT_WEBHOOK_KEY=你的webhook_key" >> .coze
source .coze
```

或者在 `scripts/load_env.sh` 中添加（如果存在）：
```bash
export WECHAT_BOT_WEBHOOK_KEY=你的webhook_key
```

### 步骤4：验证配置

运行工作流测试：
```bash
python scripts/schedule_fps_games.py --manual
```

## 方式2：通过集成配置（需平台支持）

如果平台支持集成配置，可以按照以下步骤操作：

1. 进入平台的集成管理页面
2. 找到 "微信机器人（企业微信版）" 集成
3. 配置 webhook_url：
   ```json
   {
     "webhook_key": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   }
   ```
4. 保存配置

## 测试Webhook是否正常

可以使用以下命令测试webhook是否有效：

```bash
curl -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=你的webhook_key" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "text",
    "text": {
      "content": "这是一条测试消息"
    }
  }'
```

如果返回 `{"errcode":0,"errmsg":"ok"}`，说明配置正确。

## 常见问题

### Q1: 提示 "未配置微信机器人webhook key"
**A**: 请检查：
1. 环境变量是否设置：`echo $WECHAT_BOT_WEBHOOK_KEY`
2. 环境变量是否在运行时加载
3. webhook key 是否正确

### Q2: 提示 "集成凭证请求失败"
**A**: 说明集成凭证未配置，请使用方式1（环境变量）配置

### Q3: 消息发送失败，返回错误码
**A**: 查看企业微信文档的常见错误码：
- 40001: 参数不合法
- 45009: 接口调用超过限制
- 其他错误码参考企业微信官方文档

## 安全建议

1. **不要泄露webhook key**: webhook key是机器人发送消息的唯一凭证，泄露后可能导致滥用
2. **使用环境变量**: 避免将webhook key硬编码在代码中
3. **定期更换**: 如果发现异常，可以重新创建机器人获取新的webhook key

## 多机器人支持

如果需要使用多个机器人，可以修改环境变量名称，例如：
```bash
export FPS_GAMES_BOT_KEY=第一个机器人的key
export OTHER_BOT_KEY=第二个机器人的key
```

然后在代码中读取对应的环境变量。
