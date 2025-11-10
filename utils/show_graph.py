# Created by erainm on 2025/11/9 13:14.
# IDE：PyCharm 
# @Project: agent_project
# @File：show_graph
# @Description:

def showGraphInCode(graph,fileName):
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg  # 导入matplotlib.image用于读取图像
    try:
        # 使用 Mermaid 生成图表并保存为文件
        mermaid_code = graph.get_graph().draw_mermaid_png(
            max_retries=5,
            retry_delay=2.0
        )
        with open(fileName, "wb") as f:
            f.write(mermaid_code)

        # 使用 matplotlib 显示图像
        img = mpimg.imread(fileName)
        plt.imshow(img)
        plt.axis('off')  # 关闭坐标轴
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")

def showGraphInCode2(graph):
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg  # 导入matplotlib.image用于读取图像
    try:
        # 使用 Mermaid 生成图表并保存为文件
        print("before mermid")
        mermaid_code = graph.get_graph().draw_png()
        print("after mermid")
        with open("graph.jpg", "wb") as f:
            f.write(mermaid_code)

        # 使用 matplotlib 显示图像
        img = mpimg.imread("graph.jpg")
        plt.imshow(img)
        plt.axis('off')  # 关闭坐标轴
        plt.show()
    except Exception as e:
        print(f"An error occurred: {e}")