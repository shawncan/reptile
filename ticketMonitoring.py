#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import logging
import openpyxl
import os
import json


def getHTMLText(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


if __name__ == '__main__':
    url = 'http://webresource.c-ctrip.com/code/cquery/resource/address/flight/flight_new_poi_gb2312.js?releaseno=?CR_2016_03_07_22_18_26'
    html = getHTMLText(url)
    htmlInfo = re.findall(r'([\u4e00-\u9fa5]+)\(([A-Z]{3})\)', str(html))

    a = list(set(htmlInfo))

    for i in a[0]:
        print(i)