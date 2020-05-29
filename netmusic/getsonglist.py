import requests
from bs4 import BeautifulSoup

url = 'https://music.163.com/playlist?id=719535779'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https//music.163.com",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Host": "music.163.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
    "Referer": "https//music.163.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1"
}

response = requests.get(url, headers=headers)
html = BeautifulSoup(response.text, 'lxml')


def getlist():
    dic = {}

    for li in html.find('ul', class_='f-hide'):
        songid = li.select('a')[0].attrs["href"][9:]
        name = li.string
        dic[songid] = name

    print(dic)
    return dic
