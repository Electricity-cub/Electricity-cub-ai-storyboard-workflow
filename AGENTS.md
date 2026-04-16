## 项目概述
- **名称**: AI分镜师工作流
- **功能**: 将剧本转化为Seedance 2.0（即梦）视频提示词，包含导演讲戏、人物设计、场景设计、分镜头脚本、视频提示词生成

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| director_notes | `nodes/director_notes_node.py` | agent | 导演讲戏 - 分析剧本生成导演工作单 | - | `config/director_notes_cfg.json` |
| character_design | `nodes/character_design_node.py` | agent | 人物设计 - 生成中英双版人物提示词 | - | `config/character_design_cfg.json` |
| scene_design | `nodes/scene_design_node.py` | agent | 场景设计 - 按镜头设置生成场景提示词 | - | `config/scene_design_cfg.json` |
| storyboard | `nodes/storyboard_node.py` | agent | 分镜头脚本 - 运用电影语法设计镜头序列 | - | `config/storyboard_cfg.json` |
| seedance_prompts | `nodes/seedance_prompts_node.py` | agent | 视频提示词生成 - 转化为Seedance镜头指令 | - | `config/seedance_prompts_cfg.json` |

**类型说明**: agent(大模型)

## 子图清单
| 子图名 | 文件位置 | 功能描述 | 被调用节点 |
|-------|---------|------|---------|-----------|
| 无 | - | - | - |

## 工作流结构

### 执行流程
```
剧本输入
  ↓
导演讲戏 (director_notes)
  ↓
  ├─→ 人物设计 (character_design) ─┐
  ├─→ 场景设计 (scene_design) ─────┤
  └─→ 分镜头脚本 (storyboard) ─────┤
                                    ↓
                           视频提示词生成 (seedance_prompts)
                                    ↓
                              最终输出
```

### 并行执行
- 人物设计和场景设计在导演讲戏完成后**并行执行**
- 分镜头脚本与人物/场景设计**并行执行**
- 所有前置节点完成后，进入视频提示词生成

## 输入输出

### 工作流输入 (GraphInput)
- `script_content` (str): 剧本内容
- `episode_number` (str): 集数，默认"ep01"
- `visual_style` (str): 视觉风格（3D CG | 国漫 | 日漫 | 写实）
- `project_type` (str): 项目类型（国内短剧 | 海外短剧 | 国内动漫剧 | 海外动漫剧）
- `target_language` (Optional[str]): 目标语言（海外剧时）

### 工作流输出 (GraphOutput)
- `director_notes` (dict): 导演讲戏本
  - 项目基础信息
  - 剧情点工作单（包含表演指导、美术指导、摄影指导、灯光指导、服化道指导、后期指导）
  - 人物清单、场景清单

- `character_prompts` (dict): 人物提示词
  - 每个角色的中英双版文生图提示词
  - 包含面部、体型、服装、配饰、气质等全要素

- `scene_prompts` (dict): 场景提示词
  - 按镜头设置划分的场景角度
  - 每个场景的中英双版提示词

- `storyboard` (dict): 分镜头脚本
  - 每个剧情点的镜头序列
  - 包含插入镜头设计（细节/反应/环境/主观/转场）
  - 镜头参数、画面描述、台词、音频等

- `seedance_prompts` (dict): Seedance视频提示词
  - 段落式提示词，带时间标注
  - 电影级镜头控制（焦段、景别、机位、运镜、景深、前景、背景、光线）
  - 素材对应表

## 技能使用
- 所有节点均使用**大语言模型**技能 (`/skills/public/prod/llm`)
- 模型：`doubao-seed-2-0-pro-260215`
- 支持多模态理解和结构化输出

## 项目文件结构
```
src/
├── graphs/
│   ├── state.py                    # 状态定义
│   ├── graph.py                    # 图编排
│   └── nodes/
│       ├── director_notes_node.py
│       ├── character_design_node.py
│       ├── scene_design_node.py
│       ├── storyboard_node.py
│       └── seedance_prompts_node.py
config/
├── director_notes_cfg.json         # 导演讲戏模型配置
├── character_design_cfg.json       # 人物设计模型配置
├── scene_design_cfg.json           # 场景设计模型配置
├── storyboard_cfg.json             # 分镜头脚本模型配置
└── seedance_prompts_cfg.json       # 视频提示词模型配置
```

## 测试结果
✅ 测试通过 - 工作流成功执行，输出了完整的导演讲戏本、人物提示词、场景提示词、分镜头脚本和Seedance视频提示词
