#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


class QSBK(object):

    def __init__(self):
        self.pageIndex = 1
        self.stories = [['Top1'], ['Top2'], ['Top3'], ['Top4'], ['Top5'], ['Top6'], ['Top7'], ['Top8'], ['Top9'],
                        ['Top10']]
        self.stats = []

    def getHTMLText(self):
        try:
            url = 'https://www.qiushibaike.com/hot/page/' + str(self.pageIndex)
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = 'UTF-8'
            return r.text
        except:
            print("爬取失败")

    def getContentExtraction(self):
        html = self.getHTMLText()
        soup = BeautifulSoup(html, 'html.parser')

        Qiushi_module = soup.find_all('div', attrs={'class': 'article block untagged mb15'})

        for i in Qiushi_module:
            img = i.find_all('div', attrs={'class': 'thumb'})

            if img:
                continue
            else:
                content_module = i.find('div', attrs={'class': 'content'})
                funny_module = i.find('span', attrs={'class': 'stats-vote'})

                conten = content_module.find('span').text.split()[0]
                funn = funny_module.find('i').text.split()[0]

                if self.stats:
                    self.stats.sort()
                    if len(self.stats) == 10 and funn > self.stats[0]:
                        self.stats.pop(0)
                        self.stats.append(funn)

                    elif len(self.stats) < 10:
                        self.stats.append(funn)
                    else:
                        continue
                else:
                    self.stats.append(funn)


spider = QSBK()
spider.getContentExtraction()