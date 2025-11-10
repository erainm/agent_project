# Created by erainm on 2025/11/10 11:10.
# IDE：PyCharm 
# @Project: agent_project
# @File：car_designer_demo01
# @Description:

from langchain_ollama import ChatOllama
from car_designer_demo.gather_information import getInfomation

llm = ChatOllama(model="qwen3:4b")

state = {}
state = getInfomation(state)
prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【竞品分析】和【女性汽车市场发展趋势】，结合你自己的思考，完成一份新车型设计方案。该方案输出的形式要遵循【章节安排】。

         【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"] + """

        【竞品分析】

        """ + state["competitorStatus"] + """

        【章节安排】
        第一章 新车型的设计背景和理念
        第二章 市场趋势分析
        第三章 用户人群分析与使用场景
        第四章 技术方案和细分市场定制
        第五章 竞品分析与差异化竞争优势
        第六章 产品卖点
        第七章 定价策略
        第八章 海外市场
        第九章 销量预估"""

result = llm.invoke(prompt)

print(result.content)

"""
存在问题：
1. 没有新车型车名
2. 每章节篇幅太短
"""