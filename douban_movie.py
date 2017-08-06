#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import logging
import urllib.parse
import xlsxwriter


class DBDY(object):
    def __init__(self):
        self.page = 0
        self.dbdy_url = ''
        self.movie_list = []
        self.movie_name = ''
        self.movie_details = ''
        self.row = 1
        self.enable = True

        logging.basicConfig(level=logging.WARNING,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='/Users/wangjiacan/Desktop/代码/log/DBDS.txt',
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

    def getLinkExtraction(self, data):
        html = self.getHTMLText(self.movie_details)
        soup = BeautifulSoup(html, 'html.parser')
        playBtn = soup.find_all(attrs={'class': "playBtn"})

        for i in range(len(playBtn)):
            platform = playBtn[i].attrs['data-cn']
            target_platform = '爱奇艺视频'
            if platform == target_platform:
                aqy_url = playBtn[i].attrs['href']
                play_url = re.findall(r'url=.*\.html', urllib.parse.unquote(aqy_url))[0].split('=')[1]
                data['播放地址'] = play_url
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
                movie_data = {'排名': '', '电影': '', '上映时间': '', '国家': '', '简介': '', '播放地址': '', }

                self.movie_name = details[i].img.attrs['alt']
                self.movie_details = details[i].a.attrs['href']
                movie_rankings = details[i].em.text
                release_time = re.findall(r'\d{4}', movie_information[i].text)[0]
                film_origin = re.findall(r'/\xa0.*\xa0/', movie_information[i].text)[0][2:-2]
                movie_synopsi = inq[i].text

                movie_resources = re.findall(r'\[.*\]', item[i].text)
                if movie_resources:
                    self.getLinkExtraction(movie_data)

                movie_data['排名'] = movie_rankings
                movie_data['电影'] = self.movie_name
                movie_data['上映时间'] = release_time
                movie_data['国家'] = film_origin
                movie_data['简介'] = movie_synopsi

                self.movie_list.append(movie_data)

            next = soup.find_all('link', attrs={'rel': "next"})
            if not next:
                self.enable = False

            self.page += 25
            print(self.page)
        except Exception:
            self.logger.exception("Download Page {numeral} Code failed".format(numeral=self.movie_name))

    def start(self):
        try:
            workbook = xlsxwriter.Workbook('/Users/wangjiacan/Desktop/shawn/爬取资料/duoban_movie.xlsx')
            worksheet = workbook.add_worksheet()

            dbdy_list = ['排名', '国家', '上映时间', '电影', '简介', '播放地址', ]
            col = 0

            worksheet.set_column('B:B', 15)
            worksheet.set_column('D:D', 20)
            worksheet.set_column('E:E', 50)
            worksheet.set_column('F:F', 50)

            worksheet.write('A1', dbdy_list[0])
            worksheet.write('B1', dbdy_list[1])
            worksheet.write('C1', dbdy_list[2])
            worksheet.write('D1', dbdy_list[3])
            worksheet.write('E1', dbdy_list[4])
            worksheet.write('F1', dbdy_list[5])

            while self.enable:
                self.dbdy_url = 'https://movie.douban.com/top250?start=' + str(self.page) + '&filter='
                self.getContentExtraction()

                for movie in self.movie_list:
                    for i in dbdy_list:
                        worksheet.write(self.row, col, movie[i])
                        col += 1
                    col = 0
                    self.row += 1

                self.movie_list.clear()

            workbook.close()
        except Exception:
            self.logger.exception("Writing data {name} failed".format(name=self.movie_name))


spider = DBDY()
spider.start()
