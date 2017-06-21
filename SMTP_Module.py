#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-


import smtplib
from email.mime.text import MIMEText


def mail():
    a = [['Top1',
          '小时候有点调皮，想出去玩大人不让，于是自己偷偷的跑到同学家去，第二天早上才回来，见爸妈眼睛红红的。后来听别人说我爸妈找了我一整天没找到，还请了算命先生，算命先生说我下河游泳被淹死了我爸妈哭了一晚上，反正我当时差点没被打死'],
         ['Top2', '老师问"同学"什么是天使，一男孩说天上掉下来的大便就是天屎。']]

    html_content = ''
    rows = 0
    for top in a:
        for content in top:
            rows += 1

            if rows % 2 == 0:
                html_content = html_content + content + '\n' + '\n'
            else:
                top_start = '<font size="6">'
                top_end = '</font>'
                html_content = html_content + top_start + content + top_end + '\n'

    html_start = '<font size="5"， color="#000000", face="宋体"><pre>'
    html_end = '码农：王小灿(ง⁼̴̀ω⁼̴́)ง⁼³₌₃ </pre></font>'

    my_sender = '784241389@qq.com'
    my_pass = '*******'
    my_user = '784241389@qq.com'

    msg = MIMEText(html_start + html_content + html_end, 'html', 'utf-8')
    msg["Subject"] = "糗事精选"
    msg["From"] = my_sender
    msg["To"] = my_user

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, my_user, msg.as_string())
        server.quit()
        print('邮件发送成功')
    except Exception:
        print('邮件发送失败')


mail()
