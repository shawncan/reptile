#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup


def getHTMLTexe(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


if __name__ == "__main__":
    targer = "http://python123.io/ws/demo.html"
    demo = getHTMLTexe(targer)
    soup = BeautifulSoup(demo, 'html.parser')
    print(soup.prettify())


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
