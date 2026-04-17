# AI分镜师 - 后端代理服务

## 📋 说明

这是一个Flask后端服务，用于解决前端调用Coze API时的CORS（跨域）问题。

## 🚀 快速开始

### 方法1：使用启动脚本（推荐）

```bash
cd backend
./start.sh
```

### 方法2：手动启动

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动服务
python app.py
```

### 方法3：使用 pipenv

```bash
cd backend

# 安装依赖
pipenv install

# 启动服务
pipenv run python app.py
```

## ⚙️ 配置

在 `app.py` 中修改以下配置：

```python
# Coze API配置
COZE_API_URL = "https://3b7j5mjhsz.coze.site/workflow_run"
COZE_API_TOKEN = "你的Coze_API_Token"  # 替换成你的实际Token
```

## 📡 API接口

### 1. 健康检查

**请求：**
```bash
GET http://localhost:5000/health
```

**响应：**
```json
{
  "status": "healthy",
  "service": "AI Storyboard Proxy"
}
```

### 2. 生成分镜

**请求：**
```bash
POST http://localhost:5000/api/v1/generate
Content-Type: application/json

{
  "input": {
    "script_content": "你的剧本内容",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }
}
```

**响应：**
```json
{
  // Coze API返回的结果
}
```

## 🔧 前端配置

修改 `index_cozeweb.html` 中的JavaScript代码：

```javascript
// 修改API地址为本地后端服务
const COZE_API_URL = "http://localhost:5000/api/v1/generate";
const API_TOKEN = "";  // 后端服务不需要在前端配置Token
```

## 🌐 部署到云端

### Vercel部署

1. 将 `backend/` 目录上传到GitHub
2. 访问 https://vercel.com
3. 创建新项目，选择你的仓库
4. 配置构建命令：
   ```bash
   cd backend && pip install -r requirements.txt
   ```
5. 配置启动命令：
   ```bash
   cd backend && python app.py
   ```
6. 设置环境变量 `COZE_API_TOKEN`
7. 部署完成后，获取你的域名

### Railway部署

1. 访问 https://railway.app
2. 创建新项目
3. 选择"Deploy from GitHub repo"
4. 选择你的仓库
5. 配置环境变量 `COZE_API_TOKEN`
6. 部署完成

### Render部署

1. 访问 https://render.com
2. 创建新的Web Service
3. 连接GitHub仓库
4. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. 设置环境变量 `COZE_API_TOKEN`
6. 部署完成

## 🔒 安全建议

1. **不要将API Token提交到Git**
   ```bash
   echo "backend/app.py" >> .gitignore
   echo "backend/venv/" >> .gitignore
   echo "backend/__pycache__/" >> .gitignore
   ```

2. **使用环境变量**
   ```python
   import os
   COZE_API_TOKEN = os.environ.get('COZE_API_TOKEN', '')
   ```

3. **添加访问限制**
   - 使用API Key验证前端请求
   - 添加Rate Limiting
   - 使用HTTPS

## 🐛 故障排查

### 问题1：端口被占用
```bash
# 修改app.py中的端口号
app.run(host='0.0.0.0', port=5001, debug=True)
```

### 问题2：依赖安装失败
```bash
# 升级pip
pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt
```

### 问题3：CORS问题
```bash
# 已在app.py中配置CORS，应该不会出现此问题
# 如果仍有问题，检查flask-cors是否正确安装
pip list | grep flask-cors
```

## 📚 相关文档

- [Flask官方文档](https://flask.palletsprojects.com/)
- [Flask-CORS文档](https://flask-cors.readthedocs.io/)
- [Coze API文档](https://www.coze.com/docs)

## 📝 许可证

MIT License
