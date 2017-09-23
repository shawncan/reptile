#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import time
import queue


def getProxy():
    """
    下载代理的ip
    """
    api_url = '请填写代理IP的提取链接，于IP提取网站上生成'
    result = requests.get(api_url)
    proxy_json = result.json()
    proxy = proxy_json['result']

    for proxy_ip in proxy:
        extract_ip = proxy_ip['ip:port']
        url_queue.put(extract_ip)


def verification():
    """
    检测代理的ip是否可用
    """
    success_count = 0
    failure_count = 0
    run_time = time.strftime("%Y%m%d", time.localtime())
    path = '/Users/wangjiacan/Desktop/shawn/爬取资料/ip/ip_' + run_time + '.txt'

    url = 'https://httpbin.org/get?show_env=1'

    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36'}

    for i in range(url_queue.qsize()):
        ip = url_queue.get()
        try:
            proxies = {
                "http": "http://" + ip,
                "https": "http://" + ip
                }
            r = requests.get(url, headers=headers, proxies=proxies, timeout=20)
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
    getProxy()
    print("代理ip下载完成，开始检测ip可用性")
    verification()
    print("代理ip提取结束...")
