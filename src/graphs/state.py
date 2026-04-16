from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# 全局状态定义
class GlobalState(BaseModel):
    """全局状态定义"""
    # 输入字段
    script_content: str = Field(default="", description="剧本内容")
    episode_number: str = Field(default="ep01", description="集数")
    visual_style: str = Field(default="写实", description="视觉风格：3D CG | 国漫 | 日漫 | 写实")
    project_type: str = Field(default="国内短剧", description="项目类型：国内短剧 | 海外短剧 | 国内动漫剧 | 海外动漫剧")
    target_language: Optional[str] = Field(default=None, description="目标语言（海外剧时）：英文 | 日文 | 其他")

    # 中间产物
    director_notes: dict = Field(default={}, description="导演讲戏本")
    character_prompts: dict = Field(default={}, description="人物提示词")
    scene_prompts: dict = Field(default={}, description="场景提示词")
    storyboard: dict = Field(default={}, description="分镜头脚本")

    # 最终输出
    seedance_prompts: dict = Field(default={}, description="Seedance视频提示词")


# 图输入定义
class GraphInput(BaseModel):
    """工作流的输入"""
    script_content: str = Field(..., description="剧本内容")
    episode_number: str = Field(default="ep01", description="集数")
    visual_style: str = Field(default="写实", description="视觉风格：3D CG | 国漫 | 日漫 | 写实")
    project_type: str = Field(default="国内短剧", description="项目类型：国内短剧 | 海外短剧 | 国内动漫剧 | 海外动漫剧")
    target_language: Optional[str] = Field(default=None, description="目标语言（海外剧时）")


# 图输出定义
class GraphOutput(BaseModel):
    """工作流的输出"""
    director_notes: dict = Field(..., description="导演讲戏本")
    character_prompts: dict = Field(..., description="人物提示词")
    scene_prompts: dict = Field(..., description="场景提示词")
    storyboard: dict = Field(..., description="分镜头脚本")
    seedance_prompts: dict = Field(..., description="Seedance视频提示词")


# ============ 节点输入输出定义 ============

# 1. 导演讲戏节点
class DirectorNotesInput(BaseModel):
    """导演讲戏节点的输入"""
    script_content: str = Field(..., description="剧本内容")
    episode_number: str = Field(..., description="集数")
    visual_style: str = Field(..., description="视觉风格")
    project_type: str = Field(..., description="项目类型")
    target_language: Optional[str] = Field(default=None, description="目标语言")


class DirectorNotesOutput(BaseModel):
    """导演讲戏节点的输出"""
    director_notes: dict = Field(..., description="导演讲戏本")


# 2. 人物设计节点
class CharacterDesignInput(BaseModel):
    """人物设计节点的输入"""
    director_notes: dict = Field(..., description="导演讲戏本")
    script_content: str = Field(..., description="剧本内容")
    visual_style: str = Field(..., description="视觉风格")


class CharacterDesignOutput(BaseModel):
    """人物设计节点的输出"""
    character_prompts: dict = Field(..., description="人物提示词")


# 3. 场景设计节点
class SceneDesignInput(BaseModel):
    """场景设计节点的输入"""
    director_notes: dict = Field(..., description="导演讲戏本")
    visual_style: str = Field(..., description="视觉风格")


class SceneDesignOutput(BaseModel):
    """场景设计节点的输出"""
    scene_prompts: dict = Field(..., description="场景提示词")


# 4. 分镜头脚本节点
class StoryboardInput(BaseModel):
    """分镜头脚本节点的输入"""
    director_notes: dict = Field(..., description="导演讲戏本")
    script_content: str = Field(..., description="剧本内容")
    visual_style: str = Field(..., description="视觉风格")
    project_type: str = Field(..., description="项目类型")


class StoryboardOutput(BaseModel):
    """分镜头脚本节点的输出"""
    storyboard: dict = Field(..., description="分镜头脚本")


# 5. 视频提示词节点
class SeedancePromptsInput(BaseModel):
    """视频提示词节点的输入"""
    storyboard: dict = Field(..., description="分镜头脚本")
    director_notes: dict = Field(..., description="导演讲戏本")
    character_prompts: dict = Field(..., description="人物提示词")
    scene_prompts: dict = Field(..., description="场景提示词")
    project_type: str = Field(..., description="项目类型")


class SeedancePromptsOutput(BaseModel):
    """视频提示词节点的输出"""
    seedance_prompts: dict = Field(..., description="Seedance视频提示词")
