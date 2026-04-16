import os
import json
from jinja2 import Template
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import LLMClient
from graphs.state import SeedancePromptsInput, SeedancePromptsOutput


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


def seedance_prompts_node(state: SeedancePromptsInput, config: RunnableConfig, runtime: Runtime[Context]) -> SeedancePromptsOutput:
    """
    title: Seedance视频提示词生成
    desc: 将分镜头脚本转化为Seedance 2.0可执行的镜头指令式提示词
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

    # 建立素材对应表
    asset_mapping = []
    if state.character_prompts.get("characters"):
        for idx, char in enumerate(state.character_prompts["characters"], 1):
            asset_mapping.append({
                "id": f"@图片{idx}",
                "type": "人物",
                "name": char.get("name", "")
            })

    if state.scene_prompts.get("scenes"):
        scene_start = len(asset_mapping) + 1
        for idx, scene in enumerate(state.scene_prompts["scenes"], scene_start):
            asset_mapping.append({
                "id": f"@图片{idx}",
                "type": "场景",
                "name": scene.get("name", "")
            })

    # 格式化素材对应表字符串
    asset_mapping_str = ""
    for asset in asset_mapping:
        asset_mapping_str += f"{asset['id']} - {asset['type']}: {asset['name']}\n"

    # 使用jinja2模板渲染提示词
    up_tpl = Template(up)
    user_prompt_content = up_tpl.render({
        "storyboard": json.dumps(state.storyboard, ensure_ascii=False, indent=2) if state.storyboard else "{}",
        "director_notes": json.dumps(state.director_notes, ensure_ascii=False, indent=2) if state.director_notes else "{}",
        "asset_mapping": asset_mapping_str,
        "project_type": state.project_type
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
            temperature=llm_config.get("temperature", 0.5),
            top_p=llm_config.get("top_p", 0.9),
            max_completion_tokens=llm_config.get("max_completion_tokens", 12000),
            thinking=llm_config.get("thinking", "disabled")
        )
        
        # 解析响应内容
        content = get_text_content(response.content)
        
        # 尝试解析JSON，如果失败则将内容作为字符串返回
        try:
            seedance_prompts = json.loads(content)
        except json.JSONDecodeError:
            seedance_prompts = {
                "project_info": {
                    "visual_style": state.director_notes.get("visual_style", "") if state.director_notes else "",
                    "project_type": state.project_type
                },
                "asset_mapping": asset_mapping,
                "plot_points": [],
                "raw_content": content
            }
            
    except Exception as e:
        # 错误处理
        seedance_prompts = {
            "project_info": {
                "visual_style": state.director_notes.get("visual_style", "") if state.director_notes else "",
                "project_type": state.project_type
            },
            "asset_mapping": asset_mapping,
            "plot_points": [],
            "error": str(e)
        }

    return SeedancePromptsOutput(seedance_prompts=seedance_prompts)
