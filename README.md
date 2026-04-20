# 🎬 AI分镜师 - 智能分镜生成系统

> 将剧本转化为Seedance 2.0（即梦）视频提示词的AI工作流

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-green.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0-orange.svg)](https://github.com/langchain-ai/langgraph)

## ✨ 功能特性

- 🎬 **导演讲戏**：分析剧本，生成完整的导演工作单
- 👥 **人物设计**：为每个角色生成中英双版文生图提示词
- 🎨 **场景设计**：按镜头设置生成场景提示词
- 📋 **分镜头脚本**：运用电影语法设计镜头序列
- 🎥 **视频提示词**：转化为Seedance 2.0镜头指令
- 🚀 **异步处理**：后台执行任务，无超时限制 ⭐ 推荐
- 📊 **实时进度**：显示任务状态和进度条
- 🌐 **完整部署**：包含前端、后端、云端部署方案

## 🏗️ 系统架构

```
┌─────────────────┐
│   前端页面       │  index_new.html (浏览器)
└────────┬────────┘
         │ HTTP POST
         ↓
┌─────────────────┐
│  后端服务       │  backend/app.py (Flask)
│  - 解决CORS     │
│  - 安全代理     │
└────────┬────────┘
         │ HTTP POST + Bearer Token
         ↓
┌─────────────────┐
│  Coze工作流     │  LangGraph工作流
│  - 导演讲戏     │
│  - 人物设计     │
│  - 场景设计     │
│  - 分镜脚本     │
│  - 视频提示词   │
└─────────────────┘
```

## 📦 项目结构

```
ai-storyboard-workflow/
├── backend/                    # 后端服务
│   ├── app.py                 # Flask应用（解决CORS）
│   ├── task_manager.py        # 异步任务管理器
│   ├── requirements.txt       # Python依赖
│   ├── start.sh              # 启动脚本
│   └── README.md             # 后端文档
├── src/                       # LangGraph工作流
│   ├── graphs/               # 图编排
│   │   ├── graph.py         # 主图
│   │   ├── state.py         # 状态定义
│   │   └── nodes/           # 节点
│   ├── main.py              # 入口文件
│   └── utils/               # 工具函数
├── config/                    # 配置文件
│   └── *_cfg.json           # 节点配置
├── scripts/                   # 脚本
│   ├── http_run.sh          # HTTP服务启动
│   └── setup.sh             # 依赖安装
├── docs/                      # 文档
│   ├── USAGE.md             # 使用指南
│   ├── COZE_DEPLOY.md       # Coze部署指南
│   └── QUICK_DEPLOY.md      # 快速部署指南
├── index.html                # 异步版本前端（推荐）✅
├── index_new.html            # 同步版本前端（备用）
├── index_cozeweb.html        # 旧版前端
├── start_all.sh             # 一键启动脚本
├── DEPLOYMENT_GUIDE.md      # 完整部署指南
├── DEPLOY_ONLINE.md         # 线上部署指南
├── DEPLOY_QUICK.md          # 快速部署指南
├── README.md                # 本文件
├── render.yaml              # Render部署配置
├── Procfile                 # Render启动配置
├── requirements.txt         # Python依赖
└── pyproject.toml           # 项目配置
```

## 🚀 快速开始

### 一键启动（推荐）

```bash
# 在项目根目录运行
cd backend
python3 app.py

# 在浏览器中打开
# index.html（异步版本，推荐）
```

### 推荐使用：异步版本 ✅

**打开 `index.html`（异步版本）**

异步版本特点：
- 🎯 **无超时限制** - 任务在后台执行，HTTP立即返回
- 📊 **实时进度** - 显示进度条、状态、耗时等信息
- 🔄 **可恢复** - 通过task_id查询历史任务
- 🚀 **高并发** - 支持多任务同时执行

**同步版本（index_new.html）**

同步版本保留作为备用，但推荐使用异步版本。

### 手动配置

#### 步骤1：配置API Token

打开 `backend/app.py`，修改第22行：

```python
COZE_API_TOKEN = "你的Coze_API_Token"  # 替换成实际Token
```

#### 步骤2：启动后端

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

#### 步骤3：测试

1. 打开 `index_new.html`
2. 输入剧本内容
3. 点击"生成分镜"

## 🧪 测试验证

### 后端健康检查

```bash
# 检查后端是否正常运行
curl http://localhost:5000/health
# 预期返回: {"status": "ok"}
```

### API接口测试

```bash
# 测试生成接口（格式1：包装格式）
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "script_content": "测试剧本",
      "episode_number": "ep01",
      "visual_style": "写实",
      "project_type": "国内短剧"
    }
  }'

# 测试生成接口（格式2：直接格式）
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "script_content": "测试剧本",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }'
```

### 常见问题解决

#### ❌ 问题：504 GATEWAY TIMEOUT ✅ 已修复
**原因**：工作流执行时间超过超时限制
**解决**：
- 后端超时已优化为10分钟
- 前端超时已优化为15分钟
- 添加了详细的超时提示信息
- 建议简化剧本内容（<500字，<10个场景）
- 详细说明请参考 [TIMEOUT_FIX.md](TIMEOUT_FIX.md)

#### ❌ 问题：400 BAD REQUEST ✅ 已修复
**原因**：请求格式不符合要求
**解决**：
- 后端现已支持两种格式（包装格式和直接格式）
- 确保包含必填字段：`script_content`
- 详细测试说明请参考 [TEST_GUIDE.md](TEST_GUIDE.md)

#### ❌ 问题：Failed to fetch (CORS错误)
**原因**：前端直接调用Coze API被浏览器阻止
**解决**：
- 使用 `index_new.html`（新版前端）而非 `index_cozeweb.html`
- 确保后端服务正在运行：`cd backend && python3 app.py`

#### ❌ 问题：API Token未配置
**原因**：`backend/app.py` 中的 `COZE_API_TOKEN` 未设置
**解决**：
1. 获取Coze API Token（参考 [HOW_TO_FIND_API_URL.md](HOW_TO_FIND_API_URL.md)）
2. 在 `backend/app.py` 中设置：`COZE_API_TOKEN = "你的Token"`
3. 重启后端服务

#### ❌ 问题：API地址404
**原因**：Coze工作流API地址不正确
**解决**：
1. 获取正确的Coze工作流运行地址（参考 [HOW_TO_FIND_API_URL.md](HOW_TO_FIND_API_URL.md)）
2. 在 `backend/app.py` 中更新：`COZE_API_URL = "https://xxx.coze.site/run"`
3. 重启后端服务

更多测试细节和API文档请参考 [TEST_GUIDE.md](TEST_GUIDE.md)

## 🌐 云端部署

### 方式1：本地运行（开发）

一键启动：
```bash
cd backend && python3 app.py
```

### 方式2：线上部署（推荐）

#### ✅ 代码已推送到GitHub

- 仓库地址：https://github.com/Electricity-cub/Electricity-cub-ai-storyboard-workflow
- 分支：main
- 提交：9个本地提交已推送

#### 🚀 快速部署到Render（免费）

**步骤：**

1. **访问 Render**
   - 打开：https://render.com
   - 使用GitHub账号登录

2. **创建Web服务**
   - 点击 "New +" → "Web Service"
   - 连接 `Electricity-cub-ai-storyboard-workflow` 仓库
   - 点击 "Connect"

3. **配置服务**
   - Name: `ai-storyboard-api`
   - Region: Singapore（推荐，国内访问快）
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && python3 app.py`

4. **配置环境变量（重要）**

   点击 "Advanced" → "Add Environment Variable"，添加：

   ```bash
   COZE_API_URL=https://3b7j5mjhsz.coze.site/run
   COZE_API_TOKEN=你的Coze_API_Token
   PORT=5000
   ```

5. **部署**
   - 点击 "Create Web Service"
   - 等待2-3分钟部署完成

6. **获取服务地址**

   部署成功后，你会看到：
   - 服务地址：`https://ai-storyboard-api.onrender.com`
   - 健康检查：`https://ai-storyboard-api.onrender.com/health`

7. **更新前端API地址**

   修改前端文件中的API地址：

   **index_async.html:**
   ```javascript
   const BACKEND_API_URL = 'https://ai-storyboard-api.onrender.com/api/v1/tasks';
   ```

   **index_new.html:**
   ```javascript
   const BACKEND_API_URL = 'https://ai-storyboard-api.onrender.com/run';
   ```

**详细部署指南：** [DEPLOY_ONLINE.md](DEPLOY_ONLINE.md)

### 推荐使用方式

**方式1：异步版本（推荐，无超时问题）**

打开 `index_async.html` 文件，使用异步任务处理，完全解决超时问题。

**方式2：同步版本（兼容，可能超时）**

打开 `index_new.html` 文件，使用传统的同步请求方式。

**说明：**
- 异步版本支持实时进度显示，无超时限制
- 同步版本有20分钟超时限制，复杂剧本可能超时
- 详细说明请参考 [ASYNC_SOLUTION.md](ASYNC_SOLUTION.md)

### 一键启动

```bash
# 启动后端服务
cd backend && python3 app.py

# 在浏览器中打开
# index_async.html（推荐）
# 或 index_new.html（兼容）
```

### Vercel部署（推荐）

详细步骤请查看 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

```bash
# 1. 推送代码到GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git
git push -u origin main

# 2. 在Vercel部署后端
# 访问 https://vercel.com，创建新项目

# 3. 配置环境变量
# COZE_API_TOKEN = 你的Token

# 4. 更新前端API地址
# 修改 index_new.html 中的 BACKEND_API_URL
```

### 其他平台

- [Railway](https://railway.app)
- [Render](https://render.com)
- [Heroku](https://heroku.com)

详细配置请查看 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📖 使用指南

### 本地测试

```bash
# 启动后端服务
./start_all.sh

# 在浏览器中打开 index_new.html
```

### API调用

```bash
curl -X POST http://localhost:5000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "script_content": "小明和小红在公园相遇",
      "episode_number": "ep01",
      "visual_style": "写实",
      "project_type": "国内短剧"
    }
  }'
```

### Python调用

```python
import requests

response = requests.post(
    'http://localhost:5000/api/v1/generate',
    json={
        'input': {
            'script_content': '你的剧本内容',
            'episode_number': 'ep01',
            'visual_style': '写实',
            'project_type': '国内短剧'
        }
    }
)

print(response.json())
```

## 🐛 常见问题

### 问题1：Failed to fetch

**原因**：CORS跨域问题

**解决方案**：使用后端服务（`backend/app.py`）代理请求

### 问题2：连接失败

**原因**：后端服务未启动

**解决方案**：
```bash
cd backend
./start.sh
```

### 问题3：API Token未配置

**解决方案**：修改 `backend/app.py` 第22行

更多问题请查看 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 🔒 安全建议

- ✅ Token存储在后端，不暴露在前端
- ✅ 使用环境变量配置敏感信息
- ✅ 部署到支持HTTPS的平台
- ✅ 添加访问限制（可选）

## 📚 文档

- 📖 [完整部署指南](DEPLOYMENT_GUIDE.md) - 详细的部署步骤
- 📖 [快速部署指南](QUICK_DEPLOY.md) - 5分钟快速部署
- 📖 [使用指南](docs/USAGE.md) - 详细使用说明
- 📖 [Coze部署](docs/COZE_DEPLOY.md) - Coze平台部署
- 📖 [后端文档](backend/README.md) - 后端服务说明

## 🎯 核心特性

### 1. 解决CORS问题

使用Flask后端服务代理请求，避免浏览器的跨域限制。

### 2. 安全的Token管理

API Token存储在后端环境变量中，不会暴露给前端。

### 3. 并行处理

人物、场景、分镜头脚本三个节点并行执行，提升效率。

### 4. 完整的工作流

从剧本到Seedance视频提示词的全流程自动化。

## 📊 技术栈

- **工作流**: LangGraph 1.0
- **语言**: Python 3.12
- **后端**: Flask + Flask-CORS
- **前端**: HTML + JavaScript
- **AI模型**: doubao-seed-2-0-pro-260215
- **部署**: Vercel / Railway / Render

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 许可证

MIT License

## 🎉 致谢

- [LangGraph](https://github.com/langchain-ai/langgraph) - 强大的工作流框架
- [Coze](https://www.coze.com/) - AI应用开发平台
- [Flask](https://flask.palletsprojects.com/) - 轻量级Web框架

---

**祝你使用愉快！** 🚀

如有问题，请查看文档或提交Issue。
