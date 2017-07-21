#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/top250?start=0&filter='

douban = requests.get(url)
html = douban.text

soup = BeautifulSoup(html, 'html.parser')

ol = soup.find('ol')
li = ol.find_all('p', attrs={'class': ""})
print(li[1].text)

