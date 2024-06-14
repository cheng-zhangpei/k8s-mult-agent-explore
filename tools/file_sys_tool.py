"""
@Function:  这个tool用于设计agent文件系统工具，让ai能够读写文件，从而操作文件系统
@Author : ZhangPeiCheng
@Time : 2024/5/22 10:21
"""
import os

import yaml

from typing import Annotated
from global_interface import global_config
from global_interface.response_code import TASK_SUCCEED, TOOL_ERROR

yaml_space = global_config.YAML_WORKSPACE_PATH


def read_file_yaml(file_name: Annotated[str, "Yaml Configuration file path"]) -> bool:
    """
    读取yaml文件
    :param file_name: 生成的文件名
    :return:
    """
    try:
        file_path = os.path.join(yaml_space, file_name)
        print("文件read路径： " + file_path)
        with open(file_path, 'r', encoding='utf-8') as file:
            # 加载yaml文件内容
            data = yaml.safe_load(file)
            print("YAML文件内容:", data)
            return True
    except Exception as e:
        print(f"读取YAML文件时发生错误: {e}")
        return False


def write_file_yaml(file_name: Annotated[str, "Yaml Configuration file path"],
                    file_content: Annotated[str, "the content you wanna write into the yaml file"]) -> bool:
    """
    写yaml文件
    :param file_name: 文件名
    :param file_content: 要写入的文件内容，应为字典类型
    :return: 如果文件写入成功返回True，否则返回False
    """
    try:
        yaml_space = global_config.YAML_WORKSPACE_PATH
        file_path_to_write = os.path.join(yaml_space, file_name)
        print(file_path_to_write)
        with open(file_path_to_write, 'w', encoding='utf-8') as file:
            file.write(file_content)
        return TASK_SUCCEED
    except Exception as e:
        print(f"写入YAML文件时发生错误: {e}")
        return TOOL_ERROR

if __name__ == "__main__":
    yaml_content = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:latest
        ports:
        - containerPort: 80
    """
    # 调用函数写入文件
    file_name_to_write = "nginx_deployment.yaml"

    # 确保yaml_space目录存在
    if not os.path.exists(yaml_space):
        os.makedirs(yaml_space)

    # 写入YAML文件
    write_success = write_file_yaml(file_name_to_write, yaml_content)

    if write_success:
        print(f"文件 '{file_name_to_write}' 写入成功。")
    else:
        print(f"文件 '{file_name_to_write}' 写入失败。")



