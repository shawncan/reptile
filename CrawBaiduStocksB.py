#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import traceback
import os
import time


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


def getStockInfo(lst, stockURL, path, name):
    output_file = path + name
    count = 0

    for stock in lst:
        url = stockURL + stock + '.html'
        html = getHTMLText(url)

        if not os.path.exists(path):
            os.mkdir(path)

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

            with open(output_file, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                count = count + 1
                print("\r当前进度:{:.2f}%".format(count*100/len(lst), end=""))

        except:
            # traceback.print_exc()
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            continue

    print('文件保存成功')


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = "https://gupiao.baidu.com/stock/"
    file_path = '/Users/wangjiacan/Desktop/shawn/爬取资料/股票信息/'
    file_name = 'BaiduStockInfo.txt'
    slist = []
    slist_1 = ['sz300059',  'sz002415', 'sh166105', 'sh201005']
    # getStockList(slist, stock_list_url)
    # print(slist)
    start = time.time()
    getStockInfo(slist_1, stock_info_url, file_path, file_name)
    end = time.time()
    time_consuming = time.strftime("%M:%S", time.localtime(end - start))
    print(time_consuming)


if __name__ == "__main__":
    main()
