#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import os


def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print('爬取失败')


def getImageDownload():
    pass


def getGoddessList(dict, GoddessURL):
    html = getHTMLText(GoddessURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a', attrs={'target': '_blank'})
    for i in a:
        try:
            href = i.attrs['href']
            font = i.find('font')
            if font is not None:
                name = font.string
                dict[name] = href
            else:
                continue
        except:
            print('')


def getGalleryList():
    pass


def getGalleryDetails(dict, GoddessURL):
    path = '/Users/wangjiacan/Desktop/shawn/爬取资料/宅男女神/'

    for (i, m) in dict.items():
        url = GoddessURL + m
        html = getHTMLText(url)
        soup = BeautifulSoup(html, 'html.parser')

        file_path = path + i
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        try:
            li = soup.find('a', attrs={'title': '全部图片'}).text.split()[0]
            s = re.findall(r'\d', li)
            if s[0] > '6':
                print('1')
            else:
                gallery_link = soup.find_all('a', attrs={'class': 'igalleryli_link'})
                for l in gallery_link:
                    link = l.attrs['href']
                    Goddess_url = GoddessURL + link
                    getGalleryImage(file_path, Goddess_url)

        except:
            pass


def getGalleryImage(file_path, PortraitURL):
    html = getHTMLText(PortraitURL)
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('ul', attrs={'id': 'hgallery'})
    a = img.find_all('img')
    for v in a:
        x = v.attrs['src']
        print(x)





def main():
    goddess_list_url = 'https://www.nvshens.com/rank/sum/'
    goddess_detail_url = 'https://www.nvshens.com'
    gdict = {}
    gdict_1 = {'木木hanna': '/girl/21954/'}

    # getGoddessList(gdict, goddess_list_url)
    getGalleryDetails(gdict_1, goddess_detail_url)



if __name__ == "__main__":
    main()
