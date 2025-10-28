# Created by erainm on 2025/10/28 10:11.
# IDE：PyCharm 
# @Project: agent_project
# @File：call_tools01
# @Description:

import json
import time
import ollama
from config import conf
from dashscope import Generation

# 调用本地模型 - qwen3:4b
def call_ollama_model(prompt):
    response = ollama.chat(
        model='qwen3:4b',
        messages=[{"role": "user", "content": prompt}]
    )
    print(response['message']['content'])
    return response['message']['content']

# 调用LLM
def call_llm_model(prompt):
    messages = [{"role": "user", "content": prompt}]
    # 增加重试机制
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = Generation.call(
                api_key=conf.DASHSCOPE_API_KEY,
                model=conf.LLM_MODEL,
                messages=messages,
                enable_thinking=False,
                # 添加超时设置
                timeout=30000  # 30秒超时
            )
            print(response['output']['text'])
            return response['output']['text']
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # 指数退避
            else:
                # 所有重试都失败后返回默认值或抛出异常
                print("All retry attempts failed, returning empty string")
                return ""  # 或者返回一个默认的JSON字符串

def check_tools(query):
    prompt = (
        """
        你是一位可靠的个人助理，现在为你提供【工具集】，根据【用户问题】判断是否需要使用工具，并按照【指定格式】输出。
        【工具集】
        [getTrainSchedule]
        getTrainSchedule的作用是根据指定日期、起点城市名称和重点城市名称，查询列车班次
        
        【指定格式】
        {"是否需要调用【工具集】中的工具":"是",
        "需要调用的工具名称":"getTrainSchedule",
        "调用工具需要的参数":{"query_date":"10月29日","start_station":"武汉","end_station":"青海"}}
        
        【用户问题】
        """ + query
    )
    toolCall = call_llm_model(prompt)
    return toolCall

def call_tools(toolCall):
    with open("tools.py", "r", encoding="utf-8") as f:
        content = f.read()
    argsStr = ",".join(str(key)+'="'+toolCall["调用工具需要的参数"][key]+'"' for key in toolCall["调用工具需要的参数"])
    print(f"argsStr ---> {argsStr}")
    content+="\ntoolRes="+str(toolCall["需要调用的工具名称"]+"("+argsStr+")")
    print(f"content ---> {content}")

def get_answer(query):
    tool_call_result = check_tools(query)
    if not tool_call_result or tool_call_result.strip() == "":
        print("Failed to get valid tool call result")
        return "抱歉，暂时无法处理您的请求，请稍后再试。"

    try:
        toolCall = json.loads(tool_call_result)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return "抱歉，暂时无法处理您的请求，请稍后再试。"

    print("checkTools result: *************************************")
    print(f"toolCall ---> {toolCall}")

    if toolCall.get("是否需要调用【工具集】中的工具") == "是":
        print("call_tools start *************************************")
        toolRes = call_tools(toolCall)
        print("call_tools end *************************************")
        prompt = "你是一位可靠的私人助理，用户的问题是：" + query + "。查询工具得到的结果为：" + str(
            toolRes) + "。请根据工具结果，合理的回答用户问题。"
        # finalResult = call_llm_model(prompt)
        finalResult = call_ollama_model(prompt)
    else:
        prompt = "你是一位可靠的私人助理，用户的问题是：" + query + "。请合理地回答用户问题。"
        # finalResult = call_llm_model(prompt)
        finalResult = call_ollama_model(prompt)
        print("call_llm_model end *************************************")

    return finalResult

if __name__ == '__main__':
    query = '我明天到青海去旅游，帮我规划一下行程，要求尽可能的快捷舒适。'
    result = get_answer(query)
    print(result)