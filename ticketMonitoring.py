#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import logging
import openpyxl
import os
import json
import excelOperating
import datetime
import time
import configparser


def getHTMLText(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:57.0) Gecko/20100101 Firefox/57.0',
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("爬取失败")


def getCityCode():
    filePath = '/Users/wangjiacan/Desktop/shawn/爬取资料/cityCode.xlsx'
    tableName = 'fliggy'
    columnCount = [0, 1]
    excelType = ["A", 'B']
    cityCodeInfo = excelOperating.readExcel(filePath, tableName, columnCount, excelType)
    code = []

    city = "杭州"

    for cityCode in cityCodeInfo:
        if city in cityCode.values():
            code.append(cityCode['A'])
        else:
            continue

    return code


def getDepartureTicket():
    airTicketsList = []

    cityCode = getCityCode()
    routes = cityCode[0]

    currentTime = time.time()
    startDate = time.strftime("%Y-%m-%d", time.localtime())
    endDate = time.strftime("%Y-%m-%d", time.localtime(float(currentTime + 3888000)))


    departureTicketUrl = 'https://sjipiao.fliggy.com/search/cheapFlight.htm?startDate={startDate}&endDate={endDate}&' \
                         'routes={routes}-&_ksTS=1514440974905_1979&callback=jsonp1980&ruleId=99&flag=1'.format(
        startDate=startDate, endDate=endDate, routes=routes)

    airTicketsInfo = getHTMLText(departureTicketUrl)

    host = re.findall(r'"HOST":".*","status"', airTicketsInfo)
    hostLength = len(host[0][8:-10])

    lnterceptionLength = 21 + hostLength + 22
    airTickets = airTicketsInfo.strip()[lnterceptionLength:-2]

    airTicketsData = json.loads(airTickets)

    flights = airTicketsData['flights']

    for info in flights:
        infoData = {'目的地':'', '机票价格':'', '出发日期':'', '折扣':''}

        infoData['目的地'] = info['arrName']
        infoData['机票价格'] = info['price']
        infoData['出发日期'] = info['depDate']
        infoData['折扣'] = info['discount']

        airTicketsList.append(infoData)

    return airTicketsList


def start():
    conf = configparser.ConfigParser()
    conf.read("/Users/wangjiacan/Desktop/代码/Profile/localConfiguration.ini")

    file_location = conf.get("ticketMonitoring", "file_location")
    table_name = conf.get("ticketMonitoring", "table_name")
    airTicketsList = getDepartureTicket()

    excelOperating.writeExcel(file_location, airTicketsList, table_name)
    # a = excelOperating.dataProcessing(file_location, airTicketsList, table_name)
    # print(a)


if __name__ == '__main__':
    start()