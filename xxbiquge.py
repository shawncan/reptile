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
import os


def getHTMLText(url):
    """
    下载目标网页源码
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception:
        logger.exception("Download HTML Text failed")


def getHTMKUrl(url):
    """
    提取本书所有章节的链接
    """
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        title_list = soup.find(attrs={'id': 'list'})
        dd = title_list.find_all('dd')
        for i in range(len(dd)):
            chapter_url = dd[i].attrs['href']
            url_queue.put(chapter_url)
    except Exception:
        logger.exception("Site link extraction failed")


def getContentExtraction(url_path):
    """
    提取每个章节的文本到txt中
    """
    chapter_url = 'http://www.xxbiquge.com/' + url_path
    html = getHTMLText(chapter_url)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        box_con = soup.find(attrs={'class': 'box_con'})
        bookname = box_con.find_all(attrs={'class': 'bookname'})[0]
        # print(bookname.h1.text)
        content = box_con.find_all(attrs={'id': 'content'})[0]
        print(content.text)
    except Exception:
        logger.exception("Extract page message failed")

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/xxbiquge.txt',
                        filemode='a')

    logger = logging.getLogger()
    url_queue = queue.Queue()

    # title = input("请输入要下载的笔趣链接：")
    # getHTMKUrl(str(title))
    text_url = '/2_2368/4164741.html'
    getContentExtraction(text_url)
