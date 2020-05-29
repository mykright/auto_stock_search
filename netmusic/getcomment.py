import requests
import json
from netmusic.net_constants import headers

url = "https://music.163.com/weapi/v1/resource/comments/R_SO_4_%s?csrf_token="

coo = {

}

data = {
    "params": "jBkLj9nr8LIMFnLCFGVa7ncUWzRxuhu2NvJjxC14qW1H+GNfnR5S49IIcM/TwUzxktfZyeuFERfFLP5WTnm+tTmNq6nDXRnDAPt+o5/8B8edy7RovPmIbIPnCt9W1i9CWcNAxnXs6wiqel2y7cltkQxbri6qW0WmlSpDQyv7cQx/+Gdi7uKW6hYCmVJD+oa8",
    "encSecKey": "88c4b6c4660a216fc83660f02fa1eec6057aeef7d261b0e3c6e38f8cf64364a9f6fbf12d3116137fce1c8b0fb8ac1a5b1ada89a48c2908ddee35c5bda6bb9f1d4ca4b0c8cc691c6ce079a4137e9598d544a9aa96330c5e963cb851aaa133967de8db25da556571fa0c32c30b49dfebac5f1f24d5738fcfdf39807cf43ba875cb"
}


def getcomment(id):
    comment = []
    response = requests.post(url % id, data, headers=headers)
    for com in json.loads(response.text)["hotComments"]:
        comment.append(com["content"])
    print('id:%s finish' % id)
    return comment
