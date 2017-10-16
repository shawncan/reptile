#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import queue


def getProxy(file_name):
    """
    下载代理的ip
    """
    file_path = '/Users/wangjiacan/Desktop/shawn/爬取资料/ip/' + file_name + '.txt'

    file = open(file_path, 'r')
    lines = file.readlines()

    for proxy_ip in lines:
        url_queue.put(proxy_ip[:-1])


def verification():
    """
    检测代理的ip是否可用
    """
    success_count = 0
    failure_count = 0
    path = '/Users/wangjiacan/Desktop/shawn/爬取资料/ip/proxy_ip.txt'

    url = 'https://httpbin.org/get?show_env=1'

    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36'}

    for i in range(url_queue.qsize()):
        ip = url_queue.get()
        try:
            proxies = {
                "http": "http://" + ip,
                "https": "http://" + ip
                }
            r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            r.raise_for_status()

            with open(path, 'a') as f:
                f.write(ip + "\n")
                f.close()
            success_count += 1
            print(ip + "提取成功")
        except Exception:
            failure_count += 1
            print(ip + "无效")

    print("代理ip成功：爬取成功{}条数据，爬取失败{}条数据".format(success_count, failure_count))


if __name__ == '__main__':
    url_queue = queue.Queue()
    print("代理ip提取开始...")
    name_list = ['ip_20171016']
    for i in range(len(name_list)):
        getProxy(name_list[i])
    print("代理ip文件读取完成，开始检测ip可用性")
    verification()
    print("代理ip提取结束...")
