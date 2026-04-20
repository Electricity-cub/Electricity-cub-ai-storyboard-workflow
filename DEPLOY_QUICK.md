# 🎉 线上部署快速开始

## ✅ 第一步已完成：代码已推送到GitHub

**仓库地址：** https://github.com/Electricity-cub/Electricity-cub-ai-storyboard-workflow

**包含文件：**
- ✅ 后端服务代码
- ✅ 前端页面（异步版 + 同步版）
- ✅ Render部署配置
- ✅ 详细部署指南

---

## 🚀 第二步：部署到Render（免费）

### 1. 访问 Render

打开：https://render.com

### 2. 注册/登录

使用GitHub账号登录（推荐）

### 3. 创建Web服务

1. 点击右上角 "New +"
2. 选择 "Web Service"
3. 在 "Connect a repository" 中搜索并选择：
   - `Electricity-cub/Electricity-cub-ai-storyboard-workflow`
4. 点击 "Connect"

### 4. 基础配置

填写以下信息：

```
Name: ai-storyboard-api
Region: Singapore（推荐，国内访问快）
Branch: main
Runtime: Python 3
```

### 5. 构建配置

```
Build Command: pip install -r requirements.txt
Start Command: cd backend && python3 app.py
```

### 6. 配置环境变量（重要！）

点击 "Advanced" → "Add Environment Variable"，添加3个变量：

**变量1：COZE_API_URL**
```
Key: COZE_API_URL
Value: https://3b7j5mjhsz.coze.site/run
```

**变量2：COZE_API_TOKEN**
```
Key: COZE_API_TOKEN
Value: 你的Coze_API_Token（获取方式见下方）
```

**变量3：PORT**
```
Key: PORT
Value: 5000
```

### 7. 获取Coze API Token

1. 登录 Coze 平台
2. 找到你的工作流
3. 获取 API Token
4. 复制到环境变量 `COZE_API_TOKEN` 中

### 8. 创建服务

点击底部的 "Create Web Service" 按钮

等待2-3分钟，服务部署完成

---

## ✅ 第三步：获取服务地址

部署成功后，你会看到：

**服务地址：**
```
https://ai-storyboard-api.onrender.com
```

**健康检查地址：**
```
https://ai-storyboard-api.onrender.com/health
```

**API接口地址：**
```
https://ai-storyboard-api.onrender.com/api/v1/tasks
https://ai-storyboard-api.onrender.com/run
```

---

## 🔧 第四步：更新前端API地址

修改前端页面中的API地址：

### 修改 index.html（异步版本，推荐）

找到这一行（约第255行）：
```javascript
const BACKEND_API_URL = 'http://localhost:5000/api/v1/tasks';
```

改为：
```javascript
const BACKEND_API_URL = 'https://ai-storyboard-api.onrender.com/api/v1/tasks';
```

### 修改 index_new.html（同步版本，备用）

找到这一行（约第280行）：
```javascript
const BACKEND_API_URL = 'http://localhost:5000/run';
```

改为：
```javascript
const BACKEND_API_URL = 'https://ai-storyboard-api.onrender.com/run';
```

---

## 🧪 第五步：测试部署

### 测试1：健康检查

在浏览器或命令行中访问：
```
https://ai-storyboard-api.onrender.com/health
```

**预期返回：**
```json
{
  "status": "healthy",
  "service": "AI Storyboard Proxy",
  "active_tasks": 0
}
```

### 测试2：使用前端

1. 在浏览器中打开 `index.html`（异步版本，推荐）
2. 输入剧本内容：
   ```
   小明和小红在公园相遇，一见钟情。
   ```
3. 点击"生成分镜（异步）"
4. 查看实时进度
5. 等待结果

---

## 🎉 部署完成！

恭喜！你的AI分镜师工作流已经成功部署到线上！

### 线上服务地址

- **后端API：** https://ai-storyboard-api.onrender.com
- **健康检查：** https://ai-storyboard-api.onrender.com/health
- **API文档：** https://ai-storyboard-api.onrender.com/api/v1/tasks

### 前端页面

- **异步版本：** index.html（推荐）✅
- **同步版本：** index_new.html（备用）

### 使用方法

1. 打开 `index.html`（异步版本，推荐）
2. 输入剧本内容
3. 点击"生成分镜"
4. 查看实时进度和结果

---

## 📱 分享给他人

### 方式1：直接分享HTML文件

1. 修改前端API地址为线上地址
2. 将 `index_async.html` 发送给他人
3. 对方打开即可使用

### 方式2：部署前端到GitHub Pages

1. 创建 `docs/` 目录
2. 将 `index_async.html` 移动到 `docs/`
3. 在GitHub仓库设置中启用GitHub Pages
4. 访问：`https://你的用户名.github.io/Electricity-cub-ai-storyboard-workflow/`

---

## 💡 常见问题

### Q1: 部署失败

**原因：** 环境变量未配置

**解决：**
1. 检查 `COZE_API_TOKEN` 是否正确
2. 查看Render日志，定位错误
3. 重新部署

### Q2: 首次访问慢

**原因：** Render免费版有冷启动时间（30-60秒）

**解决：** 这是正常现象，首次访问后会有缓存

### Q3: 服务自动休眠

**原因：** Render免费版15分钟无请求自动休眠

**解决：**
- 定期ping健康检查接口
- 或升级到付费版（$5/月）

### Q4: API调用失败

**原因：** Coze API Token错误或过期

**解决：**
1. 重新获取Coze API Token
2. 更新Render环境变量
3. 重新部署

---

## 📚 相关文档

- [DEPLOY_ONLINE.md](DEPLOY_ONLINE.md) - 详细部署指南
- [README.md](README.md) - 项目说明
- [QUICK_START.md](QUICK_START.md) - 快速开始
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 常见问题

---

## 🎯 下一步优化

1. **监控服务** - 添加Uptime监控，确保服务在线
2. **域名绑定** - 绑定自定义域名
3. **CDN加速** - 为前端添加CDN
4. **日志收集** - 收集和分析访问日志
5. **升级计划** - 考虑升级到付费版（如需要）

---

**最后更新：** 2025-06-20
**部署状态：** 🚀 准备就绪
