#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
import re
import json
import time
import mysqlOperating
import configparser
import hashlib


class fliggyTicketMonitoring(object):
    #===========================================================================
    # '''阿里飞猪特价机票监控
    # @generateSignature: 生成阿里api调用签名
    #
    # '''
    #===========================================================================
    def __init__(self):
        # 阿里api调用参数定义
        # method: API接口名称, app_key: 应用AppKey, timestamp: 时间戳, format: 响应格式, v: API协议版本, sign_method : 签名的摘要算法, sign: API签名， secret: 应用Secret
        # dep_city_code: 出发城市, arr_city_code: 到达城市, dep_date: 航班日期, search_type: 搜索类型
        conf = configparser.ConfigParser()
        conf.read("/Users/wangjiacan/Desktop/sourceCode/configurationFile/localConfiguration.ini")

        self.method = conf.get("fliggyTicketMonitoring", "method")
        self.app_key = conf.get("fliggyTicketMonitoring", "app_key")
        self.timestamp = ''
        self.format = 'json'
        self.v = '2.0'
        self.sign_method = 'md5'
        self.sign = ''
        self.secret = conf.get("fliggyTicketMonitoring", "secret")
        self.dep_city_code = 'HGH'
        self.arr_city_code = 'KMG'
        self.depDate = '2018-03-10'
        self.search_type = 'outbound'

        self.ticketSearchUrl = 'https://sjipiao.fliggy.com/searchow/search.htm?depCity={depCity}&depCityName={depCityName}&' \
                               'arrCity={arrCity}&arrCityName={arrCityName}&depDate={depDate}&searchSource=99'

        self.my = mysqlOperating.MYSQL()


    def getHTMLText(self, url):
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


    def getCityCode(self, city):
        # 查询城市代码sql语句
        inquire_sql = """
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

    def getTicketPrice(self):
       # 查询是否有新增监控sql语句
        addMonitoringInquire = """
        select id, departure_city, arrival_city from ticket_monitoring_information WHERE added = "0" 
        """

        searchResult = self.my.queryOperation(addMonitoringInquire)

        if searchResult:
           for city in searchResult:
               id = city[0]
               print(id)
               depCityName = city[1]
               arrCityName = city[2]

               depCity = self.getCityCode(depCityName)
               arrCity = self.getCityCode(arrCityName)

               ticketPriceInfo = self.getHTMLText(self.ticketSearchUrl.format(depCity=depCity, depCityName=depCityName, arrCity=arrCity, arrCityName=arrCityName, depDate=self.depDate))
               ticketPrice = re.findall(r'"basicCabinPrice":\d*', ticketPriceInfo)[0][18:]
               print(ticketPrice)


        print("@")




    def start(self):
        self.getTicketPrice()

if __name__ == '__main__':
    run = fliggyTicketMonitoring()
    run.start()