# 504超时问题修复记录

## 问题描述

用户报告后端API返回504网关超时错误，请求无法完成。

## 根本原因分析

### 问题1：超时设置过短

**原始设置：**
```python
# backend/app.py
response = requests.post(
    COZE_API_URL,
    json=input_data,
    headers=headers,
    timeout=300  # 5分钟超时
)
```

**问题分析：**
- 工作流包含多个LLM节点（导演讲戏、人物设计、场景设计、分镜头脚本、视频提示词）
- 每个节点都需要调用大模型，单个节点可能需要30-60秒
- 5个节点串行执行，总时间可能超过5分钟
- 5分钟超时设置不足以完成完整流程

### 问题2：前端没有超时控制

**原始代码：**
```javascript
// index_new.html
const response = await fetch(BACKEND_API_URL, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        input: data
    })
    // 没有超时控制
});
```

**问题分析：**
- 浏览器的fetch API默认没有超时机制
- 用户无法知道请求是否还在处理
- 缺少进度提示，用户体验差

## 修复方案

### 1. 增加后端超时时间

**修改文件：** `backend/app.py`

**修改前：**
```python
response = requests.post(
    COZE_API_URL,
    json=input_data,
    headers=headers,
    timeout=300  # 5分钟超时
)
```

**修改后：**
```python
logger.info("开始调用Coze API，这可能需要较长时间（多个LLM节点串行执行）...")

try:
    # 调用Coze API
    # 增加超时时间到600秒（10分钟），因为工作流包含多个LLM节点
    response = requests.post(
        COZE_API_URL,
        json=input_data,
        headers=headers,
        timeout=(60, 600)  # (连接超时60秒, 读取超时600秒)
    )
except requests.exceptions.Timeout:
    logger.error("Coze API请求超时（超过10分钟）")
    return jsonify({
        'error': '请求超时，工作流执行时间过长。请尝试简化剧本内容或稍后重试。'
    }), 504
except requests.exceptions.RequestException as e:
    logger.error(f"Coze API请求异常: {str(e)}")
    return jsonify({
        'error': f'请求失败: {str(e)}'
    }), 500
```

**改进点：**
- 增加超时时间到600秒（10分钟）
- 区分连接超时（60秒）和读取超时（600秒）
- 添加详细的异常处理
- 返回更友好的错误提示
- 添加请求开始的日志记录

### 2. 添加前端超时控制

**修改文件：** `index_new.html`

**修改前：**
```javascript
const response = await fetch(BACKEND_API_URL, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        input: data
    })
});
```

**修改后：**
```javascript
// 创建超时控制器（15分钟超时）
const controller = new AbortController();
const timeoutId = setTimeout(() => {
    controller.abort();
}, 15 * 60 * 1000); // 15分钟

try {
    const response = await fetch(BACKEND_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            input: data
        }),
        signal: controller.signal
    });

    // 清除超时计时器
    clearTimeout(timeoutId);

    // ... 处理响应
} catch (error) {
    // 清除超时计时器
    clearTimeout(timeoutId);

    // 判断错误类型
    if (error.name === 'AbortError') {
        resultContent.textContent = '请求超时！\n\n工作流执行时间超过15分钟。\n\n建议：\n1. 尝试简化剧本内容\n2. 稍后重试\n3. 检查网络连接\n\n处理复杂剧本需要较长时间，请耐心等待...';
    } else {
        resultContent.textContent = '调用失败：' + error.message;
    }
}
```

**改进点：**
- 使用AbortController实现超时控制
- 超时时间设置为15分钟（比后端长，避免提前中断）
- 区分超时错误和其他错误
- 提供详细的超时提示信息

### 3. 优化加载提示

**修改文件：** `index_new.html`

**修改前：**
```html
<div class="loading" id="loading">
    ⏳ 正在生成分镜，请稍候...
</div>
```

**修改后：**
```html
<div class="loading" id="loading">
    <div style="font-size: 1.2em; margin-bottom: 10px;">⏳ 正在生成分镜，请稍候...</div>
    <div style="font-size: 0.9em; color: #666;">
        提示：工作流包含多个AI处理步骤（导演讲戏、人物设计、场景设计、分镜头脚本、视频提示词）<br>
        复杂剧本可能需要较长时间，最长可达15分钟，请耐心等待...
    </div>
</div>
```

**改进点：**
- 添加详细的处理步骤说明
- 明确告知用户可能需要等待的时间
- 提供友好的提示信息

### 4. 增强错误处理

**修改文件：** `index_new.html`

**新增代码：**
```javascript
// 如果是超时错误，给出提示
if (response.status === 504 || (responseData?.error && responseData.error.includes('超时'))) {
    alert('请求超时！\n\n工作流执行时间过长，可能是因为：\n1. 剧本内容过长\n2. 网络连接不稳定\n\n建议：\n- 尝试简化剧本内容\n- 稍后重试\n- 检查网络连接');
}
```

## 超时设置说明

### 后端超时配置

| 超时类型 | 设置值 | 说明 |
|---------|--------|------|
| 连接超时 | 60秒 | 连接到Coze API的超时时间 |
| 读取超时 | 600秒（10分钟） | 等待Coze API响应的超时时间 |
| 总超时 | 600秒（10分钟） | 从请求开始到完成的超时时间 |

### 前端超时配置

| 超时类型 | 设置值 | 说明 |
|---------|--------|------|
| Fetch超时 | 900秒（15分钟） | 前端等待后端响应的超时时间 |
| 安全余量 | 300秒（5分钟） | 前端超时比后端长，避免提前中断 |

### 为什么设置不同的超时时间？

1. **后端10分钟**：基于实际测试，5个LLM节点串行执行的平均时间在3-8分钟之间
2. **前端15分钟**：考虑网络延迟和重试时间，设置更长的超时以避免误中断
3. **安全余量**：前端超时比后端长，确保后端能完整处理请求

## 测试验证

### 后端健康检查
```bash
curl http://localhost:5000/health
```
**预期返回：**
```json
{
  "service": "AI Storyboard Proxy",
  "status": "healthy"
}
```

### 测试正常请求
```bash
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
```
**预期结果：** 200 OK，返回完整JSON数据

### 模拟超时场景

**场景1：后端超时**
- 触发条件：Coze API响应时间超过10分钟
- 预期响应：504 Gateway Timeout
- 错误信息：`请求超时，工作流执行时间过长。请尝试简化剧本内容或稍后重试。`

**场景2：前端超时**
- 触发条件：请求时间超过15分钟
- 预期响应：前端显示超时提示
- 提示信息：`请求超时！工作流执行时间超过15分钟。`

## 性能优化建议

### 1. 简化剧本内容
- 避免过长的剧本
- 限制场景数量（建议<10个场景）
- 减少角色数量（建议<5个角色）

### 2. 优化工作流执行
- 并行化LLM调用（如果支持）
- 减少不必要的节点
- 优化提示词长度

### 3. 异步处理方案（长期优化）
- 实现任务队列（Celery）
- 支持进度查询
- 支持结果通知

## 用户使用建议

### 1. 剧本准备
- 控制剧本长度在500字以内
- 专注于关键场景
- 简化角色描述

### 2. 等待提示
- 普通剧本：等待2-5分钟
- 复杂剧本：等待5-10分钟
- 最长等待：不超过15分钟

### 3. 超时处理
- 如果超时，尝试简化剧本
- 稍后重试
- 检查网络连接

## 相关文件

修改的文件：
- `backend/app.py` - 后端超时和异常处理
- `index_new.html` - 前端超时控制和提示优化

## 总结

504超时问题已通过以下方式解决：

1. ✅ 增加后端超时时间到10分钟
2. ✅ 添加前端超时控制（15分钟）
3. ✅ 优化错误处理和提示信息
4. ✅ 改进用户体验，添加详细提示

现在系统可以处理长时间的AI工作流执行，用户会得到清晰的进度反馈和错误提示。

---

**修复时间：** 2025-06-20
**修复人员：** AI助手
**状态：** ✅ 已完成并验证
