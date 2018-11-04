#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import os

def dataCcomparison(path, fileName, markingDataList):
    markingList = []

    filePath = path + fileName
    readFile = open(filePath)
    fileContent = readFile.readlines()

    print("{name}筛选前文件数：{sum}".format(name=fileName, sum=len(fileContent)))

    for file in fileContent:
        result = markingDataList.count(file.strip('\n'))

        if result == 1:
            continue

        markingList.append(file)
        markingDataList.append(file.strip('\n'))

    readFile.close()

    print("{name}筛选后剩余文件数：{sum}".format(name=fileName, sum=len(markingList)))

    writeFile = open(filePath, 'w')

    for marking in markingList:
        writeFile.write(str(marking))

    writeFile.close()


if __name__ == '__main__':
    markingDataList = []

    dataPath = r"D:\自动工作相关\txt\\"

    fileNameList = os.listdir(dataPath)

    for fileName in fileNameList:
        dataCcomparison(dataPath, fileName, markingDataList)
        print("总问题文件数：{sum}".format(sum=len(markingDataList)))

    print("程序运行已完！！！")
