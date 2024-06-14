"""
@Function: we define a series of response code for the workflow design
真的很想吐槽，工作流现在已经很复杂了,这是在造核弹啊
直接用学号当响应码也是很无敌....

@Author : ZhangPeiCheng
@Time : 2024/5/25 19:42
"""
# 集群资源不足
RESOURCE_ERROR = 2021213320371
# 工具响应异常
TOOL_ERROR = 2021213320372
# 调用code generator
YAML_MOBILIZE = 2021213320373
# 调用api client agent
API_CLIENT_MOBILIZE = 2021213320374
# 调用集群资源概括agent
CLUSTER_SITUATION_SUMMARY = 2021213320375
# 代码/yaml文件执行错误
CODE_EXECUTE_ERROR = 2021213320376
# 任务执行成功
TASK_SUCCEED = 2021213320377
# api调用错误
API_CALL_ERROR = 2021213320378
# 人祸——用户输入很奇怪，智能体认为无法进行建模
HUMAN_INPUT_UNSATISFIED = 2021213320379
# 获取集群信息
GET_CLUSTER_INFO = 2021213320380



