"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2024/5/18 12:19
"""
from global_interface import global_config

yaml_generator_job_describe = (global_config.GLOBAL_JON_DESCRIBE +
                               ("Your occupation: yaml configuration file generation. You will receive the output from "
                                "the require agent, this output is the K8S modeling of the user requirements, that is, "
                                "the user requirements are translated into k8s cluster operation steps and resources, "
                                "you need to generate the exact yaml file based on the requirements of the other "
                                "intelligences and, the content of your output will be connected to the yaml executor "
                                "agent, which is passed through the kubectl command to operate the cluster (this is a "
                                "test environment, later will add RAG, there will be a series of private database data "
                                "to assist in generating yaml files,The final call to write_file_yaml saves the "
                                "produced yaml file to the workspace for subsequent calls and processing.If you do "
                                "not find the registered tool let me know)"))

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
