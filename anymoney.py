import xlrd

from obj.oper import Oper

data = xlrd.open_workbook("C:\\Users\\Kright\\Documents\\20170827.xls", encoding_override="utf-8")

table = data.sheets()[0]

codeMap = {}

for i in range(table.nrows):
    if i == 0:
        continue
    row = table.row_values(i)
    if not str(row[4]).__contains__("申购配号"):
        oper1 = Oper(row[3], row[5], row[10], row[4], row[6], str(row[0]) + "@ " + str(row[1]))
        operList = None
        if row[3] in codeMap:
            operList = codeMap[row[3]]
            operList.append(oper1)
        else:
            operList = [oper1]
        codeMap[row[3]] = operList


totalMoney = 0
moneyMap = {}
for oneOper in codeMap:
    num = 0
    money = 0
    for oper in codeMap[oneOper]:
        num += oper.num

        money = money + oper.money if oper.num > 0 else money - oper.money
    if num == 0:
        # print("%s 战果 %s" % (oneOper, -money))
        totalMoney += -money
        moneyMap[oneOper] = -money
    # else:
        # print("%s 持仓中" % (oneOper))

print(sorted(moneyMap.items(), key=lambda d: d[1]))

print("总战果 %s" % totalMoney)