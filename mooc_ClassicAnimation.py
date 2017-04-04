#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import bs4
import os


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


def fillAnimationList(alist, html):
    soup = BeautifulSoup(html, 'html.parser')
    a_list = []
    for tr in soup.find(id="endText").children:
        if isinstance(tr, bs4.element.Tag):
            ts = tr.find('img')
            a = tr.string
            if len(a_list) == 2:
                alist.append([a_list[0], a_list[1]])
                a_list.clear()
            if tr.string is not None and ('jpg' in a or 'png' in a or 'JPG' in a):
                a_list.append(a)
            elif isinstance(ts, bs4.element.Tag):
                b = ts.attrs['src']
                a_list.append(b)
            else:
                continue

                # '''通过把搜索然后再搜索把结果转成列表也能达到效果'''
                # p_list = list(soup.find(id="endText").find_all('p'))
                # for p in p_list[1:171]:
                #     text = p.get_text()
                #     img = p.find("img")
                #     if img:
                #         print(img.get('src'))
                #     if text:
                #         print(text)


def downloadImage(ulist):
    root = "/Users/wangjiacan/Desktop/shawn/爬取资料/"
    for i in range(len(ulist)):
        u = ulist[i]
        address = root + u[1]
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(address):
                r = requests.get(u[0], timeout=30)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
                with open(address, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print("文件保存成功")
                    print(i)
            else:
                print("文件已存在")
        except:
            print("爬取失败")


def main():
    anim = []
    targer = 'http://digi.163.com/14/1115/06/AB2PQ0CC001664LU.html'
    html = getHTMLText(targer)
    fillAnimationList(anim, html)
    downloadImage(anim)


if __name__ == '__main__':
    main()
