import sys
import time
import json
from obj.money import MoneyLog
from sql.MysqlCon import Mysql
import requests
import constants

data = {
    "a": "GetStockChouMa_New",
    "Token": constants.token,
    "c": "StockL2History",
    "UserID": constants.userId,
    "Type": 1,
    "apiv": "w5",
}
url = "https://his.kaipanla.com/w1/api/index.php"

'''
{
    "List": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, "09:25"],
        [2230055, -690420, -608314, -931321, 0, 0, 3185449, 1539635, 0, "09:30"]
    ]
}
0 50w
1 30-50w
2 10-30w
3 10w
4 对倒
5 异动次数
6 成交
7 主买
8 主卖
9 时间
'''
codes = {
    "600581": "八一钢铁"
}
day = "20171124"
conn = Mysql()
for code, name in codes.items():
    data["StockID"] = code
    respone = requests.post(url, data)
    respone.encoding = "unicode_escape"
    result = respone.text
    print(result)
    for ever5 in json.loads(result)["List"]:
        ticket = MoneyLog(
            [code, name, 0, 0, 0, ever5[7], ever5[8], ever5[7] + ever5[8], '', 0, '', ''])

        # conn.insertLog(ticket.convertToTuple())
