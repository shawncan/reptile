#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
import smtplib
from email.mime.text import MIMEText
import configparser
import time
import sys


class autoWeibo(object):
    def __init__(self):
        self.redirect_uri = 'https://api.weibo.com/oauth2/default.html'
        self.access_token_url = 'https://api.weibo.com/oauth2/access_token'
        self.weibo_url = 'https://api.weibo.com/2/statuses/share.json'

        self.app_key = ''
        self.app_secret = ''
        self.code = ''
        self.access_token = ''
        self.expires_in = ''
        self.days = ''

        self.account = ''
        self.password = ''
        self.recipient = ''
        self.error = ''

    def mail(self):
        """
        此函数用作发送脚本运行失败的提醒邮件
        """
        getCodeUrl = 'https://api.weibo.com/oauth2/authorize?client_id={app_key}&redirect_uri={redirect_uri}'.format(
            app_key=self.app_key, redirect_uri=self.redirect_uri)

        line1 = "运行失败原因{error}".format(error=self.error)
        line2 = "有可能是code过期了快去授权吧~"
        line3 = "授权地址：{url}".format(url=getCodeUrl)

        msg = MIMEText(('<font color=#000000><br>{line1}<br>{line2}<br>{line3}</font>'
            .format(line1=line1, line2=line2, line3=line3)), 'html', 'utf-8')
        msg["Subject"] = "单身狗关爱程序运行失败"
        msg["From"] = self.account
        msg["To"] = self.recipient

        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(self.account, self.password)
            server.sendmail(self.account, self.recipient, msg.as_string())
            server.quit()
        except:
            print("Because the mail sending error can not be reminded to the developer, to stop the program running")
            sys.exit(0)


    def getAccesstoken(self):
        """
        此函数用作获取access_token
        """
        access_token_Data = {
            'client_id': self.app_key,
            'client_secret': self.app_secret,
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': self.redirect_uri
        }

        r = requests.post(self.access_token_url, data=access_token_Data)
        try:
            self.access_token = r.json()['access_token']
            self.expires_in = r.json()['expires_in']
        except:
            self.error = r.json()
            self.mail()
            sys.exit(0)


    def sendWeibo(self):
        """
        此函数用作发送微博
        """
        weibo_Data = {
            'access_token': self.access_token,
            'status': '王灿灿正在努力吃全世界的狗粮，因为已经距离上次分手' + str(self.days) + '天。http://wangjiacan.com'
        }

        weibo = requests.post(self.weibo_url, data=weibo_Data)

        try:
            created_at = weibo.json()['created_at']
            if not created_at.strip():
                print(weibo.json())
            self.days = int(self.days) + 1
        except:
            self.error = weibo.json()


    def start(self):
        """
        此函数用作获取配置文件信息，获取access_token，发送微博
        """
        conf = configparser.ConfigParser()
        conf.read("scriptConfiguration.ini")

        self.app_key = conf.get("singleTimer", "appKey")
        self.app_secret = conf.get("singleTimer", "appSecret")
        self.code = conf.get("singleTimer", "code")
        self.access_token = conf.get("singleTimer", "access_token")
        self.account = conf.get("singleTimer", "account")
        self.password = conf.get("singleTimer", "password")
        self.recipient = conf.get("singleTimer", "recipient")
        self.days = conf.get("singleTimer", "days")

        expireDate = conf.get("singleTimer", "expireDate")
        currentTime = time.time()
        if currentTime > float(expireDate):
            self.getAccesstoken()
            currentTime = time.time()
            newExpireDate = str(currentTime + float(self.expires_in))

            conf.set("singleTimer", "access_token", self.access_token)
            conf.set("singleTimer", "expireDate", newExpireDate)
            conf.write(open('scriptConfiguration.ini', 'w'))

        self.sendWeibo()
        conf.set("singleTimer", "days", str(self.days))
        conf.write(open('scriptConfiguration.ini', 'w'))


if __name__ == '__main__':
    run = autoWeibo()
    run.start()