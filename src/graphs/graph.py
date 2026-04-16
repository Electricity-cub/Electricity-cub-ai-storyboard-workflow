from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)

# 导入所有节点
from graphs.nodes.director_notes_node import director_notes_node
from graphs.nodes.character_design_node import character_design_node
from graphs.nodes.scene_design_node import scene_design_node
from graphs.nodes.storyboard_node import storyboard_node
from graphs.nodes.seedance_prompts_node import seedance_prompts_node


# 创建状态图，指定图的入参和出参
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("director_notes", director_notes_node,
                 metadata={"type": "agent", "llm_cfg": "config/director_notes_cfg.json"})

builder.add_node("character_design", character_design_node,
                 metadata={"type": "agent", "llm_cfg": "config/character_design_cfg.json"})

builder.add_node("scene_design", scene_design_node,
                 metadata={"type": "agent", "llm_cfg": "config/scene_design_cfg.json"})

builder.add_node("storyboard", storyboard_node,
                 metadata={"type": "agent", "llm_cfg": "config/storyboard_cfg.json"})

builder.add_node("seedance_prompts", seedance_prompts_node,
                 metadata={"type": "agent", "llm_cfg": "config/seedance_prompts_cfg.json"})

# 设置入口点
builder.set_entry_point("director_notes")

# 添加边 - 导演讲戏后，人物设计和场景设计可以并行执行
builder.add_edge("director_notes", "character_design")
builder.add_edge("director_notes", "scene_design")

# 分镜头脚本也依赖导演讲戏本
builder.add_edge("director_notes", "storyboard")

# 人物设计、场景设计、分镜头脚本都完成后，进入视频提示词生成
builder.add_edge(["character_design", "scene_design", "storyboard"], "seedance_prompts")

# 视频提示词生成后结束
builder.add_edge("seedance_prompts", END)

# 编译图
main_graph = builder.compile()
