# Created by erainm on 2025/11/9 13:25.
# IDE：PyCharm 
# @Project: agent_project
# @File：make_coffee_branch
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
    state["water_temperature"] = state["water_temperature"]+10
    if state["water_temperature"]>100:
        state["water_temperature"] = 100
        state["product"] = "烧开的水"
    print("烧水之后:" + str(state))
    return state

#按照温度处理水的条件函数
def according_water_temperature(state):
    print("before processWater:"+str(state))
    if state["water_temperature"]== 100:
        return "水烧开了"
    else:
        return "水没开"

#冲咖啡函数
def make_coffee(state):
    print("冲咖啡之前:" + str(state))
    state["product"] = "咖啡"
    print("冲咖啡之后:"+str(state))
    return state

#需要继续加热函数
def continue_heating(state):
    state["product"] = "没烧开的水"
    print("继续加热"+str(state))
    return state


#构建图
def buildGraph():
    #初始化图
    graphBuilder = StateGraph(State)
    #添加节点
    graphBuilder.add_node("boil_water", boil_water)
    graphBuilder.add_node("make_coffee", make_coffee)
    graphBuilder.add_node("continue_heating", continue_heating)
    #添加边
    graphBuilder.add_edge(START, "boil_water")
    graphBuilder.add_conditional_edges("boil_water",according_water_temperature,{"水烧开了":"make_coffee","水没开":"continue_heating"})
    graphBuilder.add_edge("make_coffee",END)
    graphBuilder.add_edge("continue_heating", END)
    #编译图
    graph = graphBuilder.compile()
    return graph

if __name__ == "__main__":
    graph = buildGraph()

    #打印图
    from agent_demo.make_coffee_demo import show_graph
    show_graph.showGraphInCode(graph, "./pic/make_coffee_branch.jpg")

    #调用图
    state:State = {"water_temperature": 28,"product":"没烧开的水"}
    result = graph.invoke(state)
    print(result)