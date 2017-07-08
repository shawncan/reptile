#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
import base64
import rsa
import binascii


class autoWeibo(object):
    def __init__(self):
        self.parameter_url = 'https://login.sina.com.cn/sso/prelogin.php'
        self.ticket_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=1499149326610&openapilogin=qrcode'
        self.code_url = 'https://api.weibo.com/oauth2/authorize'
        self.access_token_url = 'https://api.weibo.com/oauth2/access_token'

        self.app_key = '****'
        self.app_secret = '****'
        self.redirect_uri = 'https://api.weibo.com/oauth2/default.html'
        self.username = '****'
        self.password = '****'

        self.su = ''
        self.sp = ''
        self.servertime = ''
        self.nonce = ''
        self.pubket = ''
        self.rsakv = ''
        self.code = ''
        self.access_token = ''

    def getParameter(self):
        """
        此函数用作获取微博登录的基础参数
        su为用户账号、sp为用户密码
        servertime、nonce、pubket参数为sp加密时用
        rsakv参数为ticket时用
        """
        '''base64加密用户名'''
        bytesString = self.username.encode(encoding="utf-8")
        self.su = base64.b64encode(bytesString).decode('utf-8')

        '''获取servertime、nonce、pubket、rsakv参数'''
        params = {
            'su': self.su,
            'entry': 'openapi',
            'callback': 'sinaSSOController.preloginCallBack',
            'rsakt': 'mod',
            'checkpin': '1',
            'client': 'ssologin.js(v1.4.18)',
            '_': '1499082911503'
        }

        parameter_resp = requests.get(self.parameter_url, params=params)
        parameter = parameter_resp.text.split(',')
        self.servertime = parameter[1].split(':')[1]
        self.nonce = parameter[3].split(':')[1][1:-1]
        self.pubket = parameter[4].split(':')[1][1:-1]
        self.rsakv = parameter[5].split(':')[1][1:-1]

        '''获得密码rsa加密'''
        rsa_e = '65537'
        key = rsa.PublicKey(int(self.pubket, 16), int(rsa_e))
        pw_string = str(self.servertime) + '\t' + str(self.nonce) + '\n' + str(self.password)
        ps = pw_string.encode(encoding="utf-8")
        pw_encypted = rsa.encrypt(ps, key)
        passwd = binascii.b2a_hex(pw_encypted)
        self.sp = passwd.decode()

    def getCode(self):
        """
        此函数用作获取微博登录应用授权的code
        ticket为授权时必要的参数
        code为获取access_token必要参数
        """
        '''获得ticket'''
        ticket_Para = {
            'appkey': '45d1VI',
            'cdult': '2',
            'ct': '1800',
            'domain': 'weibo.com',
            'door': '',
            'encoding': 'UTF-8',
            'entry': 'openapi',
            'from': '',
            'gateway': '1',
            'nonce': self.nonce,
            'pagerefer': '',
            'prelt': '1381',
            'pwencode': 'rsa2',
            'returntype': 'TEXT',
            'rsakv': self.rsakv,
            's': '1',
            'savestate': '0',
            'servertime': self.servertime,
            'service': 'miniblog',
            'sp': self.sp,
            'sr': '1440*900',
            'su': self.su,
            'useticket': '1',
            'vsnf': '1',
            'vsnval': '',
        }

        req = requests.post(self.ticket_url, data=ticket_Para)
        ticket = req.json()['ticket']

        '''获得code'''
        code_Data = {
            'action': 'login',
            'appkey62': '6KwNnX',
            'client_id': self.app_key,
            'display': 'default',
            'from': '',
            'isLoginSina': '',
            'passwd': '',
            'quick_auth': 'false',
            'redirect_uri': self.redirect_uri,
            'regCallback': "https://api.weibo.com/2/oauth2/authorize?client_id={app_key}&response_type=code&display=default&redirect_uri={redirect_uri}&from=&with_cookie=".format(
                app_key=self.app_key, redirect_uri=self.redirect_uri),
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

        code_headers = {
            "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0",
            "Referer": self.code_url,
            "Content-Type": "application/x-www-form-urlencoded"}

        code_return = requests.post(self.code_url, headers=code_headers, data=code_Data)
        self.code = code_return.url[47:]

    def getAccesstoken(self):
        """
        此函数用作获取微博接口调用时的access_token
        access_token为调用接口时必要的参数
        """
        access_token_Data = {
            'client_id': self.app_key,
            'client_secret': self.app_secret,
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': self.redirect_uri
        }

        r = requests.post(self.access_token_url, data=access_token_Data)
        self.access_token = r.json()['access_token']

    def start(self):
        self.getParameter()
        self.getCode()
        self.getAccesstoken()

        path = '****/count.txt'
        with open(path, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
        days = int(last_line) + 1

        weibo_Data = {
            'access_token': self.access_token,
            'status': '王灿灿正在努力吃全世界的狗粮，因为已经距离上次分手' + str(days) + '天。http://wangjiacan.com'
        }

        weibo = requests.post('https://api.weibo.com/2/statuses/share.json', data=weibo_Data)

        try:
            created_at = weibo.json()['created_at']
            if not created_at.strip():
                print(weibo.json())
            else:
                print(weibo.json()['created_at'])
                with open(path, 'a') as f:
                    f.write(str(days) + "\n")
                    f.close()
        except Exception:
            print("运行失败")

spider = autoWeibo()
spider.start()