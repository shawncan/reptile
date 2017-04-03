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


if __name__ == "__main__":
    targer = "http://python123.io/ws/demo.html"
    demo = getHTMLText(targer)
    soup = BeautifulSoup(demo, 'html.parser')
    # print(soup.find_all('p'))

    for tag in soup.find_all(True):
        print(tag.name)