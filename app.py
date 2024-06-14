import sys

from flask import Flask, request, jsonify
from openai import OpenAI


app = Flask(__name__)
modelfile = '''
FROM  ./static/models/Meta-Llama-3-70B-Instruct.Q3_K_S.gguf
PARAMETER temperature 0.1
PARAMETER stop "AI assistant:"
PARAMETER stop "---"
PARAMETER stop "==="
PARAMETER top_k 10
PARAMETER top_p 0.15
PARAMETER num_predict 1256
'''
# 用于接收模型的输出并进行清洗
# FROM D:\\czp\k8s-mult-agent\\resource\\models\\chengzipi\\huggingface\\Meta-Llama-3-70B-Instruct.Q3_K_S.gguf
client = OpenAI(base_url="http://localhost:11434/v1", api_key="lm-studio")


def transform_response(completion):
    # 将模型响应转换为OpenAI格式
    openai_formatted_response = {
        "id": completion.id,
        "object": completion.object,
        "created": completion.created,
        "model": completion.model,
        "choices": [
            {
                "message": completion.choices[0].message.content,
                "role": completion.choices[0].message.role,
                "index": completion.choices[0].index,
                "logprobs": None,  # 如果你的模型不提供logprobs，可以设置为None或者相应的值
                "finish_reason": completion.choices[0].finish_reason
            }
        ],
        "usage": {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens
        }
    }
    return openai_formatted_response


# 需要按照openai格式进行暴露大模型服务
@app.route('/v1/chat/completions', methods=['POST'])
def completions():
    # Example: reuse your existing OpenAI setup
    # 从请求中获取消息
    data = request.json
    messages = data['messages']
    completion = client.chat.completions.create(
        model="chengzipi/huggingface",
        messages=messages,
        temperature=0.7,
    )
    print("model response: " + completion.choices[0].message.content)
    openai_response = transform_response(completion)
    return openai_response


# 如果是主程序，则启动服务
if __name__ == '__main__':
    app.run()
