class Oper(object):
    def __init__(self):
        pass

    def __init__(self, name, price, money, opertype, num, date):
        self.name = name
        self.price = price
        self.money = money
        self.opertype = opertype
        self.num = num
        self.date = date

    # def __str__(self):
    #     return str(self.)
    def __str__(self):
        return ','.join(['%s:%s' % item for item in self.__dict__.items()])
