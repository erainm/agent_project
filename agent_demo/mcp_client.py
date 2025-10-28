# Created by erainm on 2025/10/28 14:15.
# IDE：PyCharm 
# @Project: agent_project
# @File：mcp_client
# @Description: MCP的客户端

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
   server_params = StdioServerParameters(
       command=sys.executable or "/usr/bin/python3",
       args=["mcp_server.py"],
       env=None,
   )

    #  使用stdio_client创建一个MCP客户端
   async with stdio_client(server_params) as (stdio, write):
       # 创建一个会话
       async with ClientSession(stdio, write) as session:
           # 初始化会话
           await session.initialize()

           # 列出可用工具
           tools_response = await session.list_tools()
           print("可用工具：", [tool.name for tool in tools_response.tools])

           available_tools = [{
               "type":"function",
               "function":{
                   "name":tool.name,
                   "description":tool.description,
                   "input_schema":tool.inputSchema
               },
           } for tool in tools_response.tools]
           print("available_tools ---> ", available_tools)

           # 调用getTrainSchedule工具
           result = await session.call_tool("getTrainSchedule", {"query_date": "10月29日", "start_station": "武汉", "end_station": "青海"})
           print("getTrainSchedule工具结果：", result)
if __name__ == '__main__':
    # 运行主函数
    asyncio.run(main())