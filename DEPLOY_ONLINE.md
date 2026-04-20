# 🚀 线上部署指南

## ✅ 第一步：代码已推送

你的代码已经成功推送到GitHub仓库：
- 仓库地址：https://github.com/Electricity-cub/Electricity-cub-ai-storyboard-workflow
- 分支：main
- 提交：9个本地提交已推送

## 🌐 第二步：选择部署平台

### 方案1：Render（推荐，免费）

**优点：**
- ✅ 完全免费
- ✅ 支持Python后端
- ✅ 自动HTTPS
- ✅ 自动部署（Git push后）
- ✅ 支持环境变量

**步骤：**

#### 1. 注册Render账号

1. 访问：https://render.com
2. 点击 "Sign Up"
3. 使用GitHub账号登录（推荐）

#### 2. 创建Web服务

1. 登录后，点击 "New +"
2. 选择 "Web Service"
3. 连接你的GitHub仓库
4. 选择 `Electricity-cub-ai-storyboard-workflow` 仓库
5. 点击 "Connect"

#### 3. 配置服务

**基本信息：**
- Name: `ai-storyboard-api`（或自定义）
- Region: Singapore（推荐，国内访问快）
- Branch: `main`

**构建配置：**
- Runtime: `Python 3`
- Build Command: `pip install -r backend/requirements.txt`
- Start Command: `cd backend && python3 app.py`

**环境变量（重要）：**

点击 "Advanced" → "Add Environment Variable"，添加以下变量：

```bash
# Coze API配置
COZE_API_URL=https://3b7j5mjhsz.coze.site/run
COZE_API_TOKEN=你的Coze_API_Token

# Flask配置
FLASK_APP=app.py
FLASK_ENV=production
PORT=5000
```

**获取Coze API Token：**
1. 登录Coze平台
2. 找到你的工作流
3. 获取API Token
4. 复制到环境变量中

#### 4. 创建服务

点击 "Create Web Service"，等待部署完成（约2-3分钟）

#### 5. 获取服务地址

部署成功后，会显示：
- 服务地址：`https://ai-storyboard-api.onrender.com`
- 健康检查：`https://ai-storyboard-api.onrender.com/health`

#### 6. 更新前端API地址

修改前端页面的API地址：

**index_async.html:**
```javascript
const BACKEND_API_URL = 'https://ai-storyboard-api.onrender.com/api/v1/tasks';
```

**index_new.html:**
```javascript
const BACKEND_API_URL = 'https://ai-storyboard-api.onrender.com/run';
```

---

### 方案2：Vercel（需要配置）

**注意：** Vercel主要用于前端，部署后端需要额外配置。

如果选择Vercel，需要创建一个 `vercel.json` 配置文件。

---

## 🔍 第三步：验证部署

### 1. 测试健康检查

```bash
curl https://ai-storyboard-api.onrender.com/health
```

**预期返回：**
```json
{
  "status": "healthy",
  "service": "AI Storyboard Proxy",
  "active_tasks": 0
}
```

### 2. 测试创建任务

```bash
curl -X POST https://ai-storyboard-api.onrender.com/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "script_content": "测试剧本",
      "episode_number": "ep01",
      "visual_style": "写实",
      "project_type": "国内短剧"
    }
  }'
```

### 3. 在浏览器中测试

1. 修改前端页面的API地址
2. 在浏览器中打开 `index_async.html`
3. 输入剧本内容，点击"生成分镜"
4. 查看结果

---

## 📝 第四步：更新文档

创建一个 `DEPLOYED.md` 文件，记录线上环境信息：

```markdown
# 线上环境配置

## 服务地址

- 后端API: https://ai-storyboard-api.onrender.com
- 健康检查: https://ai-storyboard-api.onrender.com/health

## 前端页面

- 异步版本: [index_async.html](index_async.html)
- 同步版本: [index_new.html](index_new.html)

## 使用方法

1. 打开前端页面
2. 输入剧本内容
3. 点击"生成分镜"
4. 查看结果

## 注意事项

1. 首次访问可能较慢（服务冷启动）
2. 免费版有15分钟不活动自动休眠
3. 建议定期使用保持服务活跃
```

---

## 🎯 第五步：分享给他人

1. 将前端页面（`index_async.html`）部署到静态托管（如GitHub Pages、Vercel）
2. 或直接将HTML文件发给他人（修改API地址为线上地址）
3. 提供使用说明

---

## 💡 常见问题

### 问题1：部署失败

**原因：** 环境变量未配置或配置错误

**解决：**
1. 检查COZE_API_TOKEN是否正确
2. 检查COZE_API_URL是否正确
3. 查看Render日志，定位错误

### 问题2：首次访问慢

**原因：** Render免费版有冷启动时间（约30-60秒）

**解决：** 这是正常现象，首次访问后会有缓存

### 问题3：服务自动休眠

**原因：** Render免费版15分钟无请求自动休眠

**解决：**
- 定期ping健康检查接口
- 或升级到付费版（$5/月）

### 问题4：跨域问题

**原因：** 前端直接调用线上API可能有跨域限制

**解决：**
- 确保后端配置了CORS
- 使用代理服务
- 或将前端和后端部署到同一域名

---

## 📊 部署检查清单

- [x] 代码已推送到GitHub
- [ ] Render账号已创建
- [ ] Web服务已创建
- [ ] 环境变量已配置
- [ ] 服务已部署成功
- [ ] 健康检查通过
- [ ] 前端API地址已更新
- [ ] 功能测试通过

---

## 🎉 部署完成

恭喜！你的AI分镜师工作流已经成功部署到线上！

**线上服务地址：**
- 后端API: `https://ai-storyboard-api.onrender.com`
- 健康检查: `https://ai-storyboard-api.onrender.com/health`

**下一步：**
1. 分享给团队成员
2. 收集反馈，持续优化
3. 考虑升级到付费版（如需要）

---

**最后更新：** 2025-06-20
**部署状态：** 🚀 准备部署
