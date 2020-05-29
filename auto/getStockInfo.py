import time
import arrow
import numpy as np
import auto.ts_pro as ts_pro

day = arrow.get(time.time())
YMD = 'YYYYMMDD'
todayDate = day.format(YMD)


def getMap(data):
    today = {}
    for index, stock in data.iterrows():
        today[stock['ts_code']] = stock
    return today


# [{最近一天},{倒数第二天}]
def getDaily(dates):
    dailys = []
    for date in dates:
        temp = ts_pro.getOneDayStockInfo(date)
        dailys.append(getMap(temp))
    return dailys


tradeDates = ts_pro.getCloseDay(todayDate)
dailys = getDaily(tradeDates)


def findstock(tempCode, stockarr):
    closeday = stockarr[0][tempCode]
    minPrice=99999
    maxPrice=0
    tempRight = 0.0
    tempRightTime = 0
    tempLeft = 0.0
    tempLeftTime = 0
    lastprice = closeday['close']
    lastmoney = closeday['turnover_rate']
    tempLeftArr = []
    tempRightArr = []
    first = True
    for tempDay in stockarr:
        if tempDay[tempCode]['close'] > maxPrice:
            maxPrice = tempDay[tempCode]['close']
        if tempDay[tempCode]['close'] < minPrice:
            minPrice = tempDay[tempCode]['close']
        if not first:
            if tempDay[tempCode]['close'] <= lastprice:
                tempRightArr.append(lastmoney)
                tempRight = tempRight + lastmoney
                tempRightTime = tempRightTime + 1
            else:
                tempLeftArr.append(lastmoney)
                tempLeft = tempLeft + lastmoney
                tempLeftTime = tempLeftTime + 1
            lastprice = tempDay[tempCode]['close']
            lastmoney = tempDay[tempCode]['turnover_rate']
        first = False

    # print(maxPrice,minPrice,tempLeft,tempLeftTime,tempRight,tempRightTime)
    tempMaxLeft = max(tempLeftArr)
    tempMaxRight = max(tempRightArr)
    tempRightArr.remove(tempMaxRight)

    if (tempRight/tempRightTime)/(tempLeft/tempLeftTime) > 1.3 \
            and tempRightTime > tempLeftTime \
            and closeday['close'] / minPrice < 1.15 \
            and maxPrice/closeday['close'] < 1.15 \
            and (tempRight+tempLeft) * closeday['circ_mv']/len(stockarr) > 500000\
            and tempMaxLeft < tempMaxRight:
            # and tempMaxLeft < max(tempRightArr):
        print(code)


# 寻找
for code, stock in dailys[0].items():
    try:
        findstock(code, dailys)
    except Exception as e:
        continue
