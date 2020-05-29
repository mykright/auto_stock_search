import requests

url = "http://10.100.20.30/api/merchantTest/createWxShop?userId="


coo = {
    "__mgjuuid" : "89c5118a-439b-4bc0-9739-2a16d940db55",
    "__mogujie" : "b0jaRpdI6NXyX89sxG4BPjzaP2IKsSuylumTY2oZHry531lbxnNiR9J23plI1VSU9kCxxoBrZGkm65a%2Fjbyk%2Bg%3D%3D",
    "__ud_" : "11ko1fba",
    "__must_from": "290001100_"
}

 with open("temp.txt", "r", encoding="utf-8") as f:
    for line in f:
        if line:
            res = requests.get(url + line.strip('\n'),cookies = coo)
            print(res.text)


'''
SELECT userId FROM `ws_shop_info` WHERE shopType=2 and features not like '%wxBussinessId%' where id > 1219097

'''