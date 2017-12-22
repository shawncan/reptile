#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import openpyxl
import os


def dataProcessing(title):
    """
    转化写入数据函数
    输入字段说明：
    title：待转化文本列表，列表类型。
    输出字段说明：
    writeContentList：excel模块可写入的文本列表，列表类型
    """
    writeContentList = []
    columnList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'O']
    columnNum = len(title[0])
    rowsNum = len(title)
    newColumnList = columnList[0:columnNum]

    for num_1 in range(rowsNum):
        rows = num_1 + 1
        for num_2 in range(columnNum):
            writeContent = {'column': '', 'rows': '', 'content': '', }
            column = newColumnList[num_2]
            writeContent['column'] = column
            writeContent['rows'] = rows
            writeContentList.append(writeContent)

    contentList = []
    for num in range(len(title)):
        for key in title[num]:
            content = title[num][key]
            contentList.append(content)

    for i in range(len(writeContentList)):
        writeContentList[i]['content'] = contentList[i]

    return writeContentList


def writeExcel(fileLocation, writeContentList, tableName):
    """
    excel写入函数
    输入字段说明：
    fileLocation：excel存放路径，字符串类型
    tableName：excel子表表名，字符串类型
    writeContentList：excel模块可写入的文本列表，列表类型
    """
    if not os.path.exists(fileLocation):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = tableName
        workbook.save(fileLocation)

    existedWorkbook = openpyxl.load_workbook(fileLocation)
    tableNameList = existedWorkbook.get_sheet_names()
    if tableName in tableNameList:
        position = tableNameList.index(tableName)
        existedSheet = existedWorkbook.get_sheet_by_name(existedWorkbook.get_sheet_names()[position])
        row = existedSheet.max_row

        if row == 1:
            row = 0

        for i in range(len(writeContentList)):
            column = writeContentList[i]['column']
            content = writeContentList[i]['content']
            rows = writeContentList[i]['rows'] + row
            existedSheet["{column}{rows}".format(column=column, rows=rows)].value = content
    else:
        newSheet = existedWorkbook.create_sheet()
        newSheet.title = tableName
        for i in range(len(writeContentList)):
            column = writeContentList[i]['column']
            content = writeContentList[i]['content']
            rows = writeContentList[i]['rows']
            newSheet["{column}{rows}".format(column=column, rows=rows)].value = content

    existedWorkbook.save(fileLocation)


def readExcel(fileLocation, tableName, columnCount, excelType):
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

    readWorkbook = openpyxl.load_workbook(fileLocation)
    tableNameList = readWorkbook.get_sheet_names()
    position = tableNameList.index(tableName)
    readSheet = readWorkbook.get_sheet_by_name(readWorkbook.get_sheet_names()[position])

    for row in readSheet.rows:
        rowsInfoList = []

        for column in columnCount:
            rowsInfoList.append(row[column].value)
        excelInfoData = dict(zip(excelType, rowsInfoList))

        excelInfoList.append(excelInfoData)

    readWorkbook.save(fileLocation)

    return excelInfoList

def coverExcel(fileLocation, tableName, writeContentList):
    """
    excel覆盖函数
    输入字段说明：
    fileLocation：excel存放路径，字符串类型
    tableName：excel子表表名，字符串类型
    writeContentList：excel模块可写入的文本列表，列表类型
    """
    coverWorkbook = openpyxl.load_workbook(fileLocation)
    tableNameList = coverWorkbook.get_sheet_names()
    position = tableNameList.index(tableName)
    coverSheet = coverWorkbook.get_sheet_by_name(coverWorkbook.get_sheet_names()[position])

    coverWorkbook.remove_sheet(coverSheet)

    newSheet = coverWorkbook.create_sheet(tableName)

    for i in range(len(writeContentList)):
        column = writeContentList[i]['column']
        content = writeContentList[i]['content']
        rows = writeContentList[i]['rows']
        newSheet["{column}{rows}".format(column=column, rows=rows)].value = content

    coverWorkbook.save(fileLocation)
