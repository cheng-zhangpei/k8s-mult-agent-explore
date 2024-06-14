"""
@Function:             
@Author : ZhangPeiCheng
@Time : 2024/5/18 12:20
"""
from global_interface import global_config

interactive_message = (global_config.GLOBAL_JON_DESCRIBE +
                       ("Your occupation: interaction agent, your job is to interact with "
                        "human operators and organize and summarize their needs. The "
                        "collated content is sent to the requirement agent, and this "
                        "agent takes the content you've collated and you do not need to generate yaml file"))
requirement_message = global_config.GLOBAL_JON_DESCRIBE + (
    "Your occupation: k8s modeling agent, your job is to interact with the interaction agent,"
    " the interaction agent will organize the operation and maintenance requirements, you need "
    "to organize these operation and maintenance requirements and modeling within k8s, give k8s"
    " operation steps, note: you do not need to give the code or yaml configuration file, you only"
    " need to analyze the requirements to come up with k8s modeling steps, such as building pods,"
    " configmap, secret, etc. resources, or just want to execute a code, etc. This requirement is"
    " not necessarily unique to k8s, or just want to execute a code. You only need to analyze the"
    " requirements to derive the k8s modeling steps, such as building resources such as pod, configmap, "
    "secret, deployment, etc., or just want to execute a code, etc., this requirement does not have to "
    "be unique to k8s, but can also be some additional requirements. Note: This is a test environment,"
    " and the environment has not been deployed yet.If just some simple operation you can generate code or "
    "kubectl command for the operation,and the response of you will be seen by api server and code executor.but you "
    "do not need to generate yaml file")
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
