# 后端API测试说明

## 问题已修复 ✅

之前的 400 BAD REQUEST 错误已经完全修复。后端现在支持两种请求格式。

## 支持的请求格式

### 格式1：包装格式（推荐）
```json
{
  "input": {
    "script_content": "你的剧本内容",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }
}
```

### 格式2：直接格式（兼容）
```json
{
  "script_content": "你的剧本内容",
  "episode_number": "ep01",
  "visual_style": "写实",
  "project_type": "国内短剧"
}
```

## 测试命令

### 测试格式1（包装格式）
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "script_content": "测试格式1",
      "episode_number": "ep01",
      "visual_style": "写实",
      "project_type": "国内短剧"
    }
  }'
```

### 测试格式2（直接格式）
```bash
curl -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{
    "script_content": "测试格式2",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }'
```

## 预期响应

成功时返回 200 状态码和JSON数据：
```json
{
  "character_prompts": {
    "characters": [],
    "raw_content": "..."
  },
  "director_notes": {
    "项目基础信息": {...},
    "剧情点列表": [...]
  },
  "scene_prompts": {...},
  "storyboard": {...},
  "video_prompts": {...}
}
```

## 错误响应

### 400 错误（请求格式错误）
```json
{
  "error": "剧本内容不能为空"
}
```

### 504 错误（请求超时）✅ 已优化
```json
{
  "error": "请求超时，工作流执行时间过长。请尝试简化剧本内容或稍后重试。"
}
```

**说明：**
- 工作流包含多个LLM节点，执行时间可能较长
- 后端超时设置为10分钟，前端超时设置为15分钟
- 如果超时，请尝试：
  1. 简化剧本内容（<500字，<10个场景）
  2. 稍后重试
  3. 检查网络连接

### 500 错误（服务器错误）
```json
{
  "error": "API Token未配置，请在app.py中设置COZE_API_TOKEN"
}
```

## 前端调用示例

### JavaScript（fetch）
```javascript
// 格式1
fetch('http://localhost:5000/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    input: {
      script_content: document.getElementById('script_content').value,
      episode_number: document.getElementById('episode_number').value,
      visual_style: document.getElementById('visual_style').value,
      project_type: document.getElementById('project_type').value
    }
  })
})

// 格式2
fetch('http://localhost:5000/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    script_content: document.getElementById('script_content').value,
    episode_number: document.getElementById('episode_number').value,
    visual_style: document.getElementById('visual_style').value,
    project_type: document.getElementById('project_type').value
  })
})
```

## 常见问题

### Q: 为什么之前会报 400 错误？
A: 之前的代码要求请求必须包含 `input` 字段，现在已经改为支持两种格式。

### Q: 如何验证后端是否正常运行？
A: 访问 http://localhost:5000/health 应该返回 `{"status": "ok"}`。

### Q: 如何查看后端日志？
A: 查看控制台输出或配置日志文件路径。

### Q: 请求超时怎么办？
A: 后端设置了 300 秒（5分钟）超时，如果工作流执行时间过长，可以在 `backend/app.py` 中调整 `timeout` 参数。

## 下一步

1. 确保后端服务正在运行：`cd backend && python3 app.py`
2. 打开前端页面：`index_new.html`（通过本地服务器）
3. 填写表单并提交，查看结果
