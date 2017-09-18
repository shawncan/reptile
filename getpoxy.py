#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import time
import queue


def getProxy():
    """
    下载代理的ip
    """
    api_url = 'http://proxy.mimvp.com/api/fetch.php?orderid=860170913191809460&num=200&http_type=1,2&ping_time=0.3&result_fields=1,2&result_format=json'
    result = requests.get(api_url)
    proxy_json = result.json()
    proxy = proxy_json['result']

    for proxy_ip in proxy:
        url_queue.put(proxy_ip['ip:port'])
        print("!")


def verification():
    try:
        run_time = time.strftime("%Y%m%d", time.localtime())
        path = '/Users/wangjiacan/Desktop/shawn/爬取资料/ip/ip_' + run_time + '.txt'

        url = 'https://httpbin.org/get?show_env=1'

        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36'}

        for i in range(url_queue.qsize()):
            ip = url_queue.get()
            proxies = {
                "http": "http://" + ip,
                "https": "http://" + ip
                }
            r = requests.get(url, headers=headers, proxies=proxies, timeout=20)
            r.raise_for_status()

            with open(path, 'a') as f:
                f.write(ip + "\n")
                f.close()
            print(ip + "提取成功")
    except Exception:
        print("链接出错")


url_queue = queue.Queue()

getProxy()
print(url_queue.get())
