#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import os
import json

def troubleshooting(path, fileNameList, questionLabel, errorLabelList, a):
    imageNameList = []
    for fileName in fileNameList:
        filePath = path + fileName

        if fileName[0] == '.':
            continue

        print("第{num}:{name}".format(num=a, name=fileName))
        readFile = open(filePath)

        fileContent = readFile.read()
        markingData = json.loads(fileContent.replace("'","\""))
        marking = markingData['tags']

        markingList = marking.split(';')

        for marking in markingList:
            b = questionLabel.count(marking)

            if b == 1:
                imageName = fileName[:-4] + '.jpg'
                imageNameList.append(imageName)
                break

        for imageName in imageNameList:
            c = errorLabelList.count(imageName)

            if c == 1:
                imageNameList.remove(imageName)

    return imageNameList



# 获取该目录下所有文件，存入列表中
path = '/Users/wangjiacan/Desktop/自动工作相关/标签/'
# path ='/Users/wangjiacan/Desktop/自动工作相关/test/'
outputFile = '/Users/wangjiacan/Desktop/自动工作相关/test.txt'

labelCombination = [['7', '8', '5'], ['37', '39'], ['44', '47', '40', '33'], ['42', '-1']]
labelList = []
errorLabelList = []
a = 0

for label in labelCombination:
    a +=1
    fileNameList = os.listdir(path)

    imageNameList = troubleshooting(path, fileNameList, label, errorLabelList, a)

    labelList.append(imageNameList)

    for imageName in imageNameList:
        errorLabelList.append(imageName)


writeFile = open(outputFile, 'w')

for tag in labelList:
    print(len(tag))
    for imageName in tag:
        writeFile.write(str(imageName) + '\n')

    writeFile.write('\n')

writeFile.close()

