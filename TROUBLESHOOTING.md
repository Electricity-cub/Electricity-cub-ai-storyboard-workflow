# 常见问题解决方案

## 问题汇总

本文档汇总了AI分镜师工作流中常见的问题及其解决方案。

---

## 1. 400 BAD REQUEST

### 症状
```
Error: Client error '400 BAD REQUEST' for url 'http://localhost:5000/run'
```

### 原因
请求格式不符合后端要求。

### 解决方案 ✅

**原因：** 后端之前只支持包装格式 `{"input": {...}}`

**修复：** 现在已支持两种格式

**格式1（包装格式）：**
```json
{
  "input": {
    "script_content": "剧本内容",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }
}
```

**格式2（直接格式）：**
```json
{
  "script_content": "剧本内容",
  "episode_number": "ep01",
  "visual_style": "写实",
  "project_type": "国内短剧"
}
```

**测试验证：**
```bash
# 测试格式1
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"input": {"script_content": "测试", "episode_number": "ep01", "visual_style": "写实", "project_type": "国内短剧"}}'

# 测试格式2
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"script_content": "测试", "episode_number": "ep01", "visual_style": "写实", "project_type": "国内短剧"}'
```

**相关文档：**
- [FIX_LOG.md](FIX_LOG.md) - 详细修复记录
- [TEST_GUIDE.md](TEST_GUIDE.md) - 完整测试指南

---

## 2. 504 GATEWAY TIMEOUT

### 症状
```
Error: Server error '504 GATEWAY TIMEOUT' for url 'http://localhost:5000/run'
```

### 原因
工作流执行时间超过超时限制。

### 解决方案 ✅

**原因：**
- 工作流包含5个LLM节点（导演讲戏、人物设计、场景设计、分镜头脚本、视频提示词）
- 每个节点需要调用大模型，单个节点可能需要30-60秒
- 5个节点串行执行，总时间可能超过5分钟
- 原超时设置为300秒（5分钟）不够

**修复：**
- 后端超时优化为600秒（10分钟）
- 前端超时优化为900秒（15分钟）
- 添加详细的超时提示信息

**超时配置：**
| 组件 | 超时时间 | 说明 |
|------|---------|------|
| 后端连接超时 | 60秒 | 连接到Coze API |
| 后端读取超时 | 600秒（10分钟） | 等待Coze API响应 |
| 前端Fetch超时 | 900秒（15分钟） | 等待后端响应 |

**优化建议：**
1. 简化剧本内容（<500字）
2. 限制场景数量（<10个场景）
3. 减少角色数量（<5个角色）

**用户提示：**
- 普通剧本：等待2-5分钟
- 复杂剧本：等待5-10分钟
- 最长等待：不超过15分钟

**相关文档：**
- [TIMEOUT_FIX.md](TIMEOUT_FIX.md) - 详细修复记录

---

## 3. Failed to fetch (CORS错误)

### 症状
```
Error: Failed to fetch
TypeError: Failed to fetch
```

### 原因
前端直接调用Coze API被浏览器的同源策略（CORS）阻止。

### 解决方案

**方案1：使用后端服务（推荐）**

前端应该调用本地后端服务，而不是直接调用Coze API：

```javascript
// ✅ 正确：调用后端服务
fetch('http://localhost:5000/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        input: { script_content: '...' }
    })
})

// ❌ 错误：直接调用Coze API
fetch('https://xxx.coze.site/run', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer xxx' },
    body: JSON.stringify({...})
})
```

**方案2：启动后端服务**

```bash
cd backend
./start.sh
```

**方案3：使用新版前端**

使用 `index_new.html` 而不是 `index_cozeweb.html`。

---

## 4. API Token未配置

### 症状
```
{
  "error": "API Token未配置，请在app.py中设置COZE_API_TOKEN"
}
```

### 原因
后端 `backend/app.py` 中的 `COZE_API_TOKEN` 未配置。

### 解决方案

**步骤1：获取Coze API Token**

参考 [HOW_TO_FIND_API_URL.md](HOW_TO_FIND_API_URL.md) 获取Token。

**步骤2：配置Token**

编辑 `backend/app.py`，修改第22行：

```python
COZE_API_TOKEN = "你的Coze_API_Token"  # 替换成实际Token
```

**步骤3：重启后端服务**

```bash
cd backend
./start.sh
```

---

## 5. API地址404错误

### 症状
```
Error: Coze API返回错误: 404
```

### 原因
Coze工作流API地址不正确。

### 解决方案

**步骤1：获取正确的API地址**

参考 [HOW_TO_FIND_API_URL.md](HOW_TO_FIND_API_URL.md) 获取正确的运行地址。

**步骤2：更新API地址**

编辑 `backend/app.py`，修改第21行：

```python
COZE_API_URL = "https://你的工作流地址.coze.site/run"
```

**步骤3：重启后端服务**

```bash
cd backend
./start.sh
```

---

## 6. 后端服务无法启动

### 症状
```
ModuleNotFoundError: No module named 'flask'
```

### 原因
缺少Flask依赖。

### 解决方案

**方案1：使用启动脚本（推荐）**

```bash
cd backend
./start.sh
```

**方案2：手动安装依赖**

```bash
pip install flask requests
```

**方案3：使用系统Python**

```bash
/usr/bin/python3 -m pip install flask requests
/usr/bin/python3 app.py
```

---

## 7. 前端页面无法访问

### 症状
打开 `index_new.html` 页面显示空白或报错。

### 原因
直接打开HTML文件，受浏览器安全限制。

### 解决方案

**方案1：使用本地服务器（推荐）**

```bash
# Python 3
python3 -m http.server 8000

# Node.js
npx http-server

# 然后访问
# http://localhost:8000/index_new.html
```

**方案2：使用Live Server（VS Code插件）**

安装VS Code的"Live Server"插件，右键选择"Open with Live Server"。

---

## 8. 工作流执行时间过长

### 症状
请求一直处于处理状态，超过10分钟仍未完成。

### 原因
剧本内容过长或场景过多。

### 解决方案

**优化建议：**

1. **控制剧本长度**
   - 推荐长度：< 500字
   - 简化对话和描述

2. **限制场景数量**
   - 推荐场景数：< 10个
   - 专注于关键场景

3. **减少角色数量**
   - 推荐角色数：< 5个
   - 合并相似角色

4. **分批处理**
   - 将长剧本分成多集
   - 每集单独处理

**示例：**

**❌ 不推荐（过长）：**
```
这是一个关于小明和小红的复杂爱情故事，经历了相遇、相识、相爱、误会、和好、结婚、生子、分离、重逢等30多个场景，包含20多个角色...
```

**✅ 推荐（精简）：**
```
小明和小红在公园相遇，一见钟情。他们开始聊天，发现彼此有很多共同点。
```

---

## 9. 获取不到生成的结果

### 症状
请求返回成功，但结果内容为空或不完整。

### 原因
- 剧本内容过于简单
- 缺少必要的元素（人物、场景等）

### 解决方案

**完善剧本内容：**

```json
{
  "script_content": "小明和小红在公园相遇，一见钟情。他们开始聊天，发现彼此有很多共同点。",
  "episode_number": "ep01",
  "visual_style": "写实",
  "project_type": "国内短剧"
}
```

**必填字段：**
- `script_content` - 剧本内容
- `episode_number` - 集数
- `visual_style` - 视觉风格
- `project_type` - 项目类型

---

## 10. 网络连接问题

### 症状
```
requests.exceptions.ConnectionError
Error: 检查网络连接
```

### 原因
无法连接到Coze API。

### 解决方案

**检查1：网络连接**
```bash
ping coze.site
curl -I https://coze.site
```

**检查2：代理设置**
如果使用代理，确保后端正确配置：

```python
# backend/app.py
import os
os.environ['HTTP_PROXY'] = 'http://your-proxy:port'
os.environ['HTTPS_PROXY'] = 'http://your-proxy:port'
```

**检查3：防火墙**
确保防火墙允许访问 `coze.site`

---

## 快速诊断流程

当遇到问题时，按以下流程诊断：

```
1. 检查后端服务状态
   ↓ curl http://localhost:5000/health

2. 检查API配置
   ↓ 查看 backend/app.py 的 COZE_API_TOKEN 和 COZE_API_URL

3. 检查前端请求格式
   ↓ 确保包含必填字段

4. 查看错误日志
   ↓ 后端控制台输出

5. 参考相关文档
   ↓ FIX_LOG.md, TIMEOUT_FIX.md, TEST_GUIDE.md
```

---

## 获取帮助

如果以上方案都无法解决你的问题：

1. 查看完整文档
   - [README.md](README.md) - 项目概览
   - [TEST_GUIDE.md](TEST_GUIDE.md) - 测试指南
   - [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 部署指南

2. 检查修复记录
   - [FIX_LOG.md](FIX_LOG.md) - 400错误修复
   - [TIMEOUT_FIX.md](TIMEOUT_FIX.md) - 504错误修复

3. 收集错误信息
   - 完整的错误消息
   - 后端日志
   - 前端控制台输出
   - 请求和响应数据

---

**最后更新：** 2025-06-20
