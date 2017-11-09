#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import re
import logging
from bs4 import BeautifulSoup


def getHTMLText(url):
    """
    下载目标网页源码
    """
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    try:

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception:
        logger.exception("Download HTML Text failed")


def extractIp():
    proxy_list = []
    xicidaili_url = "http://www.xicidaili.com/nn/"
    html = getHTMLText(xicidaili_url)
    soup = BeautifulSoup(html, 'html.parser')
    tbody = soup.find('table')
    tr = tbody.find_all('tr')

    for info_fast in tr[1:]:
        proxy_data = {'ip': '', '端口': '', '类型': '', '存活时间': '', '验证时间': '', }

        judgment_info = re.findall(r'<div class="bar" .*>', str(info_fast))
        # 速度
        speed = judgment_info[0].split('"')[3][:-1]
        # 连接时间
        connect_time = judgment_info[1].split('"')[3][:-1]

        if float(speed) > 3:
            continue
        if float(connect_time) > 1:
            continue

        extrac_info = re.findall(r'<td>.*</td>', str(info_fast))
        # ip地址
        ip = extrac_info[0][4:-5]
        # 端口
        port = extrac_info[1][4:-5]
        # 类型
        type = extrac_info[2][4:-5]
        # 存活时间
        survival_time = extrac_info[3][4:-5]
        # 验证时间
        verification_time = extrac_info[4][4:-5]

        proxy_data['ip'] = ip
        proxy_data['端口'] = port
        proxy_data['类型'] = type
        proxy_data['存活时间'] = survival_time
        proxy_data['验证时间'] = verification_time

        proxy_list.append(proxy_data)
    print(len(proxy_list))
    print(proxy_list[1])
    print(proxy_list)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/xicidaili_proxy.txt',
                        filemode='a')

    logger = logging.getLogger()
    extractIp()