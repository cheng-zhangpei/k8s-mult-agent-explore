"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2024/5/19 18:26
"""
import os
import tempfile

from autogen import ConversableAgent, GroupChat, GroupChatManager
from autogen.coding import LocalCommandLineCodeExecutor
from global_interface import global_config
from global_interface.prompt_engineer import yaml_executor_system_message

initializer_temp = ConversableAgent(
    "initializer_temp",
    llm_config={"config_list": global_config.GLOBAL_MODEL_CONFIG},
    human_input_mode="ALWAYS",  # always ask for human input
)

# Create a local command line code executor.
executor = LocalCommandLineCodeExecutor(
    timeout=25,  # Timeout for each code execution in seconds.
    work_dir=os.path.abspath(global_config.CODESPACE_WORKSPACE_PATH),  # 指定代码生成器的工作路径
)

# Create an agent with code executor configuration.
code_executor_agent = ConversableAgent(
    "code_executor_agent",
    system_message=yaml_executor_system_message,
    llm_config={"config_list": global_config.GLOBAL_MODEL_CONFIG},
    # 打开这个agent是为了从工作路径中拿到文件
    code_execution_config={"executor": executor},  # Use the local command line code executor.
    human_input_mode="ALWAYS",  # Always take human input for this agent for safety.
)
code_executor_agent.description = ("code executor, if previous chat pass the code format content,you can pass the file "
                                   "here to execute them")
