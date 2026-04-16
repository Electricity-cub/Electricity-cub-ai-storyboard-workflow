import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import SceneDesignInput, SceneDesignOutput


def get_text_content(content):
    """安全提取文本内容的辅助函数"""
    if isinstance(content, str):
        return content
    elif isinstance(content, list):
        if content and isinstance(content[0], str):
            return " ".join(content)
        else:
            return " ".join(item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text")
    return str(content)


def scene_design_node(state: SceneDesignInput, config: RunnableConfig, runtime: Runtime[Context]) -> SceneDesignOutput:
    """
    title: 场景提示词设计
    desc: 基于导演讲戏本，按镜头设置为每个场景角度编写中英双版文生图提示词
    integrations: 大语言模型
    """
    ctx = runtime.context

    # 读取配置文件
    cfg_file = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config['metadata']['llm_cfg'])
    with open(cfg_file, 'r') as fd:
        _cfg = json.load(fd)

    llm_config = _cfg.get("config", {})
    sp = _cfg.get("sp", "")
    up = _cfg.get("up", "")

    # 提取场景相关信息
    art_directive = state.director_notes.get("art_directive", {}) if state.director_notes else {}
    camera_directive = state.director_notes.get("camera_directive", {}) if state.director_notes else {}
    lighting_directive = state.director_notes.get("lighting_directive", {}) if state.director_notes else {}

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "director_notes": json.dumps(state.director_notes, ensure_ascii=False, indent=2) if state.director_notes else "{}",
        "visual_style": state.visual_style,
        "art_directive": json.dumps(art_directive, ensure_ascii=False) if art_directive else "{}",
        "camera_directive": json.dumps(camera_directive, ensure_ascii=False) if camera_directive else "{}",
        "lighting_directive": json.dumps(lighting_directive, ensure_ascii=False) if lighting_directive else "{}"
    })

    # 调用LLM
    client = LLMClient(ctx=ctx)
    
    messages = [
        SystemMessage(content=sp),
        HumanMessage(content=user_prompt_content)
    ]
    
    try:
        response = client.invoke(
            messages=messages,
            model=llm_config.get("model", "doubao-seed-2-0-pro-260215"),
            temperature=llm_config.get("temperature", 0.7),
            top_p=llm_config.get("top_p", 0.9),
            max_completion_tokens=llm_config.get("max_completion_tokens", 6000),
            thinking=llm_config.get("thinking", "disabled")
        )
        
        # 解析响应内容
        content = get_text_content(response.content)
        
        # 尝试解析JSON，如果失败则将内容作为字符串返回
        try:
            scene_prompts = json.loads(content)
        except json.JSONDecodeError:
            scene_prompts = {
                "scenes": [],
                "raw_content": content
            }
            
    except Exception as e:
        # 错误处理
        scene_prompts = {
            "scenes": [],
            "error": str(e)
        }

    return SceneDesignOutput(scene_prompts=scene_prompts)
