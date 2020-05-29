import time
import arrow
import requests
import constants

def todayYMD():
    return time.strftime("%Y-%m-%d", time.localtime())


def todayYMDHMS():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def getmin5():
    min = int(time.strftime("%M", time.localtime())) // 5 * 5
    min = "%02d" % min
    return time.strftime("%H", time.localtime()) + min


def getmin():
    min = time.strftime("%H%M", time.localtime())
    return min


def getmin2(unix):
    min = time.strftime("%H%M", time.localtime(unix))
    return min


def getmin3(times):
    day = arrow.get(times, "YYYY-MM-DD HH:mm:ss")
    return day.shift(days=-1)

def getAccount(data, min):
    index = min // 5
    if index > 10:
        index = index - 10
    account = constants.account[index]
    data["UserID"] = account["userId"]
    data["Token"] = account["token"]
    return data

