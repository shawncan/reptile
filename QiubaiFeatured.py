#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def getHTMLText(url, code='UTF-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("爬取失败")


a = 'https://www.qiushibaike.com/hot/'

html = getHTMLText(a)
soup = BeautifulSoup(html, 'html.parser')

q = soup.find_all('div', attrs={'class': 'article block untagged mb15'})

for i in q:
    img = i.find_all('div', attrs={'class': 'thumb'})

    if img:
        continue
    else:
        name = i.find('div', attrs={'class': 'author clearfix'})
        content = i.find('div', attrs={'class': 'content'})
        funny = i.find('span', attrs={'class': 'stats-vote'})

        # 用户
        name_2 = name.find('h2').text.split()[0]
        # 内容
        content_1 = content.find('span').text.split()[0]
        # 好笑人数
        funny_1 = funny.find('i').text.split()[0]

        print(name_2)
        print(content_1)
        print(funny_1)


class QSBK(object):

    def __init__(self):
        self.pageIndex = 1
        self.stories = [['Top1'], ['Top2'], ['Top3'], ['Top4'], ['Top5'], ['Top6'], ['Top7'], ['Top8'], ['Top9'],
                        ['Top10']]
        self.stats = []
