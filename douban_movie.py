#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import logging


class DBDY(object):
    def __init__(self):
        self.page = 0
        self.dbdy_url = 'https://movie.douban.com/top250?start=' + str(self.page) + '&filter='
        self.movie_information = {'排名': '', '电影': '', '上映时间': '', '国家': '', '简介': '', '播放地址': '', }
        self.movie_name = ''
        self.movie_details = 'https://movie.douban.com/subject/1292052/'
        self.aiqiyi_url = ''

        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='/Users/wangjiacan/Desktop/code/log/DBDS.txt',
                            # filename='/log/QiubaiFeatured.txt',
                            filemode='a')

        self.logger = logging.getLogger()

    def getHTMLText(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = 'UTF-8'
            return r.text
        except Exception:
            self.logger.exception("Download Page {numeral} Code failed".format(numeral=self.page))

    def getLinkExtraction(self):
        html = self.getHTMLText(self.movie_details)
        soup = BeautifulSoup(html, 'html.parser')
        playBtn = soup.find_all(attrs={'class': "playBtn"})

        for i in range(len(playBtn)):
            platform = playBtn[i].attrs['data-cn']
            target_platform = '爱奇艺视频'
            if platform == target_platform:
                print(playBtn[i].attrs['href'])
            else:
                continue

    def getContentExtraction(self):
        html = self.getHTMLText(self.dbdy_url)
        soup = BeautifulSoup(html, 'html.parser')

        try:
            ranking = soup.find('ol')
            details = ranking.find_all('div', attrs={'class': "pic"})
            movie_information = ranking.find_all('p', attrs={'class': ""})
            inq = ranking.find_all('span', attrs={'class': "inq"})
            item = ranking.find_all('div', attrs={'class': "item"})

            for i in range(len(details)):
                self.movie_name = details[i].img.attrs['alt']
                self.movie_details = details[i].a.attrs['href']
                movie_rankings = details[i].em.text
                release_time = re.findall(r'\d{4}', movie_information[i].text)[0]
                film_origin = re.findall(r'/\xa0.*\xa0/', movie_information[i].text)[0][2:-2]
                movie_synopsi = inq[i].text

                movie_resources = re.findall(r'\[.*\]', item[i].text)
                if movie_resources:
                    self.getLinkExtraction()

                self.movie_information['排名'] = movie_rankings
                self.movie_information['电影'] = self.movie_name
                self.movie_information['上映时间'] = release_time
                self.movie_information['国家'] = film_origin
                self.movie_information['简介'] = movie_synopsi
                self.movie_information['播放地址'] = self.aiqiyi_url
                print(self.movie_information)

        except Exception:
            self.logger.exception("Download Page {numeral} Code failed".format(numeral=self.movie_name))

spider = DBDY()
spider.getLinkExtraction()




