import time

import requests

from utils import util
from obj.money import MoneyLog
from sql.MysqlCon import Mysql
import constants

URL = "https://hq.kaipanla.com/w1/api/index.php?apiv=w7"
today = util.todayYMD()

data = {
    "c": "StockFengKData",
    "a": "GetFengKList",
    "Day": '',
    # "Day": "2017-08-25",
    "Time": '',
    # 0，1 股价 3 涨幅 7 主买
    "Order": 11,
    "index": 0,
    "st": 500,
    "UserID": constants.account[1]["userId"],
    "Token": constants.account[1]["token"]
}

moneyMap = {}
INCREASE_FLAG = 7000000
SUM_FLAG = 100000000
times = 0
conn = Mysql()
xx = 1507698000
while True:
    print("--------------------------------------------------------------------------------------------")
    min = util.getmin()
    # xx += 60
    # min = util.getmin2(xx)
    if 1130 < int(min) < 1300:
        time.sleep(300)
        continue
    if int(min) > 1500 or int(min) < 930:
        break
    print(min)
    index = constants.account[1]
    data["UserID"] = index["userId"]
    data["Token"] = index["token"]
    # data["Time"] = min
    print(data)
    respone = requests.post(URL, data)
    respone.encoding = "unicode_escape"
    result = respone.text
    print(result)
    if not result:
        continue
    # ["601619","嘉泽新能","11.3900 股价","10.05 涨幅","2206383360 市值","228541603 买入","-138661623 卖出","89879980 净额","次新股",0,"游资","1503624707 时间"]
    # with open("log/" + today + "fengkou.log", "a", encoding="utf-8") as f:
    #     f.write("--------------------------------------------------------------------------------------------\n")
    #     f.write("时间：" + data["Day"] + " " + str(data["Time"]) + "\n")
    for ticket in eval(result)["List"]:
        moneyLog = MoneyLog(ticket, 1)
        increaseMoney = 0
        nowMoney = int(ticket[7])
        if ticket[0] in moneyMap:
            increaseMoney = nowMoney - moneyMap[ticket[0]]
        else:
            increaseMoney = nowMoney
        hasRecord = False

        moneyLog.increase = increaseMoney
        try:
            conn.insertLog(moneyLog.convertToTuple())
        except Exception as e:
            conn = Mysql()
            print("%s 插入失败" % ticket[0])
            continue
        moneyMap[ticket[0]] = nowMoney
    while util.getmin() == min:
        time.sleep(5)
    times += 1
