# Created by erainm on 2025/11/9 13:34.
# IDE：PyCharm 
# @Project: agent_project
# @File：make_coffee_loop
# @Description:

from langgraph.graph import START,StateGraph,  END
from typing_extensions import TypedDict

#添加状态类
class State(TypedDict):
    water_temperature: int
    product:str

#烧水函数
def boil_water(state):
    print("*"*80)
    print("烧水之前:"+str(state))
    state["product"] = "没烧开的水"
    state["water_temperature"] = state["water_temperature"]+10
    if state["water_temperature"]>100:
        state["water_temperature"] = 100
        state["product"] = "开水"
    print("烧水之后:" + str(state))
    return state

#按照温度处理水的条件函数
def according_water_temperature(state):
    if state["water_temperature"]== 100:
        return "水烧开了"
    else:
        return "水没开"

#构建图
def buildGraph():
    #初始化图
    graphBuilder = StateGraph(State)
    #添加节点
    graphBuilder.add_node("boil_water", boil_water)
    #添加边
    graphBuilder.add_edge(START, "boil_water")
    graphBuilder.add_conditional_edges("boil_water",according_water_temperature,{"水烧开了":END,"水没开":"boil_water"})
    #编译图
    graph = graphBuilder.compile()
    return graph

if __name__ == "__main__":
    graph = buildGraph()
    #打印图
    from agent_demo.make_coffee_demo import show_graph
    show_graph.showGraphInCode(graph, "./pic/make_coffee_loop.jpg")
    #调用图
    state:State = {"water_temperature": 28,"product":"没烧开的水"}
    result = graph.invoke(state)
    print(result)