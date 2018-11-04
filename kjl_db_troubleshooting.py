#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import os
import json


def troubleshooting(path, fileNameList, questionLabel, a):
    imageNameList = []
    for fileName in fileNameList:
        filePath = path + fileName

        if fileName[0] == '.':
            continue

        print("第{num}:{name}".format(num=a, name=fileName))
        readFile = open(filePath)

        fileContent = readFile.read()
        markingData = json.loads(fileContent.replace("'", "\""))
        marking = markingData['tags']

        markingList = marking.split(';')

        for marking in markingList:
            b = questionLabel.count(marking)

            if b == 1:
                imageName = fileName[:-4] + '.jpg'
                imageNameList.append(imageName)
                break

    return imageNameList


# 获取该目录下所有文件，存入列表中
# path = '/Users/wangjiacan/Desktop/自动工作相关/标签/'
path = r"D:\自动工作相关\标签\\"

# outputFile = '/Users/wangjiacan/Desktop/自动工作相关/test.txt'
outputFile = r"D:\自动工作相关\test_3.txt"

# 柜子
labelCombination = ['7', '8', '5']
# 边几与架子
# labelCombination = ['37', '39']
# 小物件
# labelCombination = ['44', '47', '40', '33']
# 屏风
# labelCombination = ['42', '-1']

labelList = []
errorLabelList = []
a = 1

fileNameList = os.listdir(path)

imageNameList = troubleshooting(path, fileNameList, labelCombination, a)

writeFile = open(outputFile, 'w')

for tag in imageNameList:
    writeFile.write(str(tag) + '\n')

writeFile.close()
