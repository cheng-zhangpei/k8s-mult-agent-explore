"""
@Function:   用于定义功能层智能体
@Author : ZhangPeiCheng
@Time : 2024/5/18 13:46
"""
import os
from typing import Annotated
from autogen import register_function

from autogen import GroupChat, ConversableAgent, GroupChatManager, register_function

from apiserver import get_cluster_info
from global_interface import global_config
from global_interface.prompt_engineer import yaml_generator_system_message, supervisor_agent_system_message
from tools import file_sys_tool
import global_interface

# =====================================================model config=============================================

yaml_generator_job_describe = (global_config.GLOBAL_JON_DESCRIBE +
                               ("Your occupation: yaml configuration file generation. You will receive the output from "
                                "the require agent, this output is the K8S modeling of the user requirements, that is, "
                                "the user requirements are translated into k8s cluster operation steps and resources, "
                                "you need to generate the exact yaml file based on the requirements of the other "
                                "intelligences and, the content of your output will be connected to the yaml executor "
                                "agent, which is passed through the kubectl command to operate the cluster (this is a "
                                "test environment, later will add RAG, there will be a series of private database data "
                                "to assist in generating yaml files.The final call to write_file_yaml saves the "
                                "produced yaml file to the workspace for subsequent calls and processing.you should "
                                "save the content by using the file-writer tool that I provide you.and remember just "
                                "generate a reliable yaml file name )"))

group_manager_model_config = [
    {
        "model": "groupManager",
        "base_url": "http://127.0.0.1:11435/v1",
        "api_key": "chengzipi",
    }
]

# 记录yaml生成器的config
yaml_generator_agent_model_config = [
    {
        "model": "chengzipi/huggingface",
        "base_url": "http://127.0.0.1:11435/v1",
        "api_key": "ollama",
    }
]

# =====================================================model define=============================================
# 集群信息监视器，该agent可以从redis中拿取集群信息并进行汇总分析
cluster_info_supervisor = ConversableAgent(
    "cluster_info_supervisor",
    system_message=supervisor_agent_system_message,
    llm_config={"config_list": global_interface.global_config.GLOBAL_MODEL_CONFIG_2},
    code_execution_config=False,  # Turn off code execution for this agent.
    human_input_mode="NEVER"
)

code_writer_agent = ConversableAgent(
    "yaml_generator",
    system_message=yaml_generator_system_message,
    llm_config={"config_list": global_interface.global_config.GLOBAL_MODEL_CONFIG_2},
    code_execution_config=False,  # Turn off code execution for this agent.
    human_input_mode="ALWAYS"
)

code_writer_agent.description = ("An agent dedicated to customized yaml file generation based on the requirements of a "
                                 "requirement agent.")


# =====================================================给大模型注册工具=============================================
# register function tool for all agents
def register_tool_for_agent(caller_agent, executor_agent, name, description, function):
    caller_agent.register_for_llm(name=name, description=description)(function)
    executor_agent.register_for_execution(name=name)(function)
    register_function(
        file_sys_tool.write_file_yaml,
        caller=caller_agent,
        executor=executor_agent,
        name=name,
        description=description,
    )


# -----------------------------------write_yaml_file----------------------------------------------------------------
# all of the tool agent define in the cluster
yaml_writer = ConversableAgent(
    name="yaml_writer",
    llm_config=False,
)
register_tool_for_agent(code_writer_agent, yaml_writer, "yaml_writer", "a tool for generating the yaml file of k8s"
                        , file_sys_tool.write_file_yaml)

# -----------------------------------get nodes overall information of the cluster ---------------------
get_node_info_tool = ConversableAgent(
    name="get_cluster_info_tool",
    llm_config=False,
)
register_tool_for_agent(cluster_info_supervisor, get_node_info_tool, "get_cluster_info_tool", "a tool for get the overall resource(cpu and memory) information of k8s nodes"
                        , get_cluster_info.get_cluster_node_info)
# ===============================================================================================================


if __name__ == "__main__":
    """单元测试"""
    print(code_writer_agent.llm_config["tools"])
