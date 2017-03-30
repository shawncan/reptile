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


def Search():
    search = input("请输入需要查找的手机号：")
    goal = "http://m.ip138.com/mobile.asp?mobile=" + search
    print(getHTMLText(goal))


if __name__ == "__main__":
    Search()