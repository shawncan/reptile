#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

url = 'https://movie.douban.com/top250?start=0&filter='

douban = requests.get(url)
html = douban.text

soup = BeautifulSoup(html, 'html.parser')

ol = soup.find('ol')
li = ol.find_all('p', attrs={'class': ""})
a = li[0].text
print(re.findall(r'\d{4}', a)[0])
print(re.findall(r'/\xa0.*\xa0/', a)[0][2:-2])

title = ol.find_all('img', attrs={'class': ""})
print(title[0].attrs['alt'])

playable = ol.find_all('span', attrs={'class': "playable"})
print(playable[0].text)

inq = ol.find_all('span', attrs={'class': "inq"})
print(inq[0].text)

details = ol.find_all('div', attrs={'class': "pic"})
print(details[0].em.text)
print(details[0].a.attrs['href'])
print(details[0].img.attrs['alt'])
