import requests, time

print(str( "%.0f" % (910193659/10000)))

print (time.strftime("%Y-%m-%d", time.localtime()))
print (time.strftime("%M", time.localtime()))


URL = "http://phbapi.yidiancangwei.com/w1/api/index.php"
today = time.strftime("%Y-%m-%d", time.localtime())
data = {
    "c": "StockRanking",
    "a": "RealRankingInfo",
    "Date": "2017-08-25",
    "RStart": "0925",
    "REnd": "1445",
    "Ratio": "1000",
    "Type": 1,
    "Order": 1,
    "index": 0,
    "st": 20,
}

moneyMap = {}
BUYFLAG = 10000000
hour = 9

# time.sleep(10)
respone = requests.post(URL, data)
respone.encoding = "unicode_escape"
result = respone.text
print(result)
#['601878', '浙商证券', 10.01 涨幅, 6670001664 流通市值, '新股与次新股', 910193659 买入, -218535663 卖出, 691657996 净额 , 8.46 涨速, '游资' ]
for ticket in eval(result)["list"]:
    increaseMoney = 0
    if ticket[0] in moneyMap:
        increaseMoney = ticket[7] - moneyMap[ticket[0]]
    else:
        increaseMoney = ticket[7]
    if increaseMoney > BUYFLAG:
        print("%s 符合条件，单位时间新增买入 %.0f万" % (ticket, increaseMoney/10000))
    moneyMap[ticket[0]] = ticket[7]

''' 1,实时龙虎榜是否实时，即1400和1404的数据是否一样
    如果一样，sleep时间改为300
    2，当天结束时间直接写1500是否有数据返回
    如果没有，data[REnd]= (int(time.strftime("%M", time.localtime()))%5*5)

'''