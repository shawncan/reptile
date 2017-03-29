#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests


def getHTMLText(url):
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


if __name__ == "__main__":
    goal = "https://www.amazon.cn/dp/B01FLLMPJQ"
    print(getHTMLText(goal))
