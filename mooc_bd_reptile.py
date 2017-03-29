#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import requests
import time


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text[0:1000]
    except:
        print("爬取失败")


def reptileTime():
    goal = "http://www.baidu.com"
    start = time.time()
    for i in range(100):
        getHTMLText(goal)
    end = time.time()
    time_consuming = time.strftime("%M:%S", time.localtime(end - start))
    print("爬去百度100次所用的时间为:", time_consuming)


if __name__ == "__main__":
    reptileTime()
