import requests
from bs4 import BeautifulSoup


no = '1CLBX-20200119036'

URL = "http://oa.qunhequnhe.com:1808/workflow/search/WFSearchResult.jsp?offical=&officalType=-1&viewType=0"

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Cookie":"wfcookie=2; _ga=GA1.2.65163591.1570775777; gr_user_id=fed66b60-d9e6-47e8-b86f-276fe8a1c120; ecology_JSessionId=abcpIXk1BUUwWhmvNc67w; JSESSIONID=abcpIXk1BUUwWhmvNc67w; testBanCookie=test; grwng_uid=bcd29155-3389-4eb6-8433-e64993ec0ece; _hjid=1d714dbd-43d5-4a43-9cd3-78259b728f3c; _gid=GA1.2.639520164.1586768887; qunhe-jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1ODk3MTAxNTA4MDQsImtfaWQiOiIzRk8yVVhTQVU5WVMiLCJ1dCI6NSwiYyI6MTU4NzExODE1MDgwNCwiZSI6MTU4OTcxMDE1MDgwNCwidXYiOjQsImlhZSI6ZmFsc2UsImlwdSI6ZmFsc2UsImFfaWQiOjE5OTIyMzc5ODcsInJfaWQiOjE5OTIyMzc5ODd9.k1GXpeDuPy7djjnqERajA4Jdh5P_6N4DLDHF3JI7vp8; a1c39d23c37d5e95_gr_last_sent_cs1=3FO2UXSAU9YS; a1c39d23c37d5e95_gr_cs1=3FO2UXSAU9YS; loginfileweaver=%2Fwui%2Ftheme%2Fecology8%2Fpage%2Flogin.jsp%3FtemplateId%3D3%26logintype%3D1%26gopage%3D; languageidweaver=7; loginidweaver=1328",
    "Host":"oa.qunhequnhe.com:1808",
    "Origin":"http://oa.qunhequnhe.com:1808",
    "Pragma":"no-cache",
    "Referer":"http://oa.qunhequnhe.com:1808/workflow/search/WFSearchResult.jsp?resourceid=1328&needHeader=false&viewcondition=0&offical=&officalType=-1&start=1&iswaitdo=1&viewType=0&processing=0&viewScope=doing&numberType=&officalType=-1&viewcondition=0&viewScope=doing&offical=&method=all&wftypes=&complete=0",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
}

data = {
    "flowTitle": no,
    "requestname": no,
    "createdateselect": "0",
    "creatertype": "0",
    "recievedateselect": "0",
    "fromself": "1",
    "isfirst": "1",
    "fromselfSql": "__random__C608062A066ABA6AF1DEA08725671C5C",
    "iswaitdo": "1",
    "officalType": "-1",
    "viewcondition": "0",
    "isovertime": "0",
    "viewType": "0",
    "pageId": "Wf:pendingMatters",
    "start": "1",
    "viewScope": "doing",
    "needHeader": "false",
    "method": "all",
    "processing": "0",
    "complete": "0",
    "resourceid": "1328",
    "pageSizeSel1inputText": "10",
    "pageSizeSel1": "10",
    "needShow": "0",
    "tableMax": "10"
}

def submit(flNo):
    data["flowTitle"] = flno
    data["requestname"] = flno
    response = requests.post(URL,data, headers=headers)
    # print(response.text)

    name = "__tableStringKey__";
    index = response.text.index(name)
    id = response.text[index+20:index+52]

    URL2 = "http://oa.qunhequnhe.com:1808/weaver/weaver.common.util.taglib.SplitPageXmlServlet?tableInstanceId=&tableString="+id+"&pageIndex=0&orderBy=null&otype=null&mode=run&customParams=null&selectedstrs=&pageId=Wf:pendingMatters"
    response = requests.get(URL2, headers=headers)
    # print(response.text)
    html = BeautifulSoup(response.text, 'lxml')
    print("-----------------")
    subid = html.find("row").find("col").get("linkvalue")
    print(subid)
    URL3 = "http://oa.qunhequnhe.com:1808/workflow/request/RequestListOperation.jsp?multiSubIds="+subid+",&workflowid=&method=all&wftype=&flowAll=0&flowNew=0&viewcondition=0&pagefromtype=1&belongtoUserids=,"
    response = requests.post(URL3, headers=headers)
    print(response.text)
    print('流程 %s 已执行,请确认' % flNo)


for flno in no.split(","):
    print(flno)
    try:
        submit(flno)
    except Exception:
        print("流程异常: %s" % flno)