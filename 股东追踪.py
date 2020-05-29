import sys
import time
from utils import util
import requests
from obj.money import MoneyLog
from sql.MysqlCon import Mysql
import constants
from graphviz import Digraph
import json

data = {
    "a": "NewJGResult",
    "Token": constants.token,
    "c": "JGTracking",
    "Day": "2017-09-30",
    "Type": 1,
    "OrderType": 1,
    "index": 0,
    "st": 40,
    "isPer": 1,
    "UserID": constants.userId,
}

'''
{
    "Time": 1511603572,
    "StockList": [{
        "StockID": "300110",
        "name": "\u534e\u4ec1\u836f\u4e1a",
        "lpx": "13.7100",
        "rate": "-1.15%"
    }, {
        "StockID": "600684",
        "name": "\u73e0\u6c5f\u5b9e\u4e1a",
        "lpx": "5.9500",
        "rate": "0.17%"
    }, {
        "StockID": "002650",
        "name": "\u52a0\u52a0\u98df\u54c1",
        "lpx": "6.3900",
        "rate": "-0.16%"
    }, {
        "StockID": "300471",
        "name": "\u539a\u666e\u80a1\u4efd",
        "lpx": "14.0800",
        "rate": "0.00%"
    }],
    "List": [{
        "JG": "\u9ec4\u950b\u745c",
        "ID": "66660",
        "Day": "2017-09-30",
        "CYSL": 775.13,
        "SJJZC": "-49.71",
        "GuDongID": "800154",
        "StockID": "300110"
    }],
    "total": 4,
    "errcode": "0",
    "t": 0.012957
}
'''
URL = "https://lhb.kaipanla.com/w1/api/index.php?apiv=w6"
data["StockID"] = "300110"
dot = Digraph(comment=data["StockID"])

response = requests.post(URL, data)
response.encoding = "unicode_escape"
result = response.text
# print(result)
stocks = {}
for stock in json.loads(result)["StockList"]:
    stocks[stock["StockID"]] = stock["name"]
    dot.node(stock["StockID"], stock["name"], shape='box')

stockAndPersonMap = {}

for person in json.loads(result)["List"]:
    if person["JG"] == '张明顺':
        print(person)
    if person["StockID"] + person["ID"] not in stockAndPersonMap:
        num = 0
        dot.node(person["ID"], person["JG"])
        dot.edge(person["StockID"], person["ID"], constraint='false')
        stockAndPersonMap[person["StockID"] + person["ID"]] = 1

print(dot.source)
dot.render('test-output/round-table.gv', view=True)
