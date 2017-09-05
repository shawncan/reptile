#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import logging
import queue
import datetime


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
        info = soup.find_all(attrs={'id': 'info'})[0].h1.text
        title_list = soup.find(attrs={'id': 'list'})
        dd = title_list.find_all('dd')
        for i in range(len(dd)):
            chapter_url = dd[i].a.attrs['href']
            url_queue.put(chapter_url)
        return info
    except Exception:
        logger.exception("Site link extraction failed")


def getContentExtraction(url_path, path):
    """
    提取每个章节的文本到txt中
    """
    chapter_url = 'http://www.xxbiquge.com/' + url_path
    text = []
    html = getHTMLText(chapter_url)
    soup = BeautifulSoup(html, 'html.parser')
    try:
        box_con = soup.find(attrs={'class': 'box_con'})
        bookname = box_con.find_all(attrs={'class': 'bookname'})[0].h1.text
        text.append(bookname)
        content = box_con.find_all(attrs={'id': 'content'})[0].text.split("    ")
        for con in content:
            if con:
                text.append(con)
            else:
                continue

        with open(path, 'a') as f:
            for i in text:
                f.write("  " + i + "\n")
            f.close()
        print("\r当前进度:{:.2f}%".format(number * 100 / chapter_number, end=""))
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
    number = 0

    print("笔趣小说爬虫爬取开始...")
    start = datetime.datetime.now()

    title = input("请输入要下载的笔趣链接：")
    title_name = getHTMKUrl(str(title))
    title_path = '/Users/wangjiacan/Desktop/shawn/爬取资料/' + str(title_name) + '.txt'
    chapter_number = url_queue.qsize()

    for t in range(url_queue.qsize()):
        number += 1
        getContentExtraction(url_queue.get(), title_path)

    end = datetime.datetime.now()
    print("笔趣小说爬虫爬取结束...")
    print('运行时间：{time}'.format(time=(end - start)))
