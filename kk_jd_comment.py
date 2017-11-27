#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import logging
import openpyxl
import threading
import queue
import datetime
import time
import os
import json
import demjson


def getHTMLText(url):
    """
    下载目标网页源码
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
    }
    proxies = {
        "http": "http://112.95.91.56:9797",
        "https": "http://112.95.91.56:9797",
    }

    # try:
    r = requests.get(url, headers=headers, proxies=proxies, timeout=20)
    r.raise_for_status()
    r.encoding = 'GBK'
    return r.text
    # except Exception:
    #     logger.exception("Download HTML Text failed")


def getContentExtraction():
    page_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv445&productId=4183290&score=2&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'
    html = getHTMLText(page_url)
    a = html[25:-2]

    # json_obj = demjson.encode(html)
    return_josn = json.loads(a)
    print(return_josn['comments'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/kk_jd_comment.txt',
                        filemode='a')

    logger = logging.getLogger()

    getContentExtraction()