import requests
import constants
import json

data = {
    "a": "JGStockListox",
    "c": "JGTracking",
    "apiv": "w6",
    "Token": constants.token,
    "Type": 1,
    "OrderType": 0,
    "index": 0,
    "st": 40,
    "isPer": 1,
    "UserID": constants.userId,
}

'''
{
    "Time": 1511663560,
    "StockList": [{
        "StockID": "300110",
        "name": "\u534e\u4ec1\u836f\u4e1a",
        "lpx": "13.7100",
        "rate": "-1.15%"
    }],
    "List": [{
        "StockName": "\u534e\u4ec1\u836f\u4e1a",
        "StockID": "300110",
        "JG": "\u5f20\u660e\u987a",
        "ID": "50159",
        "Day": "2017-09-30",
        "CYSL": 750.01,
        "SJJZC": "\u4e0d\u53d8"
    }],
    "total": 1,
    "errcode": "0",
    "t": 0.009549
}
'''

URL = "https://lhb.kaipanla.com/w1/api/index.php"


def findByGDID(id):
    data["JGID"] = id

    response = requests.post(URL, data)
    response.encoding = "unicode_escape"
    result = response.text
    print(result)
    return json.loads(result)["List"]
