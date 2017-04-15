#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import re


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


def parsePage(ilt, html):
    try:
        plt = re.findall(r'"view_price":"[\d.]*"', html)
        tlt = re.findall(r'"raw_title":".*?"', html)
        sel = re.findall(r'"view_sales":".*?"', html)
        add = re.findall(r'"nid":"[\d.]*"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            seles = eval(sel[i].split(':')[1])
            address = eval(add[i].split(':')[1])
            ilt.append([price, title, seles, address])
    except:
        print("提取失败")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}\t{:24}"
    print(tplt.format("序号", "价格", "已销售", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[2], g[1]))


def printGoodsLink(ilt, num):
    commodity = ilt[num - 1]
    nid = commodity[3]
    url = 'https://detail.tmall.com/item.htm?id=' + nid
    print("您感兴趣的商品链接：" + url)


def main():
    goods = '书包'
    depth = 1
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)
    print('\n')
    num = input("请输入您感兴趣的商品序号：")
    printGoodsLink(infoList, int(num))


if __name__ == "__main__":
    main()
