"""
@Function:  获取集群中各种资源信息的client
@Author : ZhangPeiCheng
@Time : 2024/6/8 20:00
"""
from api_server_client import v1, client


def transform_list_2_seq(list):
    """
    将多个列表合成为token（string）
    :param list:
    :return:
    """
    pass


def get_cluster_node_info():
    nodes = v1.list_node()
    nodes_resource = {}
    for node in nodes.items:
        # 获取节点的名称
        node_name = node.metadata.name
        # 获取节点的总CPU和内存容量
        cpu_capacity_str = node.status.capacity.get('cpu')
        memory_capacity_str = node.status.capacity.get('memory')
        print(cpu_capacity_str)
        # 转换内存容量为Ki
        memory_capacity_ki = int(memory_capacity_str.rstrip('Ki'))

        # 使用Metrics API获取节点的资源使用情况
        metrics = client.CustomObjectsApi().get_cluster_custom_object(
            group="metrics.k8s.io",
            version="v1beta1",
            plural="nodes",
            name=node_name)

        # 获取节点的CPU和内存使用量
        cpu_usage_str = metrics['usage']['cpu']
        cpu_usage_cores = int(cpu_usage_str.rstrip('n')) / 1e9  # 转换为核
        memory_usage_str = metrics['usage']['memory']

        # 转换CPU容量为纳核
        if 'm' in cpu_capacity_str:
            cpu_capacity = int(cpu_capacity_str.rstrip('m')) * 1e6  # 转换为纳核
        else:
            cpu_capacity = int(cpu_capacity_str) * 1e9  # 假设单位为核心数

        #  转换CPU使用量为纳核
        cpu_usage = int(cpu_usage_str.rstrip('n'))

        #  计算剩余资源占比
        cpu_remaining_percent = (1 - cpu_usage / cpu_capacity) * 100
        # 转换内存使用量为Ki
        memory_usage_ki = int(memory_usage_str.rstrip('Ki'))
        # 计算内存剩余资源占比
        memory_remaining_percent = (1 - memory_usage_ki / memory_capacity_ki) * 100
        memory_remaining_value = (memory_capacity_ki- memory_usage_ki) / 1024
        cpu_remaining_value = int(cpu_capacity_str) - cpu_usage_cores
        # 更新nodes_resource字典
        nodes_resource["node:" + node_name + " memory_remaining_value"] = str(memory_remaining_value) + "Mi"
        nodes_resource["node:" + node_name + " cpu_remaining_value"] = str(cpu_remaining_value) + "cores"
        nodes_resource["node:" + node_name + " memory_remaining_percent"] = f"内存剩余占比: {memory_remaining_percent:.2f}%"
        nodes_resource["node:" + node_name + " cpu_remaining_percent"] = f"CPU剩余占比: {cpu_remaining_percent:.2f}%"
    return nodes_resource

def cluster_detail_info():
    """使用普罗米修斯逐渐进行精细化控制"""
    pass

def get_pod_list():
    pass
def get_statefulset_list():
    pass
def get_namespace_list():
    pass
def get_deployment_list():
    pass
def get_service_list():
    pass
def get_pv_list():
    pass
def get_pvc_list():
    pass


def get_pod_info(pod_name):
    pass
def get_statefulset_info(statefulset_name):
    pass

def get_namespace_info(namespace_name):
    pass

def get_deployment_info(deployment_name):
    pass

def get_service_info(service_name):
    pass

def get_pv_info(pv_name):
    pass

def get_pvc_info(pvc_name):
    pass



if __name__ == "__main__":
    nodes_resource = get_cluster_node_info()
    print(nodes_resource)
