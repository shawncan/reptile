#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import pymysql
import logging
import datetime


def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        print("爬取失败")


def getStockList(lst, stockURL):
    html = getHTMLText(stockURL, "GB2312")
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


def mysql(crawl_time, stock_name, stock_price, price_change, highest, lowest, volume, turnover_rate, quote_change):
    db = pymysql.connect(host="127.0.0.1", user="root", password="shawn@0216", db="wjc_user", charset='utf8')
    cursor = db.cursor()

    sql = """
                INSERT INTO StockTracking(crawl_time, stock_name, stock_price, price_change, 
                highest, lowest, volume, turnover_rate, quote_change) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/BaiduStockTracking.txt',
                        filemode='a')

    logger = logging.getLogger()

    try:
        cursor.execute(sql, (crawl_time, stock_name, stock_price, price_change, highest, lowest, volume, turnover_rate,
                             quote_change))
        db.commit()
    except:
        logger.exception("Crawling Baidu {} stock data failed".format(stock_name))
        db.rollback()

    db.close()



def getStockTracking(lst, stockURL):
    count = 0
    success_count = 0
    failure_count = 0
    crawl_time = datetime.datetime.now().strftime("%Y/%m/%d")

    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/BaiduStockTracking.txt',
                        filemode='a')

    logger = logging.getLogger()


    for stock in lst:
        url = stockURL + stock + '.html'
        html = getHTMLText(url)

        try:
            if html == "":
                continue

            soup = BeautifulSoup(html, 'html.parser')

            stockInfo = soup.find(attrs={'class': 'bets-content'})
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')

            if keyList:
                volume = 0
                highest = 0
                turnover_rate = 0
                lowest = 0

                for i in range(len(keyList)):
                    key = keyList[i].text.split()[0]
                    val = valueList[i].text.split()[0]
                    if key == '成交量':
                        volume = val
                    elif key == '最高':
                        highest = val
                    elif key == '换手率':
                        turnover_rate = val
                    elif key == '最低':
                        lowest = val
                    else:
                        continue

                name = soup.find_all(attrs={'class': 'bets-name'})[0]
                stock_name = name.text.split()[0]

                if soup.find_all(attrs={'class': 'price s-up '}):
                    price_1 = soup.find_all(attrs={'class': 'price s-up '})[0]
                    price_s_down = price_1.text.split()
                    stock_price = price_s_down[0]
                    price_change = price_s_down[1]
                    quote_change = price_s_down[2]
                elif soup.find_all(attrs={'class': 'price s-down '}):
                    price_2 = soup.find_all(attrs={'class': 'price s-down '})[0]
                    price_s_down = price_2.text.split()
                    stock_price = price_s_down[0]
                    price_change = price_s_down[1]
                    quote_change = price_s_down[2]
                else:
                    price_3 = soup.find_all(attrs={'class': 'price s-stop '})[0]
                    price_s_down = price_3.text.split()
                    stock_price = price_s_down[0]
                    price_change = price_s_down[1]
                    quote_change = price_s_down[2]

                mysql(crawl_time, stock_name, stock_price, price_change, highest, lowest, volume, turnover_rate,
                      quote_change)

                count = count + 1
                print("\r当前进度:{:.2f}%".format(count * 100 / len(lst), end=""))
                success_count = success_count + 1

            else:
                count = count + 1
                print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
                failure_count = failure_count + 1
                continue

        except Exception:
            count = count + 1
            print("\r当前进度: {:.2f}%".format(count * 100 / len(lst)), end="")
            failure_count = failure_count + 1
            logger.exception("Crawling Baidu {} stock data failed".format(stock))
            continue

    print("数据爬取成功：爬取成功{}条数据，爬取失败{}条数据".format(success_count, failure_count))


def main():
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = "https://gupiao.baidu.com/stock/"
    slist = []

    start = datetime.datetime.now()
    getStockList(slist, stock_list_url)
    print("股票列表已爬取成功共{}条数据".format(len(slist)))

    getStockTracking(slist, stock_info_url)

    end = datetime.datetime.now()
    print(end - start)


if __name__ == "__main__":
    main()
