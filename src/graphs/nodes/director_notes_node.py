import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import DirectorNotesInput, DirectorNotesOutput


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


def director_notes_node(state: DirectorNotesInput, config: RunnableConfig, runtime: Runtime[Context]) -> DirectorNotesOutput:
    """
    title: 导演讲戏
    desc: 分析剧本，生成导演工作单，包含表演指导、美术指导、摄影指导、灯光指导、服化道指导、后期指导
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

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "script_content": state.script_content,
        "episode_number": state.episode_number,
        "visual_style": state.visual_style,
        "project_type": state.project_type,
        "target_language": state.target_language or "中文"
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
            max_completion_tokens=llm_config.get("max_completion_tokens", 8000),
            thinking=llm_config.get("thinking", "disabled")
        )
        
        # 解析响应内容
        content = get_text_content(response.content)
        
        # 尝试解析JSON，如果失败则将内容作为字符串返回
        try:
            director_notes = json.loads(content)
        except json.JSONDecodeError:
            # 如果不是JSON格式，将文本内容包装为结构化数据
            director_notes = {
                "episode": state.episode_number,
                "raw_content": content,
                "plot_points": [],
                "character_list": [],
                "scene_list": []
            }
            
    except Exception as e:
        # 错误处理
        director_notes = {
            "episode": state.episode_number,
            "error": str(e),
            "plot_points": [],
            "character_list": [],
            "scene_list": []
        }

    return DirectorNotesOutput(director_notes=director_notes)
