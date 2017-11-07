#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import re
import logging
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable
import time


def getHTMLCookies(url):
    """
    下载目标网页源码
    """
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    proxies = {
        "http": "http://36.111.205.166:80",
        "https": "http://36.111.205.166:80"
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    try:
        r = requests.get(url, proxies=proxies, headers=headers, verify=False, timeout=20)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.cookies
    except Exception:
        logger.exception("Download HTML Text failed")


def getHTMLText(url, cookies):
    """
    下载目标网页源码
    """
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    proxies = {
        "http": "http://36.111.205.166:80",
        "https": "http://36.111.205.166:80"
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    try:
        r = requests.get(url, proxies=proxies, headers=headers, cookies=cookies, verify=False, timeout=20)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except Exception:
        logger.exception("Download HTML Text failed")


def getStations():
    """
    下载所有站名与站名代码
    """
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    st_dict = {}
    stations_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8971'

    html = requests.get(stations_url, verify=False)
    html.raise_for_status()
    stations_list = re.findall(r'[\u4e00-\u9fa5]+\|[A-Z]+', html.text)

    for stations in stations_list:
        area = str(stations).split('|')
        stations_name = area[0]
        stations_code = area[1]
        st_dict[stations_name] = stations_code

    return st_dict


def getTrips(departure_time, from_station, to_station, site_name):

    trips_url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={time}&leftTicketDTO.from_station' \
                '={from_station}&leftTicketDTO.to_station={to_station}&purpose_codes=ADULT'.format(time=departure_time, from_station=from_station, to_station=to_station)

    cookies_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
    tickets_cookies = getHTMLCookies(cookies_url)
    html = getHTMLText(trips_url, tickets_cookies)
    # print(html)

    return_josn = json.loads(str(html))
    trips_information = return_josn['data']['result']
    trips_list = []
    table = PrettyTable(["车次", "初始站", "时间", "历时", "商务座", "一等座", "二等座", "高级软卧", "软卧", "动卧", "硬卧", "软座",
                         "硬座", "无座", "其他"])

    for i in trips_information:
        data_text = {'车次': '', '初始站': '', '时间': '', '历时': '', '商务座': '', '一等座': '', '二等座': '', '高级软卧': '',
                     '软卧': '', '动卧': '', '硬卧': '', '软座': '', '硬座': '', '无座': '', '其他': '', }
        seat_information = i.split('|')
        lnitial_station = site_name
        # 车次
        trips = seat_information[3]
        # 起始时间
        departure_time = seat_information[8]
        Time_of_arrival = seat_information[9]
        train_time = ("%s-%s" % (departure_time, Time_of_arrival))
        # 历时
        lasted = seat_information[10]
        # 高级软卧
        advanced_soft_sleeper = seat_information[21]
        # 其他
        other = seat_information[22]
        # 软卧
        soft_sleeper = seat_information[23]
        # 软座
        soft_seat = seat_information[24]
        # 无座
        no_seat = seat_information[26]
        # 硬卧
        hard_sleeper = seat_information[28]
        # 硬座
        herd_seat = seat_information[29]
        # 二等座
        second_class = seat_information[30]
        # 一等座
        first_class_seat = seat_information[31]
        # 商务座
        normal_seat = seat_information[32]
        # 动卧
        lying_down = seat_information[33]

        data_text['车次'] = trips
        data_text['初始站'] = lnitial_station
        data_text['时间'] = train_time
        data_text['历时'] = lasted
        data_text['商务座'] = normal_seat
        data_text['一等座'] = first_class_seat
        data_text['二等座'] = second_class
        data_text['高级软卧'] = advanced_soft_sleeper
        data_text['软卧'] = soft_sleeper
        data_text['动卧'] = lying_down
        data_text['硬卧'] = hard_sleeper
        data_text['软座'] = soft_seat
        data_text['硬座'] = herd_seat
        data_text['无座'] = no_seat
        data_text['其他'] = other

        trips_list.append(data_text)

    for x in range(len(trips_list)):
        for y in trips_list[x]:
            if not trips_list[x][y]:
                trips_list[x][y] = '--'

    for b in range(len(trips_list)):
        table.add_row([trips_list[b]['车次'], trips_list[b]['初始站'], trips_list[b]['时间'], trips_list[b]['历时'],
                       trips_list[b]['商务座'], trips_list[b]['一等座'], trips_list[b]['二等座'], trips_list[b]['高级软卧'],
                       trips_list[b]['软卧'], trips_list[b]['动卧'], trips_list[b]['硬卧'], trips_list[b]['软座'],
                       trips_list[b]['硬座'], trips_list[b]['无座'], trips_list[b]['其他'], ])
    print(table)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='/Users/wangjiacan/Desktop/代码/log/tickets.txt',
                        filemode='a')

    logger = logging.getLogger()

    stations_dict = getStations()

    setoff_time = input("请输入出发时间（如：2017-11-30）：")
    departure, destination = input("请输入出发地与目的地（如：杭州 荆州）：").split()
    departure_code = stations_dict[departure]
    destination_code = stations_dict[destination]
    site_name = ("%s-%s" % (departure, destination))

    getTrips(setoff_time, departure_code, destination_code, site_name)
