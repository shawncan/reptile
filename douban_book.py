#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import logging
import urllib.parse
import xlsxwriter
import threading
import queue
import datetime
import time


class DBTS(object):
    def __init__(self):

        self.number = 0
        self.book_name = ''
        self.book_list = []
        self.q = queue.Queue()

        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='/Users/wangjiacan/Desktop/代码/log/DBTS.txt',
                            filemode='a')

        self.logger = logging.getLogger()

    def getHTMLText(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = 'utf-8'
            return r.text
        except Exception:
            self.logger.exception("Download HTML Text failed")

    def getHTMLUrl(self, url):
        html = self.getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')
        try:
            paginator = soup.find(attrs={'class': 'paginator'})
            page = paginator.find_all('a')

            for i in range(len(page)):
                next = page[i].text
                page_url = page[i].attrs['href']
                if next == "后页>":
                    continue
                self.q.put(page_url)
        except Exception:
            self.logger.exception("Site link extraction failed")

    def getContentExtraction(self, url):
        html = self.getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')

        try:
            indent = soup.find(attrs={'class': 'indent'})
            pl2 = indent.find_all(attrs={'class': 'pl2'})
            pl = indent.find_all('p', attrs={'class': 'pl'})
            rating_nums = indent.find_all(attrs={'class': 'rating_nums'})
            span_pl = indent.find_all('span', attrs={'class': 'pl'})
            item = indent.find_all('tr', attrs={'class': 'item'})

            for i in range(len(pl2)):
                book_data = {'书名': '', '作者': '', '评分': '', '评价人数': '', '评语': '', }

                self.book_name = pl2[i].a.attrs['title']
                book_information = pl[i].text
                author = book_information.split('/')[0]
                score = rating_nums[i].text
                number_of_comments = re.findall(r'\d*人评价', str(span_pl[i]))[0]

                inq = re.findall(r'\<span class\=\"inq\"\>.*\<\/span\>', str(item[i]))
                if inq:
                    comments = inq[0][18:-7]
                else:
                    comments = ""

                book_data['书名'] = self.book_name
                book_data['作者'] = author
                book_data['评分'] = score
                book_data['评价人数'] = number_of_comments
                book_data['评语'] = comments

                self.book_list.append(book_data)
        except Exception:
            self.logger.exception("Extract page {number} {name} message failed".format(number=self.number , name=self.book_name))

    def start(self):
        start = datetime.datetime.now()
        initial_url = 'https://book.douban.com/top250?start=0'
        self.q.put(initial_url)
        self.getHTMLUrl(initial_url)

        # for i in range(self.q.qsize()):
        #     self.number += 1
        #     self.getContentExtraction(self.q.get())

        for i in range(self.q.qsize()):
            self.number += 1
            t = threading.Thread(target=self.getContentExtraction, args=(self.q.get()))
            t.start()

        time.sleep(2)
        print(self.book_list)
        print(len(self.book_list))
        end = datetime.datetime.now()
        print('运行时间：{time}'.format(time=(end - start)))


spider = DBTS()
spider.start()



