#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import openpyxl


def readExcel(fileLocation, tableName):
    """
    excel读取函数

    """
    excelInfoList = []
    numberingList = []

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


file = '/Users/wangjiacan/Desktop/自动工作相关/任务码生成表格.xlsx'
name = '工作表1'
columnCount = ['A', 'B', 'C']
excelType = ['1', '2', '3']

a = readExcel(file, name)
