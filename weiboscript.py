#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
import base64
import rsa
import binascii


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

# payload = {'su': 'MTU1NTcxNjg3ODE=', 'entry':'openapi', 'callback':'sinaSSOController.preloginCallBack', 'rsakt':'mod', 'checkpin':'1', 'client':'ssologin.js(v1.4.18)', '_':'1499082911503'}
# r = requests.get('https://login.sina.com.cn/sso/prelogin.php', params=payload)
# print(r.text)

# copyright = '15557168781'
# bytesString = copyright.encode(encoding="utf-8")
# encodestr = base64.b64encode(bytesString)

# print(encodestr.decode('utf-8'))


pubkey = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'
servertime = '1499082908'
nonce = 'NSZYF4'
password = 'wjc0216wjc'


rsa_e = '65537'
key = rsa.PublicKey(int(pubkey, 16), int(rsa_e))

pw_string = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
ps = pw_string.encode(encoding="utf-8")
pw_encypted = rsa.encrypt(ps, key)
passwd = binascii.b2a_hex(pw_encypted)
a = passwd.decode()
print(a)
