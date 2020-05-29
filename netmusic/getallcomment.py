import time
from netmusic import getsonglist
from netmusic import getcomment

dic = getsonglist.getlist()

with open('comments.txt', "w", encoding="utf-8") as f1:
    for id,name in dic.items():
        f1.write('曲名：%s \n' % name)
        index = 1
        for comment in getcomment.getcomment(id):
            f1.write(str(index) + "，" + comment + '\n')
            index = index + 1
        time.sleep(3)
        f1.write('-------------------------------------------------------------------------------------\n')

