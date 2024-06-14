"""
@Function: 用于记录全局
@Author : ZhangPeiCheng
@Time : 2024/5/19 18:13
"""
import os
from typing import List, Dict

# 工作空间的全局地址
CLUSTER_INFO_WORKSPACE_PATH = os.path.abspath('../work-space/cluster-info')
CODESPACE_WORKSPACE_PATH = '../work-space/code-space'
ROLL_BACK_WORKSPACE_PATH = '../work-space/roll-back-record'
YAML_WORKSPACE_PATH = os.path.abspath('../work-space/yaml-space')
GLOBAL_JON_DESCRIBE = ("Overall mission: intelligent detection and operation of kubernetes clusters "
                       "through multi-intelligence collaboration. You are all members of the intelligences,"
                       " each of which has its own task, and through your interactions you can realize the "
                       "operation and maintenance of container orchestration clusters.Attention! All of the agent "
                       "should return response code according to the situation of the mission")

GLOBAL_MODEL_CONFIG: list[dict[str, str]] = [
    {
        "model": "global",
        "base_url": "http://127.0.0.1:11435/v1",
        "api_key": "chengzipi",
    }
]


GLOBAL_MODEL_CONFIG_2 = [
    {
        "model": "gpt-3.5-turbo",
        "base_url": "https://api.kwwai.top/v1",
        "api_key": "sk-Ipa77PaviJC1OVAj745cBb980f894c0485A748675e96379a",
    }
]


REDIS_KEY = "cluster-info-summary"


