import time

import requests

import utils
from obj.money import MoneyLog
from sql.MysqlCon import Mysql

URL = "http://phbapi.yidiancangwei.com/w1/api/index.php"
today = utils.todayYMD()

data = {
    "c": "StockFengKData",
    "a": "GetFengKList",
    "Day": '',
    # "Day": "2017-08-25",
    "Time": '0929',
    # 0，1 股价 3 涨幅 7 主买
    "Order": 11,
    "index": 0,
    "st": 500,
}

moneyMap = {}
INCREASE_FLAG = 7000000
SUM_FLAG = 100000000
times = 0
conn = Mysql()
xx = 1507689360
while True:
    print("--------------------------------------------------------------------------------------------")
    xx += 60
    min = utils.getmin2(xx)
    if 1130 < int(min) < 1300:
        time.sleep(300)
        continue
    if int(min) > 1500 or int(min) < 930:
        break
    data["Time"] = min
    print(data)
    respone = requests.post(URL, data)
    respone.encoding = "unicode_escape"
    result = respone.text
    print(result)
    # ["601619","嘉泽新能","11.3900 股价","10.05 涨幅","2206383360 市值","228541603 买入","-138661623 卖出","89879980 净额","次新股",0,"游资","1503624707 时间"]
    with open("log/" + today + "fengkouxx.log", "a", encoding="utf-8") as f:
        f.write("--------------------------------------------------------------------------------------------\n")
        f.write("时间：" + data["Day"] + " " + str(data["Time"]) + "\n")
        for ticket in eval(result)["List"]:
            moneyLog = MoneyLog(ticket)
            increaseMoney = 0
            nowMoney = int(ticket[7])
            if ticket[0] in moneyMap:
                increaseMoney = nowMoney - moneyMap[ticket[0]]
            else:
                increaseMoney = nowMoney
            hasRecord = False

            moneyLog.increase = increaseMoney
            if increaseMoney > INCREASE_FLAG and times != 0:
                conn.insertLog(moneyLog.convertToTuple())
                hasRecord = True
                f.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
                log = "%s %s 涨幅%s,市值%.0f亿 \n" \
                      "板块：%s\n" \
                      "主买：%.0f万\n" \
                      "主卖：%.0f万\n" \
                      "净买入：%.0f万\n" \
                      "类型：%s\n" \
                      "符合条件1，单位时间新增买入 %.0f万\n" % (
                          ticket[0], ticket[1], ticket[3], int(ticket[4]) / 100000000, ticket[8],
                          int(ticket[5]) / 10000, int(ticket[6]) / 10000, int(ticket[7]) / 10000, ticket[10]
                          , increaseMoney / 10000)
                f.write(log)
                print(log)
            if int(min) == 1500:
                moneyLog.inType = 3
                conn.insertLog(moneyLog.convertToTuple())
            # if nowMoney > SUM_FLAG and int(min) % 10 == 0:
            #     if not hasRecord:
            #         f.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
            #         log = "%s %s 涨幅%s,市值%.0f亿 \n" \
            #               "板块：%s\n" \
            #               "主买：%.0f万\n" \
            #               "主卖：%.0f万\n" \
            #               "净买入：%.0f万\n" \
            #               "类型：%s\n" % (
            #                   ticket[0], ticket[1], ticket[3], int(ticket[4]) / 100000000, ticket[8],
            #                   int(ticket[5]) / 10000, int(ticket[6]) / 10000, int(ticket[7]) / 10000, ticket[10]
            #               )
            #         f.write(log)
            #     log = "符合条件2，净额突破，共买入 %.0f万\n" % (nowMoney / 10000)
            #     f.write(log)
            #     print(log)
            moneyMap[ticket[0]] = nowMoney
    # time.sleep(60)
    times += 1
