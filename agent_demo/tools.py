# Created by erainm on 2025/10/28 11:01.
# IDE：PyCharm 
# @Project: agent_project
# @File：tools
# @Description: 查询可购买的火车票（模拟，实际从网站中查询）


def getTrainSchedule(queryDate, start_station, end_station):
    """根据指定日期、起点城市、终点城市名称，查询列车班次"""
    print(f"getTrainSchedule start *************************************")
    result = [["D81", "12:24", "14:30", "青海站", "890"], ["K1234", "18:24", "07:30", "青海站", "212"]]
    resultStr = "您查询的在" + queryDate + "这一天从" + start_station + "到" + end_station + "的列车班次有：" + str(len(result))+"班：\n"
    for res in result:
        resultStr += res[0] + "次列车：发车时间为：" + res[1] + "到站时间为：" + res[2] + "发车站为：" + res[3] + " 票价为： " + res[4] + "\n"
    return resultStr