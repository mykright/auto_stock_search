import tushare as ts


ts.set_token("your_token")
pro = ts.pro_api()


##查找最近N天的交易日
def getCloseDay(day, daysnum=15):
    tradeDates = []
    days = pro.query('trade_cal', start_date='20190101', end_date=day)
    index = -1
    while daysnum != 0:
        temp = days.iloc[index]
        index = index - 1
        if temp['cal_date'] > day:
            continue
        if temp['is_open'] == 1:
            tradeDates.append(temp['cal_date'])
            daysnum = daysnum - 1
    return tradeDates


'''
名称    类型    描述
ts_code    str    TS股票代码
trade_date    str    交易日期
close    float    当日收盘价
turnover_rate    float    换手率（%）
turnover_rate_f    float    换手率（自由流通股）
volume_ratio    float    量比
pe    float    市盈率（总市值/净利润）
pe_ttm    float    市盈率（TTM）
pb    float    市净率（总市值/净资产）
ps    float    市销率
ps_ttm    float    市销率（TTM）
total_share    float    总股本 （万）
float_share    float    流通股本 （万）
free_share    float    自由流通股本 （万）
total_mv    float    总市值 （万元）
circ_mv    float    流通市值（万元）
'''


def getOneDayStockInfo(date):
    return pro.daily_basic(ts_code='', trade_date=date)

