import time

import constants
import json
from obj.money import MoneyLog
from sql.MysqlCon import Mysql
import requests
from utils import util

data = {
    "a": "StockChouMaByTimeNew_W5",
    "c": "StockYiDongKanPan",
}
url = "https://hq.kaipanla.com/w1/api/index.php"

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
codes = constants.codes

today = util.todayYMD()
conn = Mysql()

exName = conn.getAll('''
    select name from exclude_name
''' )[0][0]

watchlist = conn.getAll('''
    select code,name from watch_list where flag = 1
''' )

times = 0
for tock in watchlist:
    code = tock[0]
    name = tock[1]
    print(code,name)
    conn._exeCuteCommit("delete from money_log_copy where add_time > '%s' and code = %s and in_type = 2" % (today, code))
    print("请求数据")
    data["StockID"] = code
    index = constants.account[1]
    data["UserID"] = index["userId"]
    data["Token"] = index["token"]
    respone = requests.post(url, data)
    respone.encoding = "unicode_escape"
    result = respone.text
    print(result)
    if exName.find(name) > 0:
        print("今日不看")
        continue
    codes = conn.getAll('''
    select code from money_log_copy where add_time > %s
      and code = %s and in_type = 1
''', param=[today, code])
    if codes:
        print("风口已有")
        continue
    for ever5 in json.loads(result)["List"]:
        ticket = MoneyLog(
            [code, name, 0, 0, 0, ever5[7], ever5[8], ever5[7] + ever5[8], '', 0, '', ''], 2)
        conn.insertLog(ticket.convertToTuple())
    time.sleep(3)
    times += 1
