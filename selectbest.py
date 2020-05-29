import utils
from sql.MysqlCon import Mysql

today = utils.todayYMD()
conn = Mysql()

codes = conn.getAll('''
    select code from money_log where add_time > %s GROUP BY code
''', param=[today])

codeIdMap = {}
increaseMap = {}

printCodes = []

'''
'鹏欣资源' 0
22 1
8.7 涨幅 2
datetime.datetime(2017, 8, 31, 9, 35, 30) 时间 3
132140377 主买 4
29270185 净额 5
-102870192 主卖 6
11100000 增长 7
'''


def isBest(recentRecord, record):
    # 涨幅超过7
    if record[2] > 7:
        return False
    if (record[4] - recentRecord[4]) / recentRecord[4] > 0.67 and (record[5] - recentRecord[5]) / abs(
            recentRecord[5]) > 0.7:
        return True


# 吸筹次数
INCREASE_MONEY = 7000000


def increaseMore(record):
    if record[2] > 7:
        return False
    time = 0
    if record[0] in increaseMap:
        time = increaseMap[record[0]]
    if time == 3:
        return False
    if record[7] >= INCREASE_MONEY and record[5] / record[4] > 0.4:
        time += 1
    increaseMap[record[0]] = time
    if time == 3:
        return True
    else:
        return False


for code in codes:
    records = conn.getAll('''
    select name,id,rate,SUBSTR(add_time,12),buy,net,sell,increase,code from  money_log where code = %s and add_time > %s
      and code not in (select code from exclude_code) and from_type = 1 and in_type = 1 ORDER BY code,id
''', (code[0], today,))
    if len(records) == 1:
        continue
    # print(records)
    recentRecord = None
    for record in records:

        if increaseMore(record):
            print(record, "连续吸筹")
            printCodes.append(record[8])

        storeId = 0
        if record[0] in codeIdMap:
            storeId = codeIdMap[record[0]]
        if record[1] < storeId:
            continue
        if recentRecord is not None:
            if isBest(recentRecord, record):
                print(record)
                printCodes.append(record[8])
                break
        recentRecord = record

print(set(printCodes))
