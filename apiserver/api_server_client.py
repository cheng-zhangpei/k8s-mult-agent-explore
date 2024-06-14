"""
@Function:  用于访问k8s的客户端从而进行集群操作，测试与集群的链接以及api操作效果
@Author : ZhangPeiCheng
@Time : 2024/5/18 12:56
"""

from kubernetes import config,client
config.load_kube_config(config_file="./config/config")
# 创建API的CoreV1Api实例
v1 = client.CoreV1Api()
