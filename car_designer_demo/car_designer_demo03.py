# Created by erainm on 2025/11/10 11:18.
# IDE：PyCharm 
# @Project: agent_project
# @File：car_designer_demo03
# @Description:

from langchain_ollama import ChatOllama
from car_designer_demo.gather_information import getInfomation

llm = ChatOllama(model="qwen3:4b", num_predict=10000)

state = {}
state = getInfomation(state)
prompt = """你是凯瑞汽车旗下维多利亚品牌的车型设计师，维多利亚品牌主要面向年轻的女性客户，根据【竞品分析】和【女性汽车市场发展趋势】，结合你自己的思考，完成一份新车型设计方案。该方案输出的形式要遵循【章节安排】，全文在10000字左右。

         【女性汽车市场发展趋势】
        """ + state["femaleMarketTrend"] + """

        【竞品分析】

        """ + state["competitorStatus"] + """

        【章节安排】
        第一章 新车型的设计背景和理念 #这一章节里必须给新车型起一个符合女性汽车市场的名字
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
注：尝试增加设计方案的篇幅，直接在提示词后面添加字数要求（10000字），但是第一次生成并不成功，生成的长度远小于要求的字数。
在ChatOllama里添加参数num_predict=10000后，再次试验，发现生成的文档基本达到了要求的字数。

问题：
篇幅确实增加了，但是我们需要的九章内容仍然不够详细，后面产生了很多不需要的章节。
看来小参数量模型不太适合生成较长的文本。
"""