import sys
import time
from utils import util
import requests
from obj.money import MoneyLog
from sql.MysqlCon import Mysql

data = {
    "a": "StockDPRealData",
    "Token": "29db4b581d67ec1c46a231e09e919671",
    "c": "StockYiDongKanPan",
    "UserID": 19,
    "Time": "1030"
}

'''
{
    "Turnover": 1056309043,总成交
    "Turnover_rate": "26.35%",
    "Buy_rate": "10.11%",
    "Sell_rate": "-12.71%",
    "ZLBuy": 106755592,主买
    "ZLSell": -134225421,主卖
    "ZLJE": -27469829,净额
    "ttag": 0.001634,
    "errcode": "0"
}
'''
URL = "https://hq.kaipanla.com/w1/api/index.php"

codes = {
    "000980": "众泰汽车"
}
conn = Mysql()
while True:
    print("--------------------------------------------------------------------------------------------")
    min = util.getmin()
    if 1130 < int(min) < 1300:
        time.sleep(300)
        continue
    if int(min) > 1500 or int(min) < 930:
        break

    for code, name in codes.items():
        data["StockID"] = code
        respone = requests.post(URL, data)
        respone.encoding = "unicode_escape"
        result = respone.text
        print(result)
        if not result:
            continue
        ticket = eval(result)
        moneyLog = MoneyLog([code, name, 0, 0, 0, ticket["ZLBuy"], ticket["ZLSell"], ticket["ZLJE"], '', 0, '', ''])

        conn.insertLog(moneyLog.convertToTuple())

    while util.getmin() == min:
        time.sleep(5)
