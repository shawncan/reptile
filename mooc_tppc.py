#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-
import requests
import os


def getHTMLImage(url, name):
    root = "/Users/wangjiacan/Desktop/shawn/爬取资料/"
    address = root + name
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(address):
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            with open(address, 'wb') as f:
                f.write(r.content)
                f.close()
                print("文件保存成功")
        else:
            print("文件已存在")
    except:
        print("爬取失败")


if __name__ == "__main__":
    goal = input("请输入爬取地址：")
    name = input("请输入文件名：")
    getHTMLImage(goal, name)
