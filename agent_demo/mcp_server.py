# Created by erainm on 2025/10/28 14:11.
# IDE：PyCharm 
# @Project: agent_project
# @File：mcp_server
# @Description: MCP协议服务端

from mcp.server.fastmcp import FastMCP

mcp = FastMCP('mcp_server')

@mcp.tool()
def get_train_schedule(queryDate, start_station, end_station):
    """根据指定日期、起点城市、终点城市名称，查询列车班次"""
    print(f"getTrainSchedule start *************************************")
    result = [["D81", "12:24", "14:30", "青海站", "890"], ["K1234", "18:24", "07:30", "青海站", "212"]]
    resultStr = "您查询的在" + queryDate + "这一天从" + start_station + "到" + end_station + "的列车班次有：" + str(len(result))+"班：\n"
    for res in result:
        resultStr += res[0] + "次列车：发车时间为：" + res[1] + "到站时间为：" + res[2] + "发车站为：" + res[3] + " 票价为： " + res[4] + "\n"
    return resultStr

if __name__ == '__main__':
    mcp.run(transport='stdio')