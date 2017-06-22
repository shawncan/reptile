#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import logging


class QSBK(object):

    def __init__(self):
        self.pageIndex = 1
        self.stories = [['Top1'], ['Top2'], ['Top3'], ['Top4'], ['Top5'], ['Top6'], ['Top7'], ['Top8'], ['Top9'],
                        ['Top10']]
        self.stats = []
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
        self.headers = {'User-Agent': self.user_agent}
        self.enable = True

        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='/Users/wangjiacan/Desktop/代码/log/OtakuGirlPicture.txt',
                            filemode='a')

        self.logger = logging.getLogger()

    def getHTMLText(self):
        try:
            url = 'https://www.qiushibaike.com/hot/page/' + str(self.pageIndex)
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            r.encoding = 'UTF-8'
            return r.text
        except Exception:
            self.logger.exception("Download Page {numeral} Code failed".format(numeral=self.pageIndex))

    def getContentExtraction(self):
        html = self.getHTMLText()
        soup = BeautifulSoup(html, 'html.parser')

        try:
            Qiushi_module = soup.find_all('div', attrs={'class': 'article block untagged mb15'})

            for i in Qiushi_module:
                img = i.find_all('div', attrs={'class': 'thumb'})

                if img:
                    continue
                else:
                    content_module = i.find('div', attrs={'class': 'content'})
                    funny_module = i.find('span', attrs={'class': 'stats-vote'})

                    conten = content_module.find('span').text.split()[0]
                    funn = int(funny_module.find('i').text.split()[0])

                    if self.stats:
                        list_length = len(self.stats)
                        list_small = min(self.stats)
                        position = self.stats.index(list_small)
                        if list_length == 10 and funn > list_small:
                            self.stats.insert(position, funn)
                            self.stats.remove(list_small)
                            self.stories[position].pop()
                            self.stories[position].append(conten)
                        elif list_length < 10:
                            self.stats.append(funn)
                            self.stories[list_length].append(conten)
                        else:
                            continue
                    else:
                        self.stats.append(funn)
                        self.stories[0].append(conten)
                time.sleep(2)

            self.pageIndex += 1
            next = soup.find('span', attrs={'class': 'next'}).text.split()[0]
            if next != "下一页":
                self.enable = False
            print(self.stories)
            time.sleep(20)
        except Exception:
            self.logger.exception("Extract Page {numeral} data failed".format(numeral=self.pageIndex))


    def mail(self):
        html_content = ''
        rows = 0
        for top in self.stories:
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
        my_pass = 'vytugytpvftebdcb'
        my_user = '784241389@qq.com'

        msg = MIMEText(html_start + html_content + html_end, 'html', 'utf-8')
        mail_time = time.strftime("%Y-%m-%d", time.localtime())
        msg["Subject"] = mail_time + "糗事精选"
        msg["From"] = my_sender
        msg["To"] = my_user

        try:
            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            server.login(my_sender, my_pass)
            server.sendmail(my_sender, my_user, msg.as_string())
            server.quit()
        except Exception:
            self.logger.exception("E-mail failed to send")

    def start(self):
        while self.enable:
            self.getContentExtraction()

        self.mail()


spider = QSBK()
spider.start()
