# 🚀 一键部署到Coze

## 快速开始（5分钟部署）

### 前置条件
✅ 已完成代码开发和本地测试
✅ 已安装Git
✅ 拥有GitHub/GitLab/Gitee账户
✅ 拥有Coze平台账户

---

## 第1步：推送代码到远程仓库（3分钟）

### 方案A：使用GitHub（推荐）

1. **创建GitHub仓库**
   ```bash
   # 访问 https://github.com/new
   # 仓库名：ai-storyboard-workflow
   # 设为公开或私有
   # 不要初始化README
   ```

2. **配置并推送**
   ```bash
   # 将 YOUR_USERNAME 替换为你的GitHub用户名
   git remote add origin https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git
   git branch -M main
   git push -u origin main
   ```

3. **如果需要认证**
   - 方式1：使用GitHub Token（推荐）
     - 访问 https://github.com/settings/tokens
     - 创建新Token，勾选 repo 权限
     - 推送时使用：`https://YOUR_TOKEN@github.com/YOUR_USERNAME/ai-storyboard-workflow.git`
   - 方式2：使用SSH密钥
     - 生成SSH密钥：`ssh-keygen -t rsa -b 4096`
     - 添加到GitHub：Settings → SSH and GPG keys

### 方案B：使用Gitee（国内用户首选）

1. **创建Gitee仓库**
   ```bash
   # 访问 https://gitee.com/projects/new
   # 仓库名：ai-storyboard-workflow
   # 设为公开或私有
   ```

2. **配置并推送**
   ```bash
   git remote add origin https://gitee.com/YOUR_USERNAME/ai-storyboard-workflow.git
   git branch -M main
   git push -u origin main
   ```

### 方案C：使用GitLab（企业用户）

1. **创建GitLab仓库**
   ```bash
   # 访问 https://gitlab.com/projects/new
   # 仓库名：ai-storyboard-workflow
   ```

2. **配置并推送**
   ```bash
   git remote add origin https://gitlab.com/YOUR_USERNAME/ai-storyboard-workflow.git
   git branch -M main
   git push -u origin main
   ```

---

## 第2步：在Coze平台创建应用（2分钟）

1. **登录Coze平台**
   - 访问 https://www.coze.com/

2. **创建工作流应用**
   - 点击"创建应用"
   - 选择"工作流"类型
   - 应用名称：`AI分镜师工作流`
   - 描述：`将剧本转化为Seedance 2.0视频提示词的自动化工作流`
   - 点击"创建"

---

## 第3步：关联Git仓库（1分钟）

1. **进入应用设置**
   - 点击应用进入工作台
   - 点击右上角"设置"图标

2. **关联仓库**
   - 找到"代码管理"或"Git集成"
   - 点击"关联仓库"
   - 选择你的Git平台（GitHub/GitLab/Gitee）
   - 选择仓库：`ai-storyboard-workflow`
   - 选择分支：`main`
   - 点击"确认关联"

---

## 第4步：配置部署参数（1分钟）

### 基础配置

**构建命令：**
```bash
bash scripts/setup.sh
```

**运行命令：**
```bash
bash scripts/http_run.sh -p 5000
```

### 环境变量（可选）

```bash
PORT=5000
LOG_LEVEL=INFO
```

### 其他配置

- **入口文件**：`src/main.py`
- **运行环境**：Python 3.12
- **工作目录**：/workspace/projects

---

## 第5步：触发部署（3-5分钟）

1. **开始部署**
   - 点击"部署"按钮
   - 选择分支：`main`
   - 点击"开始部署"

2. **等待部署完成**
   - 查看部署日志
   - 等待所有步骤完成（依赖安装、构建、启动）

3. **部署成功**
   - 显示"部署成功"状态
   - 获取API地址
   - 获取在线测试页面链接

---

## 第6步：验证部署（2分钟）

### 1. 健康检查

```bash
curl https://your-app.coze.run/health
```

期望输出：
```json
{
  "status": "healthy",
  "service": "AI Storyboard Workflow"
}
```

### 2. API测试

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

### 3. 在线测试

访问Coze提供的在线测试页面，直接在浏览器中测试工作流。

---

## 常见问题解决

### 问题1：推送代码失败

**错误信息：** `Permission denied`

**解决方案：**
1. 检查仓库URL是否正确
2. 配置GitHub Token：`git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/repo.git`
3. 或配置SSH密钥

### 问题2：部署时依赖安装失败

**错误信息：** `ModuleNotFoundError` 或 `pip install failed`

**解决方案：**
1. 检查 `pyproject.toml` 中的依赖配置
2. 查看部署日志中的具体错误信息
3. 确保所有依赖都已正确配置

### 问题3：应用启动失败

**错误信息：** `Application startup failed`

**解决方案：**
1. 查看Coze平台的部署日志
2. 检查入口文件 `src/main.py` 是否存在
3. 检查运行命令是否正确

### 问题4：API调用超时

**错误信息：** `Request timeout`

**解决方案：**
1. 检查网络连接
2. 增加超时时间
3. 查看工作流执行日志

---

## 部署后的操作

### 1. 查看日志

在Coze平台查看实时日志：
- 部署日志：构建和启动过程
- 运行日志：API调用和工作流执行

### 2. 监控性能

- 访问量统计
- 响应时间
- 错误率

### 3. 版本管理

- 每次代码更新后推送新提交
- 在Coze平台触发新部署
- 支持回滚到历史版本

---

## 自动化部署脚本

如果你想要自动化执行上述步骤，可以使用我们提供的脚本：

```bash
# 运行自动化部署脚本
bash auto_deploy.sh
```

该脚本会：
1. ✅ 检查Git仓库状态
2. 🔧 配置远程仓库（交互式）
3. 📤 推送代码到远程仓库
4. ⚙️ 生成部署配置文件
5. 📝 生成部署文档
6. 🚀 提供下一步操作指南

---

## 下一步

部署成功后，你可以：

1. **集成到其他应用**
   - 通过API调用
   - 集成到你的前端应用
   - 接入到Chatbot

2. **扩展功能**
   - 添加新的节点
   - 优化提示词
   - 集成其他AI能力

3. **优化性能**
   - 缓存策略
   - 异步处理
   - 并行优化

---

## 需要帮助？

- 📚 完整文档：`COZE_DEPLOY.md`
- 📖 使用指南：`USAGE.md`
- 📖 项目介绍：`README.md`
- 🧪 测试脚本：`test_workflow.sh`

---

## 部署检查清单

- [ ] 代码已推送到远程仓库
- [ ] 远程仓库分支为main
- [ ] 在Coze平台创建了应用
- [ ] 成功关联Git仓库
- [ ] 配置了正确的构建命令
- [ ] 配置了正确的运行命令
- [ ] 触发部署并成功完成
- [ ] 健康检查通过
- [ ] API测试成功
- [ ] 文档齐全

---

**部署时间：约10-15分钟** | **难度：⭐⭐☆☆☆**

🎉 **恭喜！你已成功将AI分镜师工作流部署到Coze平台！**
