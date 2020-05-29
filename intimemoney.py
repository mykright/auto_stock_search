import time

import requests

import utils
from sql.MysqlCon import Mysql

URL = "http://phbapi.yidiancangwei.com/w1/api/index.php"
today = utils.todayYMD()

data = {
    "c": "StockRanking",
    "a": "RealRankingInfo",
    "Date": today,
    "RStart": "0925",
    "REnd": "0930",
    "Ratio": "1000",
    "Type": 1,
    "Order": 1,
    "index": 0,
    "st": 50,
}

moneyMap = {}
INCREASE_FLAG = 10000000
SUM_FLAG = 100000000
times = 0
conn = Mysql()
while True:
    print("--------------------------------------------------------------------------------------------")
    min = int(utils.getmin5())
    if 1135 < int(min) < 1300:
        time.sleep(300)
        continue
    if min > 1501 or min < 930:
        break
    data["REnd"] = utils.getmin5()
    respone = requests.post(URL, data)
    respone.encoding = "unicode_escape"
    result = respone.text
    print(data)
    print(result)
    # ['601878', '浙商证券', 10.01 涨幅, 6670001664 流通市值, '新股与次新股', 910193659 买入, -218535663 卖出, 691657996 净额 , 8.46 涨速, '游资' ]
    with open("log/" + today + "money.log", "a", encoding="utf-8") as f:
        f.write("--------------------------------------------------------------------------------------------\n")
        f.write("时间：" + data["Date"] + " " + str(data["REnd"]) + "\n")
        for ticket in eval(result)["list"]:
            increaseMoney = 0
            nowMoney = int(ticket[7])
            if ticket[0] in moneyMap:
                increaseMoney = nowMoney - moneyMap[ticket[0]]
            else:
                increaseMoney = nowMoney
            hasRecord = False
            if increaseMoney > INCREASE_FLAG and times != 0:
                hasRecord = True
                conn.insertLog(
                    [ticket[1], ticket[5], ticket[7], ticket[3], ticket[9], ticket[0], utils.todayYMDHMS(), ticket[4],
                     utils.todayYMDHMS(), ticket[2], ticket[6], 1, 2, increaseMoney])
                f.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
                log = "%s %s 涨幅%s,市值%.0f亿 \n" \
                      "板块：%s\n" \
                      "主买：%.0f万\n" \
                      "主卖：%.0f万\n" \
                      "净买入：%.0f万\n" \
                      "类型：%s\n" \
                      "符合条件1，单位时间新增买入 %.0f万\n" % (
                          ticket[0], ticket[1], ticket[2], int(ticket[3]) / 100000000, ticket[4],
                          int(ticket[5]) / 10000, int(ticket[6]) / 10000, int(ticket[7]) / 10000, ticket[9],
                          increaseMoney / 10000)
                f.write(log)
                print(log)
            if nowMoney > SUM_FLAG:
                if not hasRecord:
                    conn.insertLog(
                        [ticket[1], ticket[5], ticket[7], ticket[3], ticket[9], ticket[0], utils.todayYMDHMS(), ticket[4],
                         utils.todayYMDHMS(), ticket[2], ticket[6], 2, 2, 0])
                    f.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
                    log = "%s %s 涨幅%s,市值%.0f亿 \n" \
                          "板块：%s\n" \
                          "主买：%.0f万\n" \
                          "主卖：%.0f万\n" \
                          "净买入：%.0f万\n" \
                          "类型：%s\n" % (
                              ticket[0], ticket[1], ticket[2], int(ticket[3]) / 100000000, ticket[4],
                              int(ticket[5]) / 10000, int(ticket[6]) / 10000, int(ticket[7]) / 10000, ticket[9]
                          )
                    f.write(log)
                log = "符合条件2，净额突破，共买入 %.0f万\n" % (nowMoney / 10000)
                f.write(log)
                print(log)
            moneyMap[ticket[0]] = nowMoney
    time.sleep(300)
    times += 1
