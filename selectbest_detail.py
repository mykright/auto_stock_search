import os
import time

import arrow
import matplotlib.pyplot as plt
from matplotlib.dates import AutoDateLocator, DateFormatter
from matplotlib.ticker import MultipleLocator

from utils import util
from sql.MysqlCon import Mysql
import constants

today = util.todayYMD()
conn = Mysql()

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

xmajorLocator = MultipleLocator(30)  # 将x主刻度标签设置为20的倍数
xminorLocator = MultipleLocator(5)  # 将x轴次刻度标签设置为5的倍数
autodates = AutoDateLocator()
yearsFmt = DateFormatter('%Y-%m-%d %H:%M')

# today = '2018-02-02'
# 最近的记录

exName = conn.getAll('''
    select name from exclude_name
''')[0][0]

printCodes = []
nextday = arrow.get(today, "YYYY-MM-DD").shift(days=1).format("YYYY-MM-DD")
sql = ('''
    select code from money_log_copy where add_time > '%s' and add_time < '%s'
      and name not in (%s) and name != ''
      GROUP BY code
''' % (today, nextday, exName,))
codes = conn.getAll(sql)

if not codes:
    today = nextday
    exit()
# rootpath = "/Users/xxxx1/Documents/" + today
rootpath = "G:\日记\money\\"+today
if not os.path.exists(rootpath):
    os.mkdir(rootpath)
for code in codes:
    records = conn.getAll('''
    select name,id,rate,SUBSTR(add_time,12),buy,net,sell,increase,code,add_time from  money_log_copy where code = %s 
     and add_time > %s and add_time < %s
       ORDER BY code,id
''', (code[0], today, nextday,))
    if len(records) == 1:
        continue
    # print(records)
    recentRecord = None
    nets = []
    increases = []
    rates = []
    times = []
    for record in records:
        nets.append(record[5] / 10000)
        rates.append(record[2])
        increases.append(record[7] / 10000)
        times.append(time.strftime("%H%M", record[9].timetuple()))

    plt.plot(nets)
    # plt.plot(increases)
    plt2 = plt.twinx()
    plt2.plot(rates, color='r')
    plt.title(records[-1][2])
    # ax = plt.subplot()
    # ax.autoscale_view()
    # ax.xaxis.set_major_formatter(yearsFmt)
    # xxx = pd.date_range(times[0],times[-1],freq='30min')
    # xx = xticks()
    # ax.set_xticks(xxx)
    # plt.xticks(rotation=90)
    # ax.xaxis.set_minor_locator(xminorLocator)
    # increases)
    # plt.show()
    plt.savefig(rootpath + "/" + records[0][0])
    plt.close()
    # break
today = nextday
