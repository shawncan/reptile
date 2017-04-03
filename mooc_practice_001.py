#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import bs4


def getHTMLTexe(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


if __name__ == "__main__":
    # targer = "http://python123.io/ws/demo.html"
    targer = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2017.html'
    demo = getHTMLTexe(targer)
    soup = BeautifulSoup(demo, 'html.parser')
    # print(soup(string='Advanced Python'))
    print("{:^10}\t{:^6}\t{:^10}".format("排名", "学校名称", "总分"))


    # '''遍历该标签下面子标签'''
    # for child in soup.body.children:
    #     if child.name is not None:
    #         print(child.name)

    # '''遍历该标签下面的子孙标签'''
    # for child in soup.body.descendants:
    #     if child.name is not None:
    #         print(child.name)

    # '''遍历该标签的所有先辈节点标签'''
    # for parent in soup.a.parents:
    #     print(parent.name)

    # '''遍历后续节点标签'''
    # for sibling in soup.a.next_siblings:
    #     if sibling.name is not None:
    #         print(sibling.name)

    # '''遍历前续节点标签'''
    # for sibling in soup.p.previous_siblings:
    #     if sibling.name is not None:
    #         print(sibling.name)

    # '''树桩结构HTML代码'''
    # print(soup.prettify())

    # '''树桩结构遍历整个HTML标签'''
    # for tag in soup.find_all(True):
    #     print(tag.name)

    # '''查找某个标签并遍历该标签下面子标签'''
    # for child in soup.find('tbody').children:
    #     if child.name is not None:
    #         ts = child('td')[0].contents
    #         print(ts[0].string, ts[1].string, ts[2].string, ts[3].string)
    #     # if isinstance(child, bs4.element.Tag):
    #     #     ts = child('td')
    #     #     print(ts[0].string, ts[1].string, ts[2].string, ts[3].string)

