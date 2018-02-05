#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import re
import json
import time
import mysqlOperating

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


def getCityCode(city):
    # 查询城市代码sql语句
    inquire_sql ="""
    SELECT city_code FROM city_code WHERE city = "{city}"
    """

    # 使用mysqlOperating类
    my = mysqlOperating.MYSQL()

    # 执行sql语句查询
    searchResult = my.queryOperation(inquire_sql.format(city=city))

    # 获得城市代码
    code = searchResult[0][0]

    # 返回城市代码
    return code


def writeDatabase(airTicketsList):
    # 写入sql语句
    write_sql = """
    INSERT INTO cheap_flights(departure_date, departure_city, arrival_city, price, discount, sold_out) 
    VALUES ("{departure_date}", "{departure_city}", "{arrival_city}", "{price}", "{discount}", "{sold_out}")
    """
    # 查询sql语句
    inquire_sql ="""
    select * from cheap_flights WHERE departure_date = "{departure_date}" and departure_city = "{departure_city}"
    """
    success_count = 0
    failure_count = 0

    my = mysqlOperating.MYSQL()

    for infoData in airTicketsList:
        departure_date = infoData['出发日期']
        departure_city = infoData['出发城市']
        arrival_city = infoData['到达城市']
        price = infoData['机票价格']
        discount = infoData['折扣']
        sold_out = 0

        searchResult = my.queryOperation(inquire_sql.format(departure_date=departure_date, departure_city=departure_city))

        if not searchResult:
            writeState = my.executeOperation(write_sql.format(departure_date=departure_date, departure_city=departure_city,
                                                              arrival_city=arrival_city, price=price, discount=discount, sold_out=sold_out))
            if writeState == 0:
                success_count += 1
            else:
                failure_count += 1
        else:
            continue

    print("此次数据爬取：数据库插入成功{}条数据，数据库插入失败{}条数据".format(success_count, failure_count))


def getCheapFlights():
    # airTicketsList 特价机票信息列表
    airTicketsList = []

    # 获取目标城市代码
    # target_city 目标城市, cityCode 目标城市代码
    target_city = "杭州"
    city_code = getCityCode(target_city)

    # 获取查询开始时间与结束时间
    # startDate 开始时间, endDate结束时间(45天后)
    currentTime = time.time()
    startDate = time.strftime("%Y-%m-%d", time.localtime())
    endDate = time.strftime("%Y-%m-%d", time.localtime(float(currentTime + 3888000)))

    for num in range(2):
        # 设置城市代码属性
        # 无 为出发, - 为返程
        if num == 1 :
            city_code = "-" + city_code

        CheapFlightsUrl = 'https://sjipiao.fliggy.com/search/cheapFlight.htm?startDate={startDate}&endDate={endDate}&' \
                          'routes={routes}&ruleId=99'.format(startDate=startDate, endDate=endDate, routes=city_code)

        airTicketsInfo = getHTMLText(CheapFlightsUrl)

        # 处理url返回内容
        # hostLength "HOST"参数的内容长度, lnterceptionLength "data"属性前字符数包含"data":
        # airTicketsData 处理后内容字典
        host = re.findall(r'"HOST":".*","status"', airTicketsInfo)
        hostLength = len(host[0][8:-10])
        lnterceptionLength = 12 + hostLength + 22
        airTickets = airTicketsInfo.strip()[lnterceptionLength:-2]
        airTicketsData = json.loads(airTickets)

        # 提取信息
        # depDate 出发日期, depName 出发城市, arrName 到达城市, price 机票价格, discount 折扣
        flights = airTicketsData['flights']
        for info in flights:
            infoData = {'出发日期': '', '出发城市':'', '到达城市': '', '机票价格': '',  '折扣': ''}

            infoData['出发日期'] = info['depDate']
            infoData['出发城市'] = info['depName']
            infoData['到达城市'] = info['arrName']
            infoData['机票价格'] = info['price']
            infoData['折扣'] = info['discount']

            airTicketsList.append(infoData)

    return airTicketsList

def start():
    airTicketsList = getCheapFlights()
    writeDatabase(airTicketsList)


if __name__ == '__main__':
    start()