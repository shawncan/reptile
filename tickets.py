#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import re
import logging
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable
import time


def getHTMLText(url):
    """
    下载目标网页源码
    """
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    proxies = {
        "http": "http://124.232.148.7:3128",
        "https": "http://124.232.148.7:3128"
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    try:
        r = requests.get(url, proxies=proxies, headers=headers, verify=False, timeout=20)
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


def getTrips(departure_time, from_station, to_station):

    trips_url = 'https://kyfw.12306.cn/otn/leftTicket/queryX?leftTicketDTO.train_date={time}&leftTicketDTO.from_station' \
                '={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'.format(time=departure_time, from_station=from_station, to_station=to_station)

    html = getHTMLText(trips_url)

    link_switch = True
    while link_switch:
        if html is None:
            print("1")
            time.sleep(10)
            continue
        print(html)
        j = json.loads(str(html))
        a = j['data']['result'][6]
        # print(a)
        seat_information = a.split('|')
        trips = seat_information[3]
        advanced_soft_sleeper = seat_information[21]
        other = seat_information[22]
        soft_sleeper = seat_information[23]
        soft_seat = seat_information[24]
        no_seat = seat_information[26]
        hard_sleeper = seat_information[28]
        herd_seat = seat_information[29]
        second_class = seat_information[30]
        first_class_seat = seat_information[31]
        normal_seat = seat_information[32]
        lying_down = seat_information[33]
        link_switch = False
    # print("车次%s" % trips)
    # print("商务座：{normal_seat}， 一等座：{first_class_seat}， 二等座：{second_class}， 高级软卧:{advanced_soft_sleeper}， "
    #       "软卧：{soft_sleeper}， 动卧：{lying_down}， 硬卧：{hard_sleeper}， 软座：{soft_seat}， 硬座：{herd_seat}， 无座："
    #       "{no_seat}， 其他：{other}".format(normal_seat=normal_seat, first_class_seat=first_class_seat, second_class=second_class, advanced_soft_sleeper=advanced_soft_sleeper, soft_sleeper=soft_sleeper, lying_down=lying_down, hard_sleeper=hard_sleeper, soft_seat=soft_seat, herd_seat=herd_seat, no_seat=no_seat, other=other))

        table = PrettyTable(["车次", "商务座", "一等座", "二等座", "高级软卧", "软卧", "动卧", "硬卧", "软座", "硬座", "无座", "其他"])
        table.add_row([trips, normal_seat, first_class_seat, second_class, advanced_soft_sleeper, soft_sleeper, lying_down, hard_sleeper, soft_seat, herd_seat, no_seat, other])
        table.reversesort = True
        print(table)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/tickets.txt',
                        filemode='a')

    logger = logging.getLogger()

    # stations_dict = getStations()

    # getTrips('2017-10-18', 'HZH', 'BJP')
    header = "车次 车站 时间 历时 商务座 一等座 二等座 高级软卧 软卧 动卧 硬卧 软座 硬座 无座 其他".split()

    table = PrettyTable()
    table._set_field_names(header)
    table.add_row(["G1517", "黄山北-上海虹桥", "08:11-12:22", "04:11",  "4", "无", "有", "--", "--", "--", "--", "--", "--", "--", "--"])
    table.align["车次"] = "l"
    table.padding_width = 1
    table.reversesort = True
    print(table)
