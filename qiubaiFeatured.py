#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import logging


class QSBK(object):

    def __init__(self):
        self.pageIndex = 1
        self.qs_ranking = []
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:53.0) Gecko/20100101 Firefox/53.0'
        self.headers = {'User-Agent': self.user_agent}
        # self.storepath = '/Users/wangjiacan/Desktop/代码/crawldata/qsbk.txt'
        self.storepath = '/crawldata/qsbk.txt'
        self.enable = True

        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            # filename='/Users/wangjiacan/Desktop/代码/log/QiubaiFeatured.txt',
                            filename='/log/QiubaiFeatured.txt',
                            filemode='a')

        self.logger = logging.getLogger()

    def getHTMLText(self):
        try:
            url = 'https://www.qiushibaike.com/hot/page/' + str(self.pageIndex)
            r = requests.get(url, headers=self.headers, )
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

                    conten = content_module.find('span').text
                    funn = int(funny_module.find('i').text.split()[0])

                    qs_data = {'conten': conten, 'funn': funn, }

                    if self.qs_ranking:
                        list_length = len(self.qs_ranking)
                        self.qs_ranking = sorted(self.qs_ranking, key=lambda k: k['funn'], reverse=True)
                        list_small = self.qs_ranking[-1]['funn']
                        if list_length == 10 and funn > list_small:
                            self.qs_ranking.pop()
                            self.qs_ranking.append(qs_data)
                        elif list_length < 10:
                            self.qs_ranking.append(qs_data)
                        else:
                            continue
                    else:
                        self.qs_ranking.append(qs_data)
                time.sleep(2)

            self.pageIndex += 1
            next = soup.find('span', attrs={'class': 'next'}).text.split()[0]
            if next != "下一页":
                self.enable = False
            print(self.pageIndex)
            time.sleep(20)
        except Exception:
            self.logger.exception("Extract Page {numeral} data failed".format(numeral=self.pageIndex))

    def storeData(self):
        try:
            with open(self.storepath, 'a') as f:
                f.write(time.strftime("%Y-%m-%d", time.localtime()) + "\n")
                for i in self.qs_ranking:
                    f.write(i['conten'] + "\n")
                f.write("\n")
                f.close()
        except Exception:
            self.logger.exception("File storage failed")


    def start(self):
        while self.enable:
            self.getContentExtraction()
        self.storeData()
        print("程序运行成功！")


spider = QSBK()
spider.start()
