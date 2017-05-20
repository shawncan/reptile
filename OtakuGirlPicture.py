#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def getHTMLText(url, code='utf-8'):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print('爬取失败')


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


def getPictorialList():
    pass


def getPictorialDownload(dict, GoddessURL):
    for (i, m) in dict.items():
        print(i,m)




def main():
    goddess_list_url = 'https://www.nvshens.com/rank/sum/'
    goddess_detail_url = 'https://www.nvshens.com'
    gdict = {}

    getGoddessList(gdict, goddess_list_url)
    getPictorialDownload(gdict, goddess_detail_url)



if __name__ == "__main__":
    main()
