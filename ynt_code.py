#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import openpyxl
import time

def readExcel(fileLocation, tableName):

    excelInfoList = []
    numberingList = []

    readWorkbook = openpyxl.load_workbook(fileLocation)
    tableNameList = readWorkbook.get_sheet_names()
    position = tableNameList.index(tableName)
    readSheet = readWorkbook.get_sheet_by_name(readWorkbook.get_sheet_names()[position])


    for row in readSheet.rows:
        ip = row[0].value
        httpType = row[1].value

        numbering = time.strftime("%Y%m%d", time.localtime())

        b = '编号：{productId}，账号：{score}，密码：{page}'.format(productId=numbering, score=ip, page=httpType)
        excelInfoList.append(b)
        print(b)



fileLocation = '/Users/wangjiacan/Desktop/自动工作相关/再启账号.xlsx'
tableName = 'Sheet1'

a = readExcel(fileLocation, tableName)

