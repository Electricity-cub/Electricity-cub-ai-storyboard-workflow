# 📋 如何查看Coze工作流的API地址

根据你的Token分析，你的工作流ID是：`7629249569586413578`

## 🔍 方法1：在Coze平台查看（推荐）

### 步骤：

1. **登录Coze平台**
   - 访问 https://www.coze.com/ 或 https://www.coze.cn/

2. **找到你的工作流**
   - 在工作台找到"AI分镜师"工作流
   - 点击进入工作流编辑页面

3. **查看API信息**
   - 在工作流页面，点击右上角的"发布"按钮
   - 或点击"运行"按钮旁边的三点菜单
   - 选择"API调用"或"发布为API"
   - 你会看到API调用地址和示例

4. **获取API地址**
   - API地址通常显示为：`https://xxx.coze.site/workflow_run`
   - 或：`https://api.coze.cn/v1/workflow/run`

## 🔍 方法2：从Token中推断

你的Token信息：
- **工作流ID**: `7629249569586413578`
- **发行平台**: `https://api.coze.cn`

可能的API地址：

```
1. https://api.coze.cn/v1/workflow/run
2. https://api.coze.cn/open_api/v1/workflow/run
3. https://api.coze.cn/open_api/v2/workflow/run
4. https://7629249569586413578.coze.site/workflow_run
```

## 🔍 方法3：使用Coze API测试工具

1. 访问 https://www.coze.cn/docs/developer_guides/api_reference
2. 使用在线API测试工具
3. 输入你的工作流ID和Token
4. 测试不同的API地址

## ✅ 更新配置

找到正确的API地址后，按以下步骤更新：

### 步骤1：更新backend配置

编辑 `backend/app.py` 文件：

```python
# 找到第23行，修改为正确的API地址
COZE_API_URL = "你的正确API地址"

# 例如：
COZE_API_URL = "https://api.coze.cn/open_api/v1/workflow/run"
```

### 步骤2：重启后端服务

```bash
# 停止当前服务（按Ctrl+C）

# 重新启动
cd /workspace/projects/backend
python3 app.py
```

### 步骤3：测试

```bash
curl -X POST http://localhost:5000/api/v1/generate \
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

## 📝 当前配置

你的当前配置：
```python
COZE_API_URL = "https://3b7j5mjhsz.coze.site/workflow_run"
COZE_API_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNhMmE2OTQyLTU3N2EtNDUxYi1hOWYyLWE3MTk5M2I1OTU5YyJ9.eyJpc3MiOiJodHRwczovL2FwaS5jb3plLmNuIiwiYXVkIjpbIjZrZGF1aEFoN2VOUVczWUgwS3NYMjltcEs4SGJRRldiIl0sImV4cCI6ODIxMDI2Njg3Njc5OSwiaWF0IjoxNzc2MzMyNTkzLCJzdWIiOiJzcGlmZmU6Ly9hcGkuY296ZS5jbi93b3JrbG9hZF9pZGVudGl0eS9pZDo3NjI5MjQ5NTY5NTg2NDEzNTc4Iiwic3JjIjoiaW5ib3VuZF9hdXRoX2FjY2Vzc190b2tlbl9pZDo3NjI5MjkwMzk2MTI3ODU0NTkyIn0.SKYvYox0_8ojDtrNzk8DfwaecpQvLGl9eRCRCMFz3Imk-oScDXTyBKB_FNkAG3boS5tG2e75VQ-bVxB_LVakcDKXTU2zQ324PirHsoOL4qbdNz6hCokNgAUzNIedCNboN3DYZTyIGsDXL7K_wL18qJ1L7uxPVphOaq6mrAGOQ2E9F-4lhuBboVbv21iomfRiNV1xNviMPse9UhyreDTmBompWgdVBmD0LoLt6P1ghfrFCetyfhQa8NZEh6DxFv1ZuZ1yooaIVfJ51h_hI2WMBOHMSWdQh0g7WIkeR5XtyhNV_VFtEwAlAYOiJXVYZL21FeLvBHgcLUGuN0t2eF3H2A"
```

## 🎯 下一步

1. 在Coze平台找到正确的API地址
2. 更新 `backend/app.py` 中的 `COZE_API_URL`
3. 重启服务并测试

## 💡 提示

- 如果不确定API地址，可以联系Coze技术支持
- Coze API文档：https://www.coze.cn/docs
- 工作流发布后，通常会在发布页面显示API地址
