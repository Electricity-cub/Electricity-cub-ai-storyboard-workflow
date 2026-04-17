# 🚀 AI分镜师 - 完整部署指南

## 📋 概述

本指南将帮助你从零开始部署AI分镜师工作流，解决CORS跨域问题，实现从前端到后端再到Coze工作流的完整调用链路。

## 🔧 架构说明

```
┌─────────────────┐
│   index_new.html │  ← 前端页面（浏览器）
└────────┬────────┘
         │ HTTP POST
         ↓
┌─────────────────┐
│  backend/app.py │  ← 后端服务（Flask）解决CORS
└────────┬────────┘
         │ HTTP POST + Bearer Token
         ↓
┌─────────────────┐
│   Coze Workflow │  ← AI工作流
└─────────────────┘
```

## 📦 项目结构

```
ai-storyboard-workflow/
├── backend/                  # 后端服务
│   ├── app.py               # Flask应用
│   ├── requirements.txt     # Python依赖
│   ├── start.sh            # 启动脚本
│   ├── README.md           # 后端文档
│   └── venv/               # 虚拟环境（自动创建）
├── index_new.html          # 前端页面（使用后端服务）
├── index_cozeweb.html      # 旧版前端（直接调用Coze，会有CORS问题）
└── DEPLOYMENT_GUIDE.md     # 本文档
```

## 🎯 快速开始（本地运行）

### 步骤1：配置后端服务

1. 打开 `backend/app.py` 文件
2. 找到第22行：
   ```python
   COZE_API_TOKEN = "你的Coze_API_Token"
   ```
3. 将 `"你的Coze_API_Token"` 替换成你实际的Coze API Token

### 步骤2：启动后端服务

```bash
# 进入后端目录
cd backend

# 方式1：使用启动脚本（推荐）
./start.sh

# 方式2：手动启动
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

启动成功后，你会看到：
```
=========================================
🚀 启动后端服务...
=========================================

服务地址: http://localhost:5000
健康检查: http://localhost:5000/health
API接口: http://localhost:5000/api/v1/generate

按 Ctrl+C 停止服务
```

### 步骤3：打开前端页面

1. 在浏览器中打开 `index_new.html` 文件
2. 输入剧本内容
3. 点击"生成分镜"
4. 等待结果返回

## 🌐 云端部署

### 方案1：部署到 Vercel（推荐）

#### 部署后端服务

1. **准备GitHub仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"

   # 创建GitHub仓库并关联
   git remote add origin https://github.com/YOUR_USERNAME/ai-storyboard-backend.git
   git branch -M main
   git push -u origin main
   ```

2. **部署到Vercel**
   - 访问 https://vercel.com
   - 登录GitHub账号
   - 点击 "Add New" → "Project"
   - 选择你的仓库
   - 配置项目：
     - **Framework Preset**: Python
     - **Root Directory**: `backend`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `python app.py`
   - 点击 "Deploy"

3. **配置环境变量**
   - 部署完成后，进入项目设置
   - 找到 "Environment Variables"
   - 添加：
     - Name: `COZE_API_TOKEN`
     - Value: 你的Coze API Token
   - 重新部署

4. **获取API地址**
   - 部署成功后，Vercel会提供域名
   - 例如：`https://your-app.vercel.app/api/v1/generate`

#### 更新前端页面

1. 打开 `index_new.html`
2. 修改第279行的API地址：
   ```javascript
   const BACKEND_API_URL = "https://your-app.vercel.app/api/v1/generate";
   ```

#### 部署前端页面

1. 将 `index_new.html` 上传到GitHub或任何静态托管服务
2. 例如：GitHub Pages、Netlify、Vercel

### 方案2：部署到 Railway

1. 访问 https://railway.app
2. 点击 "New Project" → "Deploy from GitHub repo"
3. 选择你的仓库
4. 配置：
   - Root Directory: `backend`
5. 设置环境变量 `COZE_API_TOKEN`
6. 部署完成

### 方案3：部署到 Render

1. 访问 https://render.com
2. 点击 "New" → "Web Service"
3. 连接GitHub仓库
4. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Root Directory: `backend`
5. 设置环境变量 `COZE_API_TOKEN`
6. 部署完成

## 🔍 测试验证

### 1. 测试后端健康检查

```bash
curl http://localhost:5000/health
```

期望输出：
```json
{
  "status": "healthy",
  "service": "AI Storyboard Proxy"
}
```

### 2. 测试生成API

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

### 3. 测试前端页面

1. 打开 `index_new.html`
2. 输入剧本内容
3. 点击"生成分镜"
4. 查看结果

## 🐛 常见问题

### 问题1：Failed to fetch（CORS错误）

**原因**：直接从HTML调用Coze API，跨域被阻止。

**解决方案**：
1. 使用后端服务（Flask）代理请求
2. 后端已配置CORS，允许跨域调用

### 问题2：连接失败：无法连接到后端服务

**原因**：后端服务未启动。

**解决方案**：
```bash
cd backend
./start.sh
```

### 问题3：API Token未配置

**原因**：后端服务中Token未配置。

**解决方案**：
1. 打开 `backend/app.py`
2. 找到第22行
3. 替换Token
4. 重启服务

### 问题4：端口被占用

**原因**：5000端口已被其他应用占用。

**解决方案**：
修改 `backend/app.py` 最后一行：
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

同时修改 `index_new.html` 第279行：
```javascript
const BACKEND_API_URL = "http://localhost:5001/api/v1/generate";
```

### 问题5：依赖安装失败

**解决方案**：
```bash
# 升级pip
pip install --upgrade pip

# 重新安装依赖
cd backend
pip install -r requirements.txt
```

## 🔒 安全建议

### 1. 不要在前端暴露Token

❌ 错误做法：
```javascript
const API_TOKEN = "你的Token"; // 暴露在前端
```

✅ 正确做法：
- Token配置在后端（`backend/app.py`）
- 前端通过后端代理调用API

### 2. 使用环境变量

修改 `backend/app.py`：
```python
import os
COZE_API_TOKEN = os.environ.get('COZE_API_TOKEN', '')
```

部署时设置环境变量：
- Vercel: Project Settings → Environment Variables
- Railway: Variables tab
- Render: Environment section

### 3. 添加访问限制（可选）

```python
# 在backend/app.py中添加
from flask import request

@app.before_request
def limit_remote_addr():
    # 只允许特定IP访问
    allowed_ips = ['127.0.0.1', 'your-frontend-ip']
    if request.remote_addr not in allowed_ips:
        return jsonify({'error': 'Access denied'}), 403
```

### 4. 使用HTTPS

部署时确保使用HTTPS：
- Vercel自动提供HTTPS
- Railway自动提供HTTPS
- Render自动提供HTTPS

## 📊 性能优化

### 1. 添加缓存

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/v1/generate', methods=['POST'])
@cache.cached(timeout=300, key_prefix=lambda: request.json)
def generate_storyboard():
    # ...
```

### 2. 异步处理

```python
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(2)

def generate_storyboard():
    def process_request():
        # 处理请求
        pass

    executor.submit(process_request)
```

## 📝 总结

### ✅ 推荐架构

```
前端 → 后端代理 → Coze API
```

### ✅ 部署流程

1. 本地测试 → 2. 部署后端 → 3. 更新前端 → 4. 部署前端

### ✅ 关键点

- 后端解决CORS问题
- Token安全存储在后端
- 使用环境变量配置敏感信息
- 部署到支持HTTPS的平台

## 🆘 获取帮助

- 📚 [Flask文档](https://flask.palletsprojects.com/)
- 📚 [Coze API文档](https://www.coze.com/docs)
- 📚 [Vercel文档](https://vercel.com/docs)
- 💬 如有问题，请查看项目README或提交Issue

---

**祝你部署顺利！** 🎉
