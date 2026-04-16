# 🎯 立即开始部署

## 当前状态
✅ 代码已完成并提交
✅ 部署文档齐全
✅ 自动化脚本已准备
❌ **待完成：推送到远程仓库**
❌ **待完成：在Coze平台部署**

---

## 🚀 两种部署方案

### 方案A：使用自动化脚本（推荐，最简单）

```bash
# 运行自动化部署脚本
bash auto_deploy.sh
```

脚本会引导你完成：
1. ✅ 检查Git仓库状态
2. 🔧 配置远程仓库（交互式选择GitHub/GitLab/Gitee）
3. 📤 推送代码到远程仓库
4. ⚙️ 生成部署配置
5. 📝 提供下一步操作指南

---

### 方案B：手动部署（完全控制）

#### 步骤1：创建GitHub仓库（1分钟）
```
1. 访问 https://github.com/new
2. 仓库名：ai-storyboard-workflow
3. 设为公开或私有
4. 不要初始化README
5. 点击"Create repository"
```

#### 步骤2：配置并推送（1分钟）
```bash
# 将YOUR_USERNAME替换为你的GitHub用户名
git remote add origin https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git
git branch -M main
git push -u origin main
```

如果需要Token：
```
1. 访问 https://github.com/settings/tokens
2. 创建Token，勾选repo权限
3. 使用：https://YOUR_TOKEN@github.com/YOUR_USERNAME/ai-storyboard-workflow.git
```

#### 步骤3：在Coze平台创建应用（2分钟）
```
1. 访问 https://www.coze.com/
2. 点击"创建应用" → "工作流"
3. 应用名称：AI分镜师工作流
4. 点击"创建"
```

#### 步骤4：关联Git仓库（1分钟）
```
1. 进入应用设置
2. 找到"代码管理"或"Git集成"
3. 点击"关联仓库"
4. 选择GitHub
5. 选择仓库：ai-storyboard-workflow
6. 选择分支：main
7. 点击"确认关联"
```

#### 步骤5：配置部署参数（1分钟）
```
构建命令：bash scripts/setup.sh
运行命令：bash scripts/http_run.sh -p 5000
```

#### 步骤6：触发部署（3-5分钟）
```
1. 点击"部署"按钮
2. 选择分支：main
3. 点击"开始部署"
4. 等待部署完成
```

#### 步骤7：验证部署（2分钟）
```bash
# 健康检查
curl https://your-app.coze.run/health

# API测试
curl -X POST https://your-app.coze.run/api/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "script_content": "小明和小红在公园相遇，一见钟情。",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }'
```

---

## 📚 详细文档

- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) - 🚀 5分钟快速部署
- [DEPLOY_CHECKLIST.md](DEPLOY_CHECKLIST.md) - 📋 详细步骤清单
- [COZE_DEPLOY.md](COZE_DEPLOY.md) - 📚 完整部署文档
- [USAGE.md](USAGE.md) - 📖 使用指南

---

## ⏱️ 时间估算

- 方案A（自动化）：10-15分钟
- 方案B（手动）：10-15分钟

---

## ❓ 需要帮助？

### 推送代码失败
```bash
# 检查远程仓库
git remote -v

# 重新配置
git remote set-url origin <正确的URL>

# 或使用Token
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/repo.git
```

### 部署失败
- 查看Coze平台的部署日志
- 检查构建命令和运行命令
- 确认依赖安装成功

### API调用失败
- 检查API地址是否正确
- 查看工作流执行日志
- 确认请求参数格式

---

## 🎉 准备好了吗？

**选择方案并开始部署！**

推荐使用方案A（自动化脚本）：
```bash
bash auto_deploy.sh
```

或选择方案B（手动部署），按步骤执行。

---

**需要帮助？查看详细文档：**
- [快速部署](QUICK_DEPLOY.md)
- [步骤清单](DEPLOY_CHECKLIST.md)
- [完整文档](COZE_DEPLOY.md)
