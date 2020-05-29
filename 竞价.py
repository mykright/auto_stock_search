import requests
import json

data = {
    "a": "GetBidYiDong",
    "Token": "29db4b581d67ec1c46a231e09e919671",
    "c": "StockBidYiDong",
    "UserID": 19,
    "day": "20171026"
}

url = "https://hq.kaipanla.com/w1/api/index.php"

respone = requests.post(url, data)
respone.encoding = "unicode_escape"
result = respone.text
print(result)
result = result.replace("zhangfu", "涨幅").replace("BidAmount", "成交").replace("sjltp", "市值")\
    .replace("BidAmount", "净额").replace("BuyP", "大单占比").replace("Buy100", "买入")\
    .replace("Sell100", "卖出").replace("BidAmount", "净额").replace("Plate", "概念")
for p in json.loads(result)["List"]:
    print("--------------------------------------------------------------------------------")
    print(p)


