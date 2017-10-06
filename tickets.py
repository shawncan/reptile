#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import re
import logging
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def getHTMLText(url):
    """
    下载目标网页源码
    """
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    try:
        r = requests.get(url, verify=False)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception:
        logger.exception("Download HTML Text failed")


def getStations():
    """
    下载所有站名与站名代码
    """
    st_dict = {}
    stations_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'

    html = getHTMLText(stations_url)
    stations_list = re.findall(r'[\u4e00-\u9fa5]+\|[A-Z]+', html)

    for stations in stations_list:
        area = str(stations).split('|')
        stations_name = area[0]
        stations_code = area[1]
        st_dict[stations_name] = stations_code

    return st_dict


def getTrips(time, from_station, to_station):

    trips_url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={time}&leftTicketDTO.from_station' \
                '={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'.format(time=time, from_station=from_station, to_station=to_station)

    html = getHTMLText(trips_url)
    print(html)
    j = json.loads(str(html))
    a = j['data']['result'][4]
    print(a.split('|'))


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/tickets.txt',
                        filemode='a')

    logger = logging.getLogger()

    # stations_dict = getStations()

    getTrips('2017-10-15', 'VRH', 'HZH')

