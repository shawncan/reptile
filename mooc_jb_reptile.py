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
        return "爬取失败"


if __name__ == "__main__":
    goal = "http://item.jd.com/4110748.html"
    print(getHTMLText(goal))
