#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
import base64
import rsa
import binascii
import time

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

# '''获得ticket'''
# postPara = {
#     'appkey': '45d1VI',
#     'cdult': '2',
#     'ct': '1800',
#     'domain': 'weibo.com',
#     'door': '',
#     'encoding': 'UTF-8',
#     'entry': 'openapi',
#     'from': '',
#     'gateway': '1',
#     'nonce': nonce,
#     'pagerefer': '',
#     'prelt': '1381',
#     'pwencode': 'rsa2',
#     'returntype': 'TEXT',
#     'rsakv': rsakv,
#     's': '1',
#     'savestate': '0',
#     'servertime': servertime,
#     'service': 'miniblog',
#     'sp': sp,
#     'sr': '1440*900',
#     'su': su,
#     'useticket': '1',
#     'vsnf': '1',
#     'vsnval': '',
# }
#
# ticket_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=1499149326610&openapilogin=qrcode'
# req = requests.post(ticket_url, data=postPara)
# ticket = req.json()['ticket']

#
# '''获得code'''
# app_key = '2811141451'
# redirect_uri = 'https://api.weibo.com/oauth2/default.html'
#
# codePara = {
#     'action': 'login',
#     'appkey62': '6KwNnX',
#     'client_id': app_key,
#     'display': 'default',
#     'from': '',
#     'isLoginSina': '',
#     'passwd': '',
#     'quick_auth': 'false',
#     'redirect_uri': redirect_uri,
#     'regCallback': "https://api.weibo.com/2/oauth2/authorize?client_id={0}&response_type=code&display=default&redirect_uri={1}&from=&with_cookie=".format(
#         app_key, redirect_uri),
#     'response_type': 'code',
#     'scope': '',
#     'state': '',
#     'switchLogin': '0',
#     'ticket': ticket,
#     'userId': '',
#     'verifyToken': 'null',
#     'withOfficalAccount': '',
#     'withOfficalFlag': '0'
# }

# codePara = {
#     'action': 'authorize',
#     'appkey62': '6KwNnX',
#     'client_id': app_key,
#     'display': 'default',
#     'from': '',
#     'isLoginSina': '',
#     'redirect_uri': redirect_uri,
#     'regCallback': "https://api.weibo.com/2/oauth2/authorize?client_id={0}&response_type=code&display=default&redirect_uri={1}&from=&with_cookie=".format(
#         app_key, redirect_uri),
#     'response_type': 'code',
#     'scope': '',
#     'state': '',
#     'ticket': '',
#     'uid': '5767076537',
#     'url': "https://api.weibo.com/oauth2/authorize?redirect_uri={0}&client_id={1}".format(redirect_uri, app_key),
#     'verifyToken': 'f3ea46f5ae1e913baabb6e11c836f597',
#     'visible': '0',
#     'withOfficalAccount': '',
#     'withOfficalFlag': '0'
# }

#
# code_url = 'https://api.weibo.com/oauth2/authorize'
# headers = {
#     "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0",
#     "Referer": code_url,
#     "Content-Type": "application/x-www-form-urlencoded"}
#
# code_return = requests.post(code_url, headers=headers, data=codePara)
# code = code_return.url[47:]
#
# '''获取access_token'''
# app_secret = 'e8090ffc41d9e21bc195f7160abb8952'
#
# payload_1 = {
#     'client_id': app_key,
#     'client_secret': app_secret,
#     'grant_type': 'authorization_code',
#     'code': code,
#     'redirect_uri': redirect_uri
# }
#
# r = requests.post('https://api.weibo.com/oauth2/access_token', data=payload_1)
# access_token = r.json()['access_token']
# expires_in = r.json()['expires_in']
# uid = r.json()['uid']


# '''发送微博'''
# payload_2 = {
#     'access_token': access_token,
#     'status': '王灿灿正在努力吃全世界的狗粮，因为已经距离上次分手52天。http://wangjiacan.com'
# }
#
# r = requests.post('https://api.weibo.com/2/statuses/share.json', data=payload_2)
#
# print(r.json())


# '''第二种发送微博的方法'''
# '''获得Cookie'''
#
# postPara = {
#     'encoding': 'UTF-8',
#     'entry': 'weibo',
#     'from': '',
#     'gateway': '1',
#     'nonce': nonce,
#     'pagerefer': 'http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http://weibo.com/logout.php?backurl=%2F',
#     'prelt': '206',
#     'pwencode': 'rsa2',
#     'qrcode_flag': 'false',
#     'returntype': 'META',
#     'rsakv': rsakv,
#     'savestate': '7',
#     'servertime': servertime,
#     'service': 'miniblog',
#     'sp': sp,
#     'sr': '1440*900',
#     'su': su,
#     'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
#     'useticket': '1',
#     'vsnf': '1',
# }
#
# ticket_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
# req = requests.post(ticket_url, data=postPara)
# ticket = req.cookies
#
# SCF = ticket['SCF']
# SUBP = ticket['SUBP']
# SUHB = '0cSXZtc9OqqAlT'
# UOR = 'www.baidu.com,weibo.com,login.sina.com.cn'
# SINAGLOBAL = '6426740726008.886.1499221066162'
# ULV = '1499240369901:3:3:3:1942127623044.283.1499240369894:1499233820185'
# un = '15557168781'
# wb_publish_fist100_5767076537 = '1'
# YF = 'ea90f703b7694b74b62d38420b5273df'
# SUB = ticket['SUB']
# login = '6b98d2404605c519dc0f2c4f39e9ee5a'
# V5 = '35ff6d315d1a536c0891f71721feb16e'
# tentry = '-'
# Apache = '1942127623044.283.1499240369894'
# Page = '4c69ce1a525bc6d50f53626826cd2894'
# ALF = ticket['ALF']
# SSOLoginState = '1499242692'
# wvr = '6'
#
# cookies = 'SCF={SCF};SUBP={SUBP};SUHB={SUHB};UOR={UOR};SINAGLOBAL={SINAGLOBAL};ULV={ULV};un={un};wb_publish_fist100_5767076537={wb_publish_fist100_5767076537};' \
#           'YF-Ugrow-G0={YF};SUB={SUB};logi={login};YF-V5-G0={V5};_s_tentry={tentry};Apache={Apache};YF-Page-G0={Page};ALF={ALF};SSOLoginState={SSOLoginState};' \
#           'wvr={wvr}'.format(SCF=SCF, SUBP=SUBP, SUHB=SUHB, UOR=UOR, SINAGLOBAL=SINAGLOBAL, ULV=ULV, un=un, wb_publish_fist100_5767076537=wb_publish_fist100_5767076537,
#                              YF=YF, SUB=SUB, login=login, V5=V5, tentry=tentry, Apache=Apache, Page=Page, ALF=ALF, SSOLoginState=SSOLoginState, wvr=wvr)
#
#
# payload = {
#     '_t': '0',
#     'appkey': '',
#     'location': 'v6_content_home',
#     'module': 'stissue',
#     'pdetail': '',
#     'pic_id': '',
#     'pub_source': 'main_',
#     'pub_type': 'dialog',
#     'rank': '0',
#     'rankid': '',
#     'style_type': '1',
#     'text': '真测试下~',
#     'tid': ''
# }
# headers = {
#     'Referer': 'http://weibo.com/u/5767076537/home?wvr=5',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Cookie': cookies
# }
#
# a = int(time.time() * 1000)
# url = 'http://weibo.com/aj/mblog/add?ajwvr=6&__rnd=' + str(a)
#
# html = requests.post(url, headers=headers, data=payload)
# print(html.text)
