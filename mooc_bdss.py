#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬去失败")


def bdSearch():
    search = input("请输入搜索内容：")
    goal = "http://www.baidu.com/s?wd=" + search
    print(getHTMLText(goal))


if __name__ == "__main__":
    bdSearch()
