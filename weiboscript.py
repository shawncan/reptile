#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests



url = 'https://api.weibo.com/oauth2/authorize'

payload = {'client_id': '2533105686', 'redirect_uri': 'https://api.weibo.com/oauth2/default.html'}

html = requests.get(url, params=payload)
# print(html.url)

# payload_1 = {
#     'client_id': '2533105686',
#     'client_secret': '4d9945487d33cbeed5f10daf69834b4c',
#     'grant_type': 'authorization_code',
#     'code': 'a2b9c3999cdd17ca56c660deb12b0ba6',
#     'redirect_uri': 'https://api.weibo.com/oauth2/default.html'
# }
#
# r = requests.post('https://api.weibo.com/oauth2/access_token', data=payload_1)
#
# data = r.json()
# print(r.json())
# print(data['access_token'])

access_token = '2.00VDESSG1Ve7lC302cb2d77bDc21hB'

payload_2 = {
    'access_token': '2.00VDESSG1Ve7lC302cb2d77bDc21hB',
    'status': '王灿灿正在努力的吃狗粮，因为已经分手49天',

}

r = requests.post('https://api.weibo.com/2/statuses/update.json', data=payload_2)

print(r.json())