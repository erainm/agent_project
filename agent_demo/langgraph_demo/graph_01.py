# Created by erainm on 2025/10/29 14:41.
# IDE：PyCharm 
# @Project: agent_project
# @File：graph_01
# @Description:

from langgraph.graph import START, StateGraph, END

graphBuilder = StateGraph(dict)

graphBuilder.add_edge(START, END)
graph = graphBuilder.compile()

# 用matplotlib输出graph
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

try:
    # 使用 Mermaid 生成图表并保存为文件
    mermaid_code = graph.get_graph().draw_mermaid_png()
    with open("graph_01.jpg", "wb") as f:
        f.write(mermaid_code)

    # 使用 matplotlib 显示图像
    img = mpimg.imread("graph_01.jpg")
    plt.imshow(img)
    plt.axis("off")
    plt.show()
except Exception as e:
    print(f"An error occurred: {e}")