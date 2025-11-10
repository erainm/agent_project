# Created by erainm on 2025/11/10 11:29.
# IDE：PyCharm 
# @Project: agent_project
# @File：car_designer_v2_demo02
# @Description:大参数量模型+分章节输出，在之前方案上做了加大幅度的改动，每个章节单独输出，可以非常准确地控制每章的篇幅和细节。最后把结果拼装在一起。注意：这里每章的生成内容互不干扰，可以并行

from langchain_core.runnables import Runnable
from typing import Dict, Optional
from langgraph.graph import StateGraph, START
from typing_extensions import TypedDict
from typing import Annotated
import operator
from car_designer_demo.gather_information import getInfomation


def updateReceiveDate(left, right):
    if len(left) > 0:
        return left
    else:
        return right


class State(TypedDict):
    femaleMarketTrend: Annotated[str, updateReceiveDate]
    victoriaStatus: Annotated[str, updateReceiveDate]
    competitorStatus: Annotated[str, updateReceiveDate]

    # 背景，目标，理念
    chapter1: Annotated[str, operator.add]
    # 市场趋势分析
    chapter2: Annotated[str, operator.add]
    # 用户人群分析与使用场景
    chapter3: Annotated[str, operator.add]
    # 技术方案+细分市场定制
    chapter4: Annotated[str, operator.add]
    # 竞品分析与差异化竞争
    chapter5: Annotated[str, operator.add]
    # 产品卖点
    chapter6: Annotated[str, operator.add]
    # 定价策略
    chapter7: Annotated[str, operator.add]
    # 海外市场
    chapter8: Annotated[str, operator.add]
    # 销量预估
    chapter9: Annotated[str, operator.add]

    design: Annotated[str, updateReceiveDate]


class CustomModel(Runnable):
    def __init__(self, model_endpoint: str, api_key: str):
        self.endpoint = model_endpoint
        self.api_key = api_key

    def invoke(self, prompt: str, modelName: str = "deepseek-ai/DeepSeek-V3", maxTokens: int = 3000, tempreture=0.6,
               config: Optional[Dict] = None) -> Dict:
        """调用自定义模型API"""
        import requests

        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        payload = {
            "model": modelName,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": tempreture,
            "max_tokens": maxTokens
        }

        response = requests.post(self.endpoint, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']


llm = CustomModel(
    model_endpoint="https://api.siliconflow.cn/v1/chat/completions",
    api_key=""
)


def generateChapter1(state):
    # 背景，理念
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【女性汽车市场发展趋势】，结合你自己的思考，完成新车型设计方案的第一章“一、设计背景和理念”，说明新车型的设计背景和理念。各级标题使用markdown格式。600字以内。

        【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"]
    result = llm.invoke(prompt)
    # print("背景和设计理念："+result)
    state["chapter1"] = result
    return state


def generateChapter2(state):
    # 市场趋势分析
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【女性汽车市场发展趋势】、【竞品资料】，结合你自己的思考，完成新车型设计方案的第二章“二、市场趋势分析”，说明当前女性汽车市场的趋势。各级标题使用markdown格式。800字以内。

        【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"] + """

        【竞品资料】
        """ + state["competitorStatus"]
    result = llm.invoke(prompt)
    # print("市场趋势分析：" + result)
    state["chapter2"] = result
    return state


def generateChapter3(state):
    # 用户人群分析和使用场景
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【女性汽车市场发展趋势】，结合你自己的思考，完成新车型设计方案的第三章“三、目标客户与场景”，分析用户人群特点和产品的适用场景。各级标题使用markdown格式。800字以内。

        【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"]
    result = llm.invoke(prompt)
    # print("用户人群分析和使用场景：" + result)
    state["chapter3"] = result
    return state


def generateChapter4(state):
    # 技术方案
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【女性汽车市场发展趋势】，结合你自己的思考，完成新车型设计方案的第四章“四、技术方案”，具体说明新车型的技术方案，尤其是针对细分市场的定制特性。各级标题使用markdown格式。1500字以内。

        【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"]
    result = llm.invoke(prompt)
    # print("技术方案：" + result)
    state["chapter4"] = result
    return state


def generateChapter5(state):
    # 竞品分析与差异化竞争
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【竞品资料】，结合你自己的思考，完成新车型设计方案的第五章“五、竞品分析”，分析竞品的特性和销售情况，并分析新车型的差异化竞争优势。各级标题使用markdown格式。1500字以内。

        【竞品资料】
        """ + state["competitorStatus"]
    result = llm.invoke(prompt)
    # print("竞品分析：" + result)
    state["chapter5"] = result
    return state


def generateChapter6(state):
    # 产品卖点
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【女性汽车市场发展趋势】、【竞品资料】，结合你自己的思考，完成新车型设计方案的第六章“六、产品卖点”，详细说明在当前市场趋势下，与竞品相比，新车型的卖点。各级标题使用markdown格式。800字以内。

         【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"] + """

        【竞品资料】
        """ + state["competitorStatus"]
    result = llm.invoke(prompt)
    # print("产品卖点：" + result)
    state["chapter6"] = result
    return state


def generateChapter7(state):
    # 定价策略
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【竞品资料】，结合你自己的思考，完成新车型设计方案的第七章“七、定价策略”，制定一个详细的新车型定价策略。各级标题使用markdown格式。800字以内。

        【竞品资料】
        """ + state["competitorStatus"]
    result = llm.invoke(prompt)
    # print("定价策略：" + result)
    state["chapter7"] = result
    return state


def generateChapter8(state):
    # 海外市场
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【女性汽车市场发展趋势】，结合你自己的思考，完成新车型设计方案的第八章“八、海外市场”，详细分析新车型在海外市场需要做哪些调整，可能的表现。各级标题使用markdown格式。800字以内。

         【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"]
    result = llm.invoke(prompt)
    # print("海外市场：" + result)
    state["chapter8"] = result
    return state


def generateChapter9(state):
    # 销量预估
    prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【女性汽车市场发展趋势】、【竞品资料】，结合你自己的思考，完成新车型设计方案的第九章“九、销量预估”，预估新车型的销量。各级标题使用markdown格式。200字以内。

         【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"] + """

        【竞品资料】
        """ + state["competitorStatus"]
    result = llm.invoke(prompt)
    # print("定价策略：" + result)
    state["chapter9"] = result
    return state


def merge(state):
    state["design"] = state["chapter1"] + "\n" + \
                      state["chapter2"] + "\n" + \
                      state["chapter3"] + "\n" + \
                      state["chapter4"] + "\n" + \
                      state["chapter5"] + "\n" + \
                      state["chapter6"] + "\n" + \
                      state["chapter7"] + "\n" + \
                      state["chapter8"] + "\n" + \
                      state["chapter9"]
    return state


def buildGraph():
    graphBuilder = StateGraph(State)

    graphBuilder.add_node("getInfomation", getInfomation)
    graphBuilder.add_node("generateChapter1", generateChapter1)
    graphBuilder.add_node("generateChapter2", generateChapter2)
    graphBuilder.add_node("generateChapter3", generateChapter3)
    graphBuilder.add_node("generateChapter4", generateChapter4)
    graphBuilder.add_node("generateChapter5", generateChapter5)
    graphBuilder.add_node("generateChapter6", generateChapter6)
    graphBuilder.add_node("generateChapter7", generateChapter7)
    graphBuilder.add_node("generateChapter8", generateChapter8)
    graphBuilder.add_node("generateChapter9", generateChapter9)
    graphBuilder.add_node("merge", merge)

    graphBuilder.add_edge(START, "getInfomation")
    graphBuilder.add_edge("getInfomation", "generateChapter1")
    graphBuilder.add_edge("getInfomation", "generateChapter2")
    graphBuilder.add_edge("getInfomation", "generateChapter3")
    graphBuilder.add_edge("getInfomation", "generateChapter4")
    graphBuilder.add_edge("getInfomation", "generateChapter5")
    graphBuilder.add_edge("getInfomation", "generateChapter6")
    graphBuilder.add_edge("getInfomation", "generateChapter7")
    graphBuilder.add_edge("getInfomation", "generateChapter8")
    graphBuilder.add_edge("getInfomation", "generateChapter9")

    graphBuilder.add_edge(
        ["generateChapter1", "generateChapter2", "generateChapter3", "generateChapter4", "generateChapter5",
         "generateChapter6", "generateChapter7", "generateChapter8", "generateChapter9"], "merge")

    graph = graphBuilder.compile()
    return graph


if __name__ == "__main__":
    graph = buildGraph()

    from agent_demo.make_coffee_demo import show_graph

    show_graph.showGraphInCode(graph, "./pic/car_designer_v2_demo02.jpg")

    state: State = {}
    result = graph.invoke(state)
    print("新车型设计书  " + "*" * 80)
    print(result["design"])


"""
问题：
这一版的细节控制能力明显增强，但是各部分间的内容有冲突：
    1. 微型电动车定位（4.2米车身）与高性能版（零百5.8s）存在矛盾，前者强调经济实用，后者需要更大电池/电机配置，可能导致成本超出5万元价格带。
    2. 隐藏式毫米波雷达与超声波雷达误识别问题：方案未说明如何解决毫米波雷达对金属饰品（如项链）的干扰问题，可能引发新的误判风险。
    3. 可变形后排座椅（亲子模式）与应急尿布台存在空间冲突，展开尿布台需占用后排空间，此时无法同时使用旋转座椅功能。
    4. 莫兰迪色系强调低调，但"局部亮色模块"设计可能破坏整体哑光质感，与"反刻板印象"理念产生视觉冲突。
    5. 生理周期监测需持续收集健康数据，与"女性数据安全"条款中"避免功能外显"原则存在潜在伦理冲突。
"""