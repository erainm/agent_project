# Created by erainm on 2025/11/9 13:40.
# IDE：PyCharm 
# @Project: agent_project
# @File：make_coffee_parallel
# @Description:

from langgraph.graph import START,StateGraph, END
from typing_extensions import TypedDict
from typing import Annotated

#合并温度值的方式，取其大者
def updateTempreture(left, right):
    return max(left, right)

#合并产物的方式，优先取工序靠后的产物
def updateProduct(left,right):
    if left=="咖啡" or right == "咖啡":
        return "咖啡"
    elif left=="开水" or right == "开水":
        return "开水"
    elif left=="温水" or right == "温水":
        return "温水"
    else:
        return "凉水"

#合并咖啡固体的方式，优先取工序靠后的产物
def updateSolid(left,right):
    if left=="咖啡粉" or right == "咖啡粉":
        return "咖啡粉"
    else:
        return "咖啡豆"

#添加状态类
#如果有并行的节点，必然涉及到并行节点输出数据的合并，使用Annotated，第一个参数是数据类型，第二个参数是合并数据的方式
class State(TypedDict):
    水温: Annotated[int,updateTempreture]
    产物:Annotated[str,updateProduct]
    咖啡固体:Annotated[str,updateSolid]

#磨咖啡豆函数
def 磨咖啡豆(state):
    print("*" * 80)
    print("磨咖啡豆之前:" + str(state))
    state["咖啡固体"] = "咖啡粉"
    print("磨咖啡豆之后:" + str(state))
    return state

#烧温水函数
def 烧温水(state):
    print("*"*80)
    print("烧温水之前:"+str(state))
    state["产物"] = "没烧开的水"
    if state["水温"]<38:
        state["水温"] = 38
        state["产物"] = "温水"
    print("烧温水之后:" + str(state))
    return state

#烧开水函数
def 烧开水(state):
    print("*"*80)
    print("烧开水之前:"+str(state))
    state["产物"] = "没烧开的水"
    if state["水温"]<100:
        state["水温"] = 100
        state["产物"] = "开水"
    print("烧开水之后:" + str(state))
    return state

#冲咖啡函数
def 冲咖啡(state):
    print("冲咖啡之前:" + str(state))
    state["产物"]="咖啡"
    print("冲咖啡之后:" + str(state))
    return state

#构建图
def buildGraph1():
    #初始化图
    graphBuilder = StateGraph(State)
    #添加节点
    graphBuilder.add_node("烧水2", 烧开水)
    graphBuilder.add_node("磨咖啡豆",磨咖啡豆)
    graphBuilder.add_node("冲咖啡", 冲咖啡)
    # 添加边
    graphBuilder.add_edge(START, "磨咖啡豆")
    graphBuilder.add_edge(START, "烧水2")
    graphBuilder.add_edge("磨咖啡豆", "冲咖啡")
    graphBuilder.add_edge("烧水2", "冲咖啡")
    graphBuilder.add_edge("冲咖啡", END)
    #上述流程的执行顺序：
    #第一批计算的节点是 烧水2 和 磨咖啡豆
    #第二批计算的节点是 冲咖啡
    #这种写法貌似得到了正确的结果，其实是一种错觉，实际工作中不要这样写

    #编译图
    graph = graphBuilder.compile()
    return graph

if __name__ == "__main__":
    graph = buildGraph1()
    # 打印图
    from utils import show_graph

    show_graph.showGraphInCode(graph, "/Users/erainm/Documents/application/dev/workSpace/agent_project/agent_demo/make_coffee_demo/pic/make_coffee_parallel.jpg")
    # 调用图
    state:State = {"水温": 28,"产物":"凉水","咖啡固体":"咖啡豆"}
    result = graph.invoke(state)
    print(result)