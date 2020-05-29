from utils import util
import time

class MoneyLog(object):
    def __init__(self, ticket, inType):
        # ['601878', '浙商证券', 10.01 涨幅, 6670001664 流通市值, '新股与次新股', 910193659 买入, -218535663 卖出, 691657996 净额 , 8.46 涨速, '游资' ]
        # ["601619","嘉泽新能","11.3900 股价","10.05 涨幅","2206383360 市值","228541603 买入","-138661623 卖出","89879980 净额","次新股",0,"游资","1503624707 时间"]
        self.code = ticket[0]
        self.name = ticket[1]
        self.rate = ticket[3]
        self.total = ticket[4]
        self.buy = ticket[5]
        self.sell = ticket[6]
        self.net = ticket[7]
        self.type = ticket[10]
        self.kind = ticket[8]
        if ticket[11] != '':
            self.date = time.localtime(int(ticket[12]))
        else:
            self.date = time.localtime()
        self.inType = inType
        self.fromType = 1
        self.increase = 0

        # self.add_time = ticket[3]

    def convertToTuple(self):
        return [self.name, self.buy, self.net, self.total, self.type, self.code, self.date, self.kind,
                util.todayYMDHMS(), self.rate, self.sell, self.inType, self.fromType, self.increase]
