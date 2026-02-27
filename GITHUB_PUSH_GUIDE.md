# 推送到GitHub的快速脚本

## 使用方法

### 1. 复制本文件到项目根目录
```bash
cp GITHUB_PUSH_GUIDE.md PUSH_TO_GITHUB.sh
```

### 2. 修改脚本中的仓库地址

编辑 `PUSH_TO_GITHUB.sh`，修改以下内容：
```bash
REPO_URL="https://github.com/你的用户名/你的仓库名.git"
```

### 3. 给脚本添加执行权限
```bash
chmod +x PUSH_TO_GITHUB.sh
```

### 4. 运行脚本
```bash
./PUSH_TO_GITHUB.sh
```

---

## 手动推送到GitHub（如果不使用脚本）

### 方式1：首次推送

```bash
# 初始化git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Add FPS games daily push workflow with GitHub Actions"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

### 方式2：已有仓库，添加新文件

```bash
# 添加新文件
git add .github/workflows/
git add GITHUB_ACTIONS_SETUP.md

# 提交
git commit -m "Add GitHub Actions workflow for daily FPS games push"

# 推送
git push
```

---

## 推送后的步骤

### 1. 确认文件已上传

访问你的GitHub仓库，确认可以看到：
- ✅ `.github/workflows/fps-games-daily.yml` 文件
- ✅ `GITHUB_ACTIONS_SETUP.md` 文件

### 2. 配置Secrets

按照 `GITHUB_ACTIONS_SETUP.md` 文档中的第二步操作。

### 3. 测试工作流

1. 进入GitHub仓库的 **Actions** 页面
2. 选择 **FPS Games Daily Push**
3. 点击 **Run workflow** 进行手动测试

### 4. 确认收到消息

查看钉钉群是否收到了测试消息。

---

## 常见问题

### Q1: 推送失败，提示"Repository not found"

**A**: 检查：
1. 仓库地址是否正确
2. 是否有该仓库的写入权限
3. 仓库是否存在

### Q2: 提示"Authentication failed"

**A**: 需要配置GitHub认证：
```bash
# 使用Personal Access Token
git remote set-url origin https://你的token@github.com/你的用户名/你的仓库名.git
```

### Q3: Actions页面找不到工作流

**A**: 检查：
1. 文件路径是否正确：`.github/workflows/fps-games-daily.yml`
2. 文件是否成功推送到GitHub
3. 等待1-2分钟，GitHub可能需要时间同步

---

## 更新代码后重新推送

```bash
# 添加修改的文件
git add .

# 提交
git commit -m "Update workflow"

# 推送
git push
```

GitHub Actions会自动检测到新的提交，但不会立即执行定时任务（等待到下一个定时点）。
如需立即测试，使用手动触发功能。
