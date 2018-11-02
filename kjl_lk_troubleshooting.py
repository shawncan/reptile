#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import os
import re


def troubleshooting(path, fileNameList):
    a = 0
    imageNameList = []


    for fileName in fileNameList:
        markingList = []
        questionLabel = ['14', '15', '17', ]

        filePath = path + fileName

        if fileName[0] == '.':
            continue

        print(fileName)
        readFile = open(filePath)

        fileContent = readFile.read()
        frameDataList = re.findall(r'"tags":"[0-9]*"', fileContent)

        for frameData in frameDataList:
            marking = frameData[8:-1]
            markingList.append(marking)

        print(markingList)
        for marking in markingList:
            result = questionLabel.count(marking)

            if result == 1:
                imageName = fileName[:-4] + '.jpg'
                imageNameList.append(imageName)
                break

        a += 1
        print(a)

    return imageNameList



#获取该目录下所有文件，存入列表中
# path ='/Users/wangjiacan/Desktop/自动工作相关/test/'
path='/Users/wangjiacan/Desktop/自动工作相关/标框/'

outputFile = '/Users/wangjiacan/Desktop/自动工作相关/test_1.txt'
fileNameList = os.listdir(path)

imageNameList = troubleshooting(path, fileNameList)

print(imageNameList)
print(len(imageNameList))

writeFile = open(outputFile, 'w')

for imageName in imageNameList:
    writeFile.write(str(imageName) + '\n')

writeFile.close()

