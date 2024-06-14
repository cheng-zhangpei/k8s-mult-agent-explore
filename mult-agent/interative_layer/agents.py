"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2024/5/18 12:18
"""
import os

from autogen import ConversableAgent, AssistantAgent, GroupChat, GroupChatManager


from global_interface import global_config
from global_interface.global_config import GLOBAL_MODEL_CONFIG_2, GLOBAL_MODEL_CONFIG
from global_interface.prompt_engineer import interactive_system_message, requirement_agent_system_message

interactive_agent_model_config = [
    {
        "model": "chengzipi/huggingface",
        "base_url": "http://127.0.0.1:11435/v1",
        "api_key": "ollama",
    }
]
requirement_agent_model_config = [
    {
        "model": "chengzipi/huggingface",
        "base_url": "http://127.0.0.1:11435/v1",
        "api_key": "ollama",
    }
]

# 定义一个交互的agent
# 对话是永远无法被终止的，因为这里设计的是一个交互循环?
# 我感觉需要保存对话，对话似乎并不会一直无法终止，每次对话需要加载上一次终止的对话
# 避免忘记对话很可能会用到RAG的思维


# 这两个agent用groupManager来进行管理，并控制智能体顺序工作流
interactive_agent = ConversableAgent(
    "interactive_agent",
    system_message=interactive_system_message,
    llm_config={"config_list": GLOBAL_MODEL_CONFIG_2},
    human_input_mode="ALWAYS",  # ALWAYS ask for human input.
)

requirement_agent = AssistantAgent(
    "requirement_agent",
    system_message=requirement_agent_system_message,
    llm_config={"config_list": GLOBAL_MODEL_CONFIG_2},
    human_input_mode="ALWAYS",  # ALWAYS ask for human input.
)

