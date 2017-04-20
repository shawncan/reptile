#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import traceback


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


def getStockList(lst, stockURL):
    html = getHTMLText(stockURL)
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']
            match = re.findall(r'[s][hz]\d{6}', href)
            if match:
                lst.append(match[0])
            else:
                continue
        except:
            continue


def getStockInfo(lst, stockURL):
    for stock in lst:
        url = stockURL + stock + '.html'
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')

            name = soup.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})

            stockInfo = soup.find(attrs={'class': 'bets-content'})
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text.split()[0]
                val = valueList[i].text.split()[0]
                infoDict[key] = val

            print(infoDict)



        except:
            print('')


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = "https://gupiao.baidu.com/stock/"
    output_file = '/Users/wangjiacan/Desktop/shawn/爬取资料/股票信息/'
    slist = []
    slist_1 = ['sz002415']
    # getStockList(slist, stock_list_url)
    getStockInfo(slist_1, stock_info_url)


if __name__ == "__main__":
    main()
