# Created by erainm on 2025/10/28 12:50.
# IDE：PyCharm 
# @Project: agent_project
# @File：memory_demo
# @Description:
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOllama(model="qwen3:4b")

def chatbot(state: State):
    return {"messages":[llm.invoke(state["messages"])]}

def build_graph():
    graphBuilder = StateGraph(State)

    graphBuilder.add_node("chatbot", chatbot)

    graphBuilder.add_edge(START, "chatbot")
    graphBuilder.add_edge("chatbot", END)

    graph = graphBuilder.compile()
    return graph

def build_graph_with_memory():
    graphBuilder = StateGraph(State)
    memory = MemorySaver()

    graphBuilder.add_node("chatbot", chatbot)

    graphBuilder.add_edge(START, "chatbot")
    graphBuilder.add_edge("chatbot", END)

    # 编译图时指定的memory
    graph = graphBuilder.compile(checkpointer=memory)
    return graph

def single_round(graph):
    while True:
        try:
            userInput = input("User: ")
            if userInput.lower() in ["quit", "exit", "q", "bye"]:
                print("Goodbye!")
                break
            state = {"messages": [{"role": "user", "content": userInput}]}
            result = graph.invoke(state)
            print("Assitant: ", result["messages"][-1].content)
        except Exception as e:
            print(f"Error: {e}")

def multi_round(graph, config):
    while True:
        try:
            userInput = input("User: ")
            if userInput.lower() in ["quit", "exit", "q", "bye"]:
                print("Goodbye!")
                break
            state = {"messages": [{"role": "user", "content": userInput}]}
            result = graph.invoke(state, config)
            print("Assitant: ", result["messages"][-1].content)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    # 单轮对话
    # graph = build_graph()
    # single_round(graph)
    # 多轮对话
    graph = build_graph_with_memory()
    config = {"configurable" : {"thread_id": "1"}}
    multi_round(graph, config)
