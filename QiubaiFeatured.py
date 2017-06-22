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



spider = QSBK()
spider.getContentExtraction()