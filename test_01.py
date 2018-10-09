#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import openpyxl
import os
import sys
import configparser
import pymysql
import re



def readExcel(fileAddress, tableName):
    """
    """

    readWorkbook = openpyxl.load_workbook(fileAddress)

    readSheet = readWorkbook[tableName]

    for row in readSheet.rows:

        excelInfo = {'申请时间': '',  '标注人': '', '团队长': '', '账号': '', '正确率': '', '数量': '', '价格': '' ,}


        details = row[0].value
        correctRate = row[1].value

        if not details:
            continue

        newDetails = re.findall(r"[A-Za-z0-9]{13}", details)[0]

        print(newDetails)





tableName = '叶艳'
fileAddress = '/Users/wangjiacan/Desktop/自动工作相关/test.xlsx'


readExcel(fileAddress, tableName)