# AI分镜师工作流使用指南

## 🚀 快速开始

### 方式1：启动HTTP服务（推荐）

#### 1. 启动服务
```bash
bash scripts/http_run.sh -m http -p 5000
```

服务启动后，会在 `http://localhost:5000` 提供API接口。

#### 2. 调用API

**请求示例：**
```bash
curl -X POST http://localhost:5000/api/v1/run \
  -H "Content-Type: application/json" \
  -d '{
    "script_content": "第1集：荒海求生\n\n【场景：甲板 - 日】\n\nP01：苏醒\n\n海面上空，一艘破旧的货船在灰蓝阴天下漂浮。\n\n甲板上，凌羽慢慢睁开眼睛，发现自己躺在横七竖八的女生中间。",
    "episode_number": "ep01",
    "visual_style": "写实",
    "project_type": "国内短剧",
    "target_language": null
  }'
```

**响应格式（JSON）：**
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

### 方式2：Python脚本直接调用

创建一个 `run_workflow.py` 文件：

```python
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import new_context
from graphs.graph import main_graph
from graphs.state import GraphInput

# 创建上下文
ctx = new_context("run")

# 准备输入参数
input_data = GraphInput(
    script_content="""
    第1集：荒海求生
    
    【场景：甲板 - 日】
    
    P01：苏醒
    
    海面上空，一艘破旧的货船在灰蓝阴天下漂浮。
    
    甲板上，凌羽慢慢睁开眼睛，发现自己躺在横七竖八的女生中间。女生们面色苍白，长发凌乱，一动不动。
    
    凌羽（惊恐）：这是哪儿？
    
    洛凝雪（虚弱）：我们...好像在海上。
    
    凌羽站起身，环顾四周。桅杆断裂，残帆在风中抖动。
    """,
    episode_number="ep01",
    visual_style="写实",
    project_type="国内短剧",
    target_language=None
)

# 运行工作流
config = RunnableConfig(
    configurable={"thread_id": ctx.run_id}
)

result = main_graph.invoke(input_data, config=config, runtime=Runtime(ctx))

# 输出结果
print("=" * 50)
print("🎬 导演讲戏本")
print("=" * 50)
print(result["director_notes"])

print("\n" + "=" * 50)
print("👥 人物提示词")
print("=" * 50)
print(result["character_prompts"])

print("\n" + "=" * 50)
print("🎨 场景提示词")
print("=" * 50)
print(result["scene_prompts"])

print("\n" + "=" * 50)
print("📋 分镜头脚本")
print("=" * 50)
print(result["storyboard"])

print("\n" + "=" * 50)
print("🎥 Seedance视频提示词")
print("=" * 50)
print(result["seedance_prompts"])
```

运行脚本：
```bash
python run_workflow.py
```

## 📊 输出结果说明

### 1. 导演讲戏本 (director_notes)

**字段说明：**
```json
{
  "项目基础信息": {
    "集数": "ep01",
    "项目名称": "荒海求生",
    "项目类型": "国内短剧",
    "视觉风格": "写实",
    "人物清单": ["凌羽", "洛凝雪", "白霜", "遇险女生群像"],
    "场景清单": ["货船甲板（日）", "货船船舱（日）"]
  },
  "剧情点工作单": [
    {
      "元数据": {
        "编号": "P01",
        "标题": "苏醒",
        "时长建议": "1分30秒",
        "场景": "货船甲板 - 日",
        "出场人物": ["凌羽", "洛凝雪", "遇险女生群像"]
      },
      "表演指导": {...},
      "美术指导": {...},
      "摄影指导": {...},
      "灯光指导": {...},
      "服化道指导": {...},
      "后期指导": {...}
    }
  ]
}
```

**用途：**
- 给导演和演员看，明确每个场景的表演要求
- 给美术、摄影、灯光团队提供详细的制作指导
- 提取人物清单和场景清单

### 2. 人物提示词 (character_prompts)

**格式示例：**
```json
{
  "characters": [
    {
      "name": "凌羽",
      "description": "24岁左右的东亚男性，脸型偏方硬朗...",
      "prompt_cn": "单人竖屏全身像，简洁背景，写实风格。24岁左右的东亚男性...",
      "prompt_en": "Vertical full body portrait of a single person, plain background..."
    }
  ]
}
```

**用途：**
- 将 `prompt_cn` 复制到即梦/Seedream生成角色参考图
- 将 `prompt_en` 复制到Midjourney生成角色参考图
- 用于后续视频生成的角色一致性

### 3. 场景提示词 (scene_prompts)

**格式示例：**
```json
{
  "scenes": [
    {
      "name": "货船甲板（日）- P01苏醒全景",
      "angle": "24mm广角航拍",
      "prompt_cn": "写实风格，无人空镜，24mm广角航拍大景别...",
      "prompt_en": "Photorealistic style, no people, 24mm wide-angle..."
    }
  ]
}
```

**用途：**
- 将 `prompt_cn` 复制到即梦/Seedream生成场景参考图
- 将 `prompt_en` 复制到Midjourney生成场景参考图
- 用于视频生成的场景一致性

### 4. 分镜头脚本 (storyboard)

**格式示例：**
```json
{
  "total_shots": 15,
  "insert_shots": 6,
  "plot_points": [
    {
      "number": "P01",
      "title": "苏醒",
      "shots": [
        {
          "shot_id": "P01-S01",
          "type": "[环境INSERT]",
          "camera": "24mm",
          "movement": "航拍",
          "duration": "3s",
          "description": "海面上空，一艘破旧的货船...",
          "dialogue": "无台词",
          "audio": "海风呼啸声"
        }
      ]
    }
  ]
}
```

**用途：**
- 给摄影师看，明确每个镜头的拍摄要求
- 检查镜头逻辑和叙事完整性
- 传递给视频提示词生成节点

### 5. Seedance视频提示词 (seedance_prompts)

**格式示例：**
```json
{
  "project_info": {
    "visual_style": "写实",
    "project_type": "国内短剧",
    "aspect_ratio": "竖屏9:16"
  },
  "asset_mapping": [
    {"id": "@图片1", "type": "人物", "name": "凌羽"},
    {"id": "@图片2", "type": "人物", "name": "洛凝雪"},
    {"id": "@图片3", "type": "场景", "name": "货船甲板"}
  ],
  "plot_points": [
    {
      "number": "P01",
      "prompts": [
        {
          "shot_id": "P01-S01",
          "type": "[环境INSERT]",
          "duration": "3s",
          "prompt": "竖屏9:16，3秒。24mm全景，航拍，固定。灰蓝侧光左上45度，明暗分割。海面上空，一艘破旧的货船在灰蓝阴天下漂浮，桅杆断裂，残帆在风中抖动。音频：海风呼啸声。画面中不要出现任何字幕。",
          "assets": ["@图片3"]
        }
      ]
    }
  ]
}
```

**用途：**
- 直接复制到Seedance 2.0（即梦）生成视频
- 每条提示词对应一个4-15秒的视频片段
- 按顺序生成后拼接成完整视频

## 🎯 输出结果保存

### 保存为JSON文件
```python
import json

# 保存完整结果
with open("workflow_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# 分别保存各部分
with open("director_notes.json", "w", encoding="utf-8") as f:
    json.dump(result["director_notes"], f, ensure_ascii=False, indent=2)

with open("character_prompts.json", "w", encoding="utf-8") as f:
    json.dump(result["character_prompts"], f, ensure_ascii=False, indent=2)
```

### 转换为Markdown文档
```python
def save_to_markdown(result, output_dir="outputs"):
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # 保存导演讲戏本
    with open(f"{output_dir}/01-director-notes.md", "w", encoding="utf-8") as f:
        f.write("# 导演讲戏本\n\n")
        f.write(f"## 项目基础信息\n\n")
        # ... 写入内容
    
    # 保存人物提示词
    with open(f"{output_dir}/02-character-prompts.md", "w", encoding="utf-8") as f:
        f.write("# 人物提示词\n\n")
        # ... 写入内容
    
    # 保存场景提示词
    with open(f"{output_dir}/03-scene-prompts.md", "w", encoding="utf-8") as f:
        f.write("# 场景提示词\n\n")
        # ... 写入内容
    
    # 保存分镜头脚本
    with open(f"{output_dir}/04-storyboard.md", "w", encoding="utf-8") as f:
        f.write("# 分镜头脚本\n\n")
        # ... 写入内容
    
    # 保存视频提示词
    with open(f"{output_dir}/05-seedance-prompts.md", "w", encoding="utf-8") as f:
        f.write("# Seedance视频提示词\n\n")
        # ... 写入内容
```

## 📝 参数说明

### 输入参数
| 参数 | 类型 | 必填 | 说明 | 可选值 |
|------|------|------|------|--------|
| script_content | string | ✅ | 剧本内容 | - |
| episode_number | string | ❌ | 集数 | 默认 "ep01" |
| visual_style | string | ❌ | 视觉风格 | 3D CG \| 国漫 \| 日漫 \| 写实 |
| project_type | string | ❌ | 项目类型 | 国内短剧 \| 海外短剧 \| 国内动漫剧 \| 海外动漫剧 |
| target_language | string | ❌ | 目标语言（海外剧时） | 英文 \| 日文 \| 其他 |

### 输出参数
所有输出均为JSON格式，包含5个核心部分。

## ⚠️ 注意事项

1. **剧本长度**：建议单集剧本不超过5000字，过长可能影响生成质量
2. **人物数量**：建议单集主要角色不超过10个
3. **场景数量**：建议单集场景不超过20个
4. **API调用**：HTTP服务默认端口5000，可根据需要修改
5. **超时设置**：工作流默认超时15分钟，复杂剧本可能需要更长时间

## 🐛 常见问题

### Q1: 工作流运行很慢怎么办？
A: 
- 剧本太长，建议拆分成多个剧情点分别处理
- 可以调整各节点的 `max_completion_tokens` 参数减少生成内容

### Q2: 输出结果不理想怎么办？
A:
- 检查剧本格式是否规范（场景标注、对话格式等）
- 调整 `visual_style` 和 `project_type` 参数
- 可以修改配置文件中的系统提示词（sp）来优化输出质量

### Q3: 如何批量处理多集剧本？
A:
```python
# 批量处理示例
episodes = [
    "第1集内容...",
    "第2集内容...",
    "第3集内容..."
]

for i, script in enumerate(episodes, 1):
    input_data = GraphInput(
        script_content=script,
        episode_number=f"ep{i:02d}",
        visual_style="写实",
        project_type="国内短剧"
    )
    result = main_graph.invoke(input_data)
    # 保存结果
```

## 📞 技术支持

如有问题，请查看：
- 项目日志：`/app/work/logs/bypass/app.log`
- 配置文件：`config/` 目录
- 节点实现：`src/graphs/nodes/` 目录
