# 📋 部署步骤清单

## 当前状态
- ✅ 代码开发完成
- ✅ 本地测试通过
- ✅ Git提交完成
- ✅ 部署文档齐全
- ❌ **待完成：推送到远程仓库**
- ❌ **待完成：在Coze平台创建应用**
- ❌ **待完成：触发部署**

---

## 🚀 立即开始部署（选择一个方案）

### 方案A：GitHub部署（推荐，国际通用）

```bash
# 1. 创建GitHub仓库
# 访问：https://github.com/new
# 仓库名：ai-storyboard-workflow
# 公开或私有：按需选择
# 不要初始化README

# 2. 配置远程仓库（将YOUR_USERNAME替换为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git
git branch -M main
git push -u origin main

# 3. 如果需要Token，访问：https://github.com/settings/tokens
# 创建Token，勾选repo权限，然后使用：
# git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/ai-storyboard-workflow.git
```

### 方案B：Gitee部署（国内访问快）

```bash
# 1. 创建Gitee仓库
# 访问：https://gitee.com/projects/new
# 仓库名：ai-storyboard-workflow

# 2. 配置远程仓库（将YOUR_USERNAME替换为你的Gitee用户名）
git remote add origin https://gitee.com/YOUR_USERNAME/ai-storyboard-workflow.git
git branch -M main
git push -u origin main
```

### 方案C：使用自动化脚本

```bash
# 运行自动化部署脚本（交互式）
bash auto_deploy.sh
```

---

## 📤 步骤1：推送代码到远程仓库

**检查当前状态：**
```bash
# 查看远程仓库配置
git remote -v

# 查看当前分支
git branch

# 查看最近3次提交
git log --oneline -3
```

**配置并推送：**
```bash
# 添加远程仓库（选择一个）
git remote add origin <你的仓库URL>

# 推送到远程
git branch -M main
git push -u origin main
```

---

## 🏗️ 步骤2：在Coze平台创建应用

1. **访问Coze平台**
   - 登录：https://www.coze.com/

2. **创建工作流应用**
   - 点击"创建应用"
   - 选择"工作流"类型
   - 应用名称：`AI分镜师工作流`
   - 描述：`将剧本转化为Seedance 2.0视频提示词`
   - 点击"创建"

3. **关联Git仓库**
   - 进入应用设置
   - 找到"代码管理"或"Git集成"
   - 点击"关联仓库"
   - 选择你的Git平台
   - 选择仓库：`ai-storyboard-workflow`
   - 选择分支：`main`
   - 点击"确认关联"

---

## ⚙️ 步骤3：配置部署参数

**基础配置：**
- **构建命令：** `bash scripts/setup.sh`
- **运行命令：** `bash scripts/http_run.sh -p 5000`

**环境变量（可选）：**
```
PORT=5000
LOG_LEVEL=INFO
```

**其他配置：**
- 入口文件：`src/main.py`
- 运行环境：Python 3.12

---

## 🚀 步骤4：触发部署

1. 点击"部署"按钮
2. 选择分支：`main`
3. 点击"开始部署"
4. 等待部署完成（3-5分钟）
5. 查看部署日志

---

## ✅ 步骤5：验证部署

**健康检查：**
```bash
curl https://your-app.coze.run/health
```

**API测试：**
```bash
curl -X POST https://your-app.coze.run/api/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "script_content": "小明和小红在公园相遇，一见钟情。",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }'
```

**在线测试：**
- 访问Coze提供的在线测试页面
- 直接在浏览器中测试工作流

---

## 📚 参考文档

| 文档 | 说明 |
|------|------|
| [QUICK_DEPLOY.md](QUICK_DEPLOY.md) | 🚀 快速部署指南（5分钟） |
| [COZE_DEPLOY.md](COZE_DEPLOY.md) | 📚 完整部署文档 |
| [USAGE.md](USAGE.md) | 📖 使用指南 |
| [README.md](README.md) | 📖 项目介绍 |
| [AGENTS.md](AGENTS.md) | 📋 工作流结构说明 |

---

## 🔧 辅助脚本

```bash
# 部署前检查
bash pre_deploy_check.sh

# 自动化部署（交互式）
bash auto_deploy.sh

# 工作流测试
bash test_workflow.sh
```

---

## ⏱️ 时间估算

- 推送代码：2-3分钟
- 创建Coze应用：1-2分钟
- 配置部署：1分钟
- 触发部署：3-5分钟
- 验证部署：2分钟

**总计：约10-15分钟**

---

## ❓ 常见问题

### Q: 推送代码失败
**A:** 检查仓库URL是否正确，或配置GitHub Token/SSH密钥

### Q: 部署时依赖安装失败
**A:** 查看部署日志，检查pyproject.toml配置

### Q: 应用启动失败
**A:** 查看Coze部署日志，检查入口文件和运行命令

### Q: API调用超时
**A:** 检查网络连接，增加超时时间，查看工作流执行日志

---

## 📞 需要帮助？

1. 查看详细文档
2. 运行部署检查脚本
3. 查看部署日志
4. 联系技术支持

---

## ✨ 下一步

部署成功后，你可以：

1. **集成到其他应用**
   - 通过API调用
   - 集成到前端应用
   - 接入到Chatbot

2. **扩展功能**
   - 添加新节点
   - 优化提示词
   - 集成其他AI能力

3. **优化性能**
   - 缓存策略
   - 异步处理
   - 并行优化

---

**准备好开始了吗？选择一个方案，开始你的部署之旅！🚀**
