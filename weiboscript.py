#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
import base64
import rsa
import binascii

# url = 'https://api.weibo.com/oauth2/authorize'
#
# payload = {'client_id': '2533105686', 'redirect_uri': 'https://api.weibo.com/oauth2/default.html'}
#
# html = requests.get(url, params=payload)
# print(html.url)


'''base64加密用户名'''
username = '15557168781'
bytesString = username.encode(encoding="utf-8")
su = base64.b64encode(bytesString).decode('utf-8')


'''获取servertime、nonce、pubket、rsakv参数'''
params = {
    'su': su,
    'entry': 'openapi',
    'callback': 'sinaSSOController.preloginCallBack',
    'rsakt': 'mod',
    'checkpin': '1',
    'client': 'ssologin.js(v1.4.18)',
    '_': '1499082911503'
}
r = requests.get('https://login.sina.com.cn/sso/prelogin.php', params=params)
a = r.text.split(',')
servertime = a[1].split(':')[1]
nonce = a[3].split(':')[1][1:-1]
pubket = a[4].split(':')[1][1:-1]
rsakv = a[5].split(':')[1][1:-1]


'''获得密码rsa加密'''
password = 'wjc0216wjc'
rsa_e = '65537'
key = rsa.PublicKey(int(pubket, 16), int(rsa_e))
pw_string = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
ps = pw_string.encode(encoding="utf-8")
pw_encypted = rsa.encrypt(ps, key)
passwd = binascii.b2a_hex(pw_encypted)
sp = passwd.decode()


'''获得ticket'''
postPara = {
    'appkey': '45d1VI',
    'cdult': '2',
    'ct': '1800',
    'domain': 'weibo.com',
    'door': '',
    'encoding': 'UTF-8',
    'entry': 'openapi',
    'from': '',
    'gateway': '1',
    'nonce': nonce,
    'pagerefer': '',
    'prelt': '1381',
    'pwencode': 'rsa2',
    'returntype': 'TEXT',
    'rsakv': rsakv,
    's': '1',
    'savestate': '0',
    'servertime': servertime,
    'service': 'miniblog',
    'sp': sp,
    'sr': '1440*900',
    'su': su,
    'useticket': '1',
    'vsnf': '1',
    'vsnval': '',
}

ticket_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=1499149326610&openapilogin=qrcode'
req = requests.post(ticket_url, data=postPara)
ticket = req.json()['ticket']


'''获得code'''
app_key = '2533105686'
redirect_uri = 'https://api.weibo.com/oauth2/default.html'

codePara = {
    'action': 'login',
    'appkey62': '45d1VI',
    'client_id': app_key,
    'display': 'default',
    'from': '',
    'isLoginSina': '',
    'passwd': '',
    'quick_auth': 'false',
    'redirect_uri': redirect_uri,
    'regCallback': "https://api.weibo.com/2/oauth2/authorize?client_id={0}&response_type=code&display=default&redirect_uri={1}&from=&with_cookie=".format(
        app_key, redirect_uri),
    'response_type': 'code',
    'scope': '',
    'state': '',
    'switchLogin': '0',
    'ticket': ticket,
    'userId': '',
    'verifyToken': 'null',
    'withOfficalAccount': '',
    'withOfficalFlag': '0'
}

code_url = 'https://api.weibo.com/oauth2/authorize'
headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
    "Referer": code_url,
    "Content-Type": "application/x-www-form-urlencoded"}
code_return = requests.post(code_url, headers=headers, data=codePara)
code = code_return.url[47:]
print(code)


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

# access_token = '2.00VDESSG1Ve7lC302cb2d77bDc21hB'
#
# payload_2 = {
#     'access_token': '2.00VDESSG1Ve7lC302cb2d77bDc21hB',
#     'status': '王灿灿正在努力的吃狗粮，因为已经分手49天',
#
# }
#
# r = requests.post('https://api.weibo.com/2/statuses/update.json', data=payload_2)
#
# print(r.json())