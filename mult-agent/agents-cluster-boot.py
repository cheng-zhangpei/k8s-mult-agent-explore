"""
@Function: 整体上使用 sequence pattern 进行整体的对话布局
前后会进行carryover的形式来进行不同智能体的前后信息传递
@Author : ZhangPeiCheng
@Time : 2024/5/12 19:04
"""
import os
from typing import Annotated

import yaml
from autogen import ConversableAgent, GroupChat, GroupChatManager, register_function

from global_interface.global_config import CLUSTER_INFO_WORKSPACE_PATH
from global_interface.response_code import RESOURCE_ERROR, YAML_MOBILIZE, CLUSTER_SITUATION_SUMMARY, CODE_EXECUTE_ERROR, \
    TASK_SUCCEED, API_CALL_ERROR, HUMAN_INPUT_UNSATISFIED, GET_CLUSTER_INFO
from interative_layer.agents import interactive_agent, requirement_agent
from global_interface import global_config
from function_layer.agents import code_writer_agent, yaml_writer, cluster_info_supervisor
from operation_layer.agents import code_executor_agent
from tools import file_sys_tool
from tools.file_sys_tool import yaml_space

# 整个agent工作流的起始

initializer = ConversableAgent(
    "User ",
    llm_config=False,  # no LLM used for human proxy
)

# 整体工作流定义
# 注意一下，很多拓展功能在这个位置都可以通过自定义工作流-->这个自定义功能非常强大，也是本循环的核心流程
# 记住chat_group其实就是一个中转器,可以再发向下一个agent的时候添加入相关的信息

"""
1. 比如requirement的制定需要集群信息的辅助决策
2. 整个工作流你们不应该有None，我可以让流程的最低点反过来调用interactive_agent
"""


def check_messages_content(messages):
    for message in messages:
        message['content'] = 'tool call success'
    return messages


def validate_message_format(messages):
    valid_messages = []
    for message in messages:
        # 检查每个消息对象是否只包含 'content' 字段
        if set(message.keys()) == {'content'}:
            valid_messages.append(message)
        else:
            print("发现格式不正确的消息对象:", message)
    return valid_messages


def clean_messages(messages):
    cleaned_messages = []
    for message in messages:
        # 工具调用这个openai的接口在ollama中是无法使用的
        if 'tool_calls' in message or 'tool_responses' in message:
            continue
        if message['content'] == '':
            continue
        cleaned_messages.append(message)
    return cleaned_messages


def state_transition(last_speaker, groupchat):
    try:
        last_message_content = groupchat.messages[-1]["content"]
    except:
        last_message_content = "-1"
        print("the agent do not have any response")
    last_space_index = last_message_content.rfind('2021')
    code_str = last_message_content[last_space_index:]
    try:
        response_code_int = int(code_str)
    except:
        response_code_int = -1
        print("此智能体不产生响应码参与集群工作流")
    if last_speaker is interactive_agent:
        # retrieve: action 1 -> action 2
        # 获得集群信息 ->  调用supervisor -> requirement agent
        if not os.path.exists(os.path.join(CLUSTER_INFO_WORKSPACE_PATH, "cluster_info")):
            # 调用supervisor agent
            print("集群信息不存在")
        # 将集群信息加入message中传递给requirement
        # 如果存在
        # 获取缓冲区数据
        # 解析缓冲区数据之后将数据拼接到智能体token开头
        return requirement_agent
    elif last_speaker is requirement_agent:
        if response_code_int == RESOURCE_ERROR:
            # 资源不足,将信息返回给用户
            return interactive_agent
        if response_code_int == YAML_MOBILIZE:
            # 允许进行yaml文件和代码的编写
            return code_writer_agent
        if response_code_int == CLUSTER_SITUATION_SUMMARY:
            # 触发集群资源的获取
            return code_writer_agent
        if response_code_int == CODE_EXECUTE_ERROR:
            # 代码执行失败->重新进行代码的编写
            return code_writer_agent
        if response_code_int == TASK_SUCCEED:
            # 成功完成用户任务
            return interactive_agent
        if response_code_int == API_CALL_ERROR:
            # api调用失败
            return interactive_agent
        if response_code_int == GET_CLUSTER_INFO:
            # 调用从而获得集群信息并返回
            return cluster_info_supervisor
        if response_code_int == HUMAN_INPUT_UNSATISFIED:
            # 人类的需求无法被集群操作或是会对分布式集群产生生产风险则将需求驳回
            return interactive_agent
        # 如果是用户闲聊传递过来的就再传递回去
        return interactive_agent
    elif last_speaker is code_writer_agent:
        if response_code_int == TASK_SUCCEED:
            # 这个地方我估计就是不同agent的局限性了，我估计这个地方是有请求的兼容性问题的
            return requirement_agent
        # 代码生成器生成之后的code直接传递给执行器就ok了
        # 这个地方只需要调用一层工具就好了，如果需要重新调用工具则需要requirement agent来进行调度
        return yaml_writer
    elif last_speaker is yaml_writer:
        # 工具调用失败则需要重新生成文件
        if response_code_int == TASK_SUCCEED:
            # 这个地方我估计就是不同agent的局限性了，我估计这个地方是有请求的兼容性问题的
            # 这个地方需要去调用执行器
            return requirement_agent
        else:
            return code_writer_agent
    elif last_speaker is code_executor_agent:
        # 执行器如果执行正常就直接返回requirement agent
        if last_message_content is TASK_SUCCEED:
            # 此处需要构造一个message信息，因为工具调用会让message为空而报错
            return requirement_agent
        else:
            return code_writer_agent
    elif last_speaker is cluster_info_supervisor:
        return requirement_agent

# 用一组groupChat将工作流包裹起来
# framework_group_chat = GroupChat(
#     agents=[initializer, interactive_agent, requirement_agent, function_group_manger, operation_group_manger],
#     messages=[],
#     max_round=20,
#     speaker_selection_method="round_robin",
#     # allow_repeat_speaker = False
# )
# agent workflow control

# allowed_transitions = {
#     initializer: [interactive_agent],
#     interactive_agent: [requirement_agent],
#     requirement_agent: [code_writer_agent],
# }
framework_chat = GroupChat(
    agents=[initializer, interactive_agent, requirement_agent, code_writer_agent, code_executor_agent, yaml_writer,cluster_info_supervisor],
    messages=[],
    max_round=12,
    send_introductions="False",
    speaker_selection_method=state_transition,
)

framework_manger = GroupChatManager(
    groupchat=framework_chat,
    llm_config={"config_list": global_config.GLOBAL_MODEL_CONFIG_2},
    human_input_mode="ALWAYS    ",
)

if __name__ == "__main__":
    interactive_agent.initiate_chat(
        framework_manger,
    )
