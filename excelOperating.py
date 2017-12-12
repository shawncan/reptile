#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import logging
import openpyxl
import os
import json


class excelOperating(object):
    def __init__(self, fileLocation, title, tableName):
        self.columnList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O']
        self.newColumnList = []
        self.writeContentList = []
        self.fileLocation = fileLocation
        self.title = title
        self.tableName = tableName


    def dataProcessing(self):
        columnNum = len(self.title[0])
        rowsNum = len(self.title)
        self.newColumnList = self.columnList[0:columnNum]
        for num_1 in range(rowsNum):

            rows = num_1 + 1
            for num_2 in range(columnNum):
                writeContent = {'column': '', 'rows': '', 'content': '', }
                column = self.newColumnList[num_2]
                writeContent['column'] = column
                writeContent['rows'] = rows
                self.writeContentList.append(writeContent)

            # for key in self.title[num_1]:
            #     # print(self.writeContentList[num_1])
            #     content = self.title[num_1][key]
            #     # self.writeContentList[num_1]['content'] = content
            #     # print(content)


        # print(self.writeContentList)
        # for i in range(len(self.writeContentList)):
        #     print(self.writeContentList[i])
        aList = []
        for num in range(len(self.title)):
            for key in self.title[num]:
                content = self.title[num][key]
                aList.append(content)

        for i in range(len(self.writeContentList)):
            self.writeContentList[i]['content'] = aList[i]

        print(self.writeContentList)



    def writeExcel(self):
        test = [{'column': 'A', 'content': '用户名','rows':'1'}, {'column': 'B', 'content': '会员等级', 'rows':'1'}]

        if not os.path.exists(self.fileLocation):
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet.title = self.tableName
            for i in range(len(test)):
                column = test[i]['column']
                content = test[i]['content']
                rows = test[i]['rows']
                sheet["{column}{rows}".format(column=column, rows=rows)].value = content
            workbook.save(self.fileLocation)

        print("yep")




a = '/Users/wangjiacan/Desktop/shawn/爬取资料/test1.xlsx'
b = [{'ip': 'ip', '类型': '类型', '验证时间': '验证时间', },
     {'ip': '202.85.213.219:3128', '类型': 'HTTP/HTTPS', '验证时间': '2017-12-01 18:12:24', }, ]
c = '2332'
spider = excelOperating(a, b, c)
# spider.writeExcel()
spider.dataProcessing()
