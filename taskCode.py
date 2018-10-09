#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import openpyxl
import os

def readExcel(fileLocation, tableName):
    """
    excel读取函数
    输入字段说明：
    fileLocation：excel存放路径，字符串类型
    tableName：excel子表表名，字符串类型
    columnCount：读取的列数列表，列表类型
    excelType：读取的excel标题栏，列表类型
    输出字段说明：
    excelInfoList：返回已读取的数据列表，列表类型
    """
    excelInfoList = []
    numberingList = []
    newNumberingList = []

    readWorkbook = openpyxl.load_workbook(fileLocation)
    tableNameList = readWorkbook.get_sheet_names()
    position = tableNameList.index(tableName)
    readSheet = readWorkbook.get_sheet_by_name(readWorkbook.get_sheet_names()[position])


    for row in readSheet.rows:
        ip = row[0].value
        httpType = row[1].value
        checkDtime = row[2].value

        if not ip:
            continue

        b = '编号：{productId}，账号：{score}，密码：{page}'.format(productId=ip, score=httpType, page=checkDtime)
        excelInfoList.append(b)
        print(b)

        numberingList.append(ip)

    newNumberingList = list(set(numberingList))

    for a in newNumberingList:
        print(a)


    for i in newNumberingList:
        print(numberingList.count(i))
    return excelInfoList


fileLocation = '/Users/wangjiacan/Desktop/自动工作相关/任务码生成表格.xlsx'
tableName = '工作表1'
columnCount = ['A', 'B', 'C']
excelType = ['1', '2', '3']

a = readExcel(fileLocation, tableName)

