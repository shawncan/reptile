#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, 'html.parser')
    for tr in soup.find('tbody').children:
        if tr.name is not None:
            ts = tr('td')[0].contents
            ulist.append([ts[0].string, ts[1].string, ts[2].string])


def printUnivList(ulist, num):
    tplt = "{0:^10}\t{1:{3}^10}\t{2:^10}"
    print(tplt.format("排名", "学校名称", "总分", chr(12288)))
    for i in range(num):
        u = ulist[i]
        print(tplt.format(u[0], u[1], u[2], chr(12288)))


def main():
    unifo = []
    targer = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2017.html'
    html = getHTMLText(targer)
    fillUnivList(unifo, html)
    printUnivList(unifo, 50)


if __name__ == "__main__":
    main()
