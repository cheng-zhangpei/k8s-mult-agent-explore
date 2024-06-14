import os

from autogen import ConversableAgent


import global_interface.global_config

from pydantic import BaseModel, Field
from typing import Annotated, Literal

from tools.file_sys_tool import yaml_space

Operator = Literal["+", "-", "*", "/"]
def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")
def write(file_name: Annotated[str, "Yaml Configuration file path"],
                    file_content: Annotated[str, "the content you wanna write into the yaml file"]) -> bool:
    """
    写yaml文件
    :param file_name: 文件名
    :param file_content: 要写入的文件内容，应为字典类型
    :return: 如果文件写入成功返回True，否则返回False
    """
    try:
        file_path_to_write = os.path.join(yaml_space, file_name)
        with open(file_path_to_write, 'w', encoding='utf-8') as file:
            file.write(file_content)
        return True
    except Exception as e:
        print(f"写入YAML文件时发生错误: {e}")
        return False
# Let's first define the assistant agent that suggests tool calls.
assistant = ConversableAgent(
    name="Assistant",
    system_message="you should generate yaml file according to the user demand,"
                   "\the yaml is use for k8s resource define,and you must write file into the work space",
    llm_config={"config_list": global_interface.global_config.GLOBAL_MODEL_CONFIG_2},
)

# The user proxy agent is used for interacting with the assistant agent
# and executes tool calls.
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# Register the tool signature with the assistant agent.
assistant.register_for_llm(name="write", description="to tool for write the k8s yaml file")(write)

# Register the tool function with the user proxy agent.
user_proxy.register_for_execution(name="write")(write)


from autogen import register_function

# Register the calculator function to the two agents.
register_function(
    write,
    caller=assistant,  # The assistant agent can suggest calls to the calculator.
    executor=user_proxy,  # The user proxy agent can execute the calculator calls.
    name="write",  # By default, the function name is used as the tool name.
    description="a tool for write the file into the yaml space",  # A description of the tool.
)

print(assistant.llm_config["tools"])
chat_result = user_proxy.initiate_chat(assistant, message="I wanna deploy a nginx service with 3 replicas and nodeport service type")