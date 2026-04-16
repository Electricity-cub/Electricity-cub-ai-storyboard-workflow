# AI分镜师工作流

> 将剧本转化为Seedance 2.0（即梦）视频提示词的AI工作流

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12-green.svg)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.0-orange.svg)](https://github.com/langchain-ai/langgraph)

## ✨ 功能特性

- 🎬 **导演讲戏**：分析剧本，生成完整的导演工作单（表演/美术/摄影/灯光/服化道/后期指导）
- 👥 **人物设计**：为每个角色生成中英双版文生图提示词
- 🎨 **场景设计**：按镜头设置生成场景提示词
- 📋 **分镜头脚本**：运用电影语法设计镜头序列，包含5种插入镜头
- 🎥 **视频提示词**：转化为Seedance 2.0镜头指令，可直接生成视频
- 🚀 **并行处理**：人物、场景、分镜头脚本并行执行，提升效率
- 🌐 **API服务**：提供HTTP API，轻松集成到现有系统

## 🚀 快速开始

### 方式1：本地运行

#### 1. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

#### 2. 启动HTTP服务

```bash
bash scripts/http_run.sh -p 5000
```

#### 3. 调用API

```bash
curl -X POST http://localhost:5000/api/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "script_content": "你的剧本内容",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧"
  }'
```

### 方式2：快速测试

```bash
# 启动服务（终端1）
bash scripts/http_run.sh -p 5000

# 运行测试脚本（终端2）
bash test_workflow.sh
```

### 方式3：Python脚本调用

```python
from graphs.graph import main_graph
from graphs.state import GraphInput

result = main_graph.invoke(GraphInput(
    script_content="你的剧本内容",
    episode_number="ep01",
    visual_style="写实",
    project_type="国内短剧"
))

print(result["seedance_prompts"])
```

## 📖 使用指南

详细使用方法请查看 [USAGE.md](USAGE.md)

## 🌐 部署到云端

### Coze平台一键部署

**推荐使用快速部署指南（5分钟完成）**

👉 [点击查看：QUICK_DEPLOY.md](QUICK_DEPLOY.md)

**简版流程：**
```bash
# 1. 推送代码到GitHub/GitLab/Gitee
git remote add origin https://github.com/YOUR_USERNAME/ai-storyboard-workflow.git
git branch -M main
git push -u origin main

# 2. 在Coze平台创建工作流应用
# 3. 关联Git仓库
# 4. 配置部署参数：
#    - 构建命令：bash scripts/setup.sh
#    - 运行命令：bash scripts/http_run.sh -p 5000
# 5. 触发部署
```

### 自动化部署脚本

```bash
# 运行完整的自动化部署流程（交互式）
bash auto_deploy.sh
```

### 部署前检查

```bash
# 检查部署环境
bash pre_deploy_check.sh
```

**详细文档：**
- 🚀 [快速部署指南](QUICK_DEPLOY.md) - 5分钟完成部署
- 📚 [完整部署文档](COZE_DEPLOY.md) - 详细的步骤说明
- 🧪 [测试脚本](test_workflow.sh) - 部署后验证

### 上传到GitHub

```bash
# 使用自动化脚本
bash upload_to_github.sh
```

## 📊 输出结果

工作流输出包含5个核心部分：

```json
{
  "director_notes": {
    "项目基础信息": {...},
    "剧情点工作单": [...]
  },
  "character_prompts": {
    "characters": [...]
  },
  "scene_prompts": {
    "scenes": [...]
  },
  "storyboard": {...},
  "seedance_prompts": {
    "project_info": {...},
    "plot_points": [...]
  }
}
```

**各部分用途：**

| 输出部分 | 用途 | 工具 |
|---------|------|------|
| 导演讲戏本 | 给导演和剧组参考 | 文档查看 |
| 人物提示词 | 生成角色参考图 | 即梦/Midjourney |
| 场景提示词 | 生成场景参考图 | 即梦/Midjourney |
| 分镜头脚本 | 摄影师镜头设计参考 | - |
| 视频提示词 | 生成视频片段 | Seedance 2.0 |

## 🏗️ 项目结构

```
.
├── src/
│   ├── graphs/
│   │   ├── state.py              # 状态定义
│   │   ├── graph.py              # 图编排
│   │   └── nodes/                # 5个节点
│   │       ├── director_notes_node.py
│   │       ├── character_design_node.py
│   │       ├── scene_design_node.py
│   │       ├── storyboard_node.py
│   │       └── seedance_prompts_node.py
│   ├── main.py                   # HTTP服务入口
│   ├── agents/                   # Agent定义
│   ├── tools/                    # 工具函数
│   └── utils/                    # 工具类
├── config/                       # 大模型配置文件
│   ├── director_notes_cfg.json
│   ├── character_design_cfg.json
│   ├── scene_design_cfg.json
│   ├── storyboard_cfg.json
│   └── seedance_prompts_cfg.json
├── scripts/                      # 脚本工具
│   ├── http_run.sh              # 启动HTTP服务
│   ├── setup.sh                 # 环境设置
│   └── pack.sh                  # 打包依赖
├── USAGE.md                      # 使用指南
├── COZE_DEPLOY.md               # Coze部署指南
├── AGENTS.md                    # 项目文档
├── test_workflow.sh             # 测试脚本
├── pre_deploy_check.sh          # 部署前检查
├── upload_to_github.sh          # GitHub上传脚本
└── pyproject.toml               # 项目配置
```

## 🔧 技术栈

- **框架**: LangGraph 1.0
- **语言**: Python 3.12
- **大模型**: doubao-seed-2-0-pro-260215
- **Web框架**: FastAPI
- **依赖管理**: uv

## 📝 输入参数

| 参数 | 类型 | 必填 | 说明 | 可选值 |
|------|------|------|------|--------|
| script_content | string | ✅ | 剧本内容 | - |
| episode_number | string | ❌ | 集数 | 默认 "ep01" |
| visual_style | string | ❌ | 视觉风格 | 3D CG \| 国漫 \| 日漫 \| 写实 |
| project_type | string | ❌ | 项目类型 | 国内短剧 \| 海外短剧 \| 国内动漫剧 \| 海外动漫剧 |
| target_language | string | ❌ | 目标语言 | 英文 \| 日文 \| 其他 |

## 🎯 使用场景

1. **短剧制作**：快速生成竖屏短剧的分镜和视频提示词
2. **动画制作**：为动画剧集设计分镜头和角色场景
3. **短视频创作**：批量生成短视频的分镜脚本
4. **广告制作**：根据脚本生成广告片的镜头设计
5. **教育培训**：学习影视制作和分镜设计

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [LangGraph](https://github.com/langchain-ai/langgraph) - 工作流编排框架
- [Coze](https://www.coze.cn/) - AI应用开发平台
- [Seedance 2.0](https://jimeng.jianying.com/) - 视频生成工具

## 📞 联系方式

- 项目主页: [GitHub](https://github.com/yourusername/ai-storyboard-workflow)
- 问题反馈: [Issues](https://github.com/yourusername/ai-storyboard-workflow/issues)
- 文档: [Wiki](https://github.com/yourusername/ai-storyboard-workflow/wiki)

---

**注意**: 本工作流生成的内容仅供参考，实际使用时请根据具体需求调整。
