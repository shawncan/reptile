#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-


import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr



def mail():
    a = [['请叫我情圣大哥',
          '小时候有点调皮，想出去玩大人不让，于是自己偷偷的跑到同学家去，第二天早上才回来，见爸妈眼睛红红的。后来听别人说我爸妈找了我一整天没找到，还请了算命先生，算命先生说我下河游泳被淹死了我爸妈哭了一晚上，反正我当时差点没被打死'],
         ['病娇模拟器', '老师问"同学"什么是天使，一男孩说天上掉下来的大便就是天屎。']]

    b = ''
    for i in a:
        for x in i:
            b = b + x + '\n'


    my_sender = '784241389@qq.com'
    my_pass = '************'
    my_user = '784241389@qq.com'

    msg = MIMEText(b)
    msg["Subject"] = "糗事精选"
    msg["From"] = my_sender
    msg["To"] = my_user

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, my_user, msg.as_string())
        server.quit()
    except Exception:
        print('邮件发送失败')

mail()

