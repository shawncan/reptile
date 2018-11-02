#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import os
import json

path='/Users/wangjiacan/Desktop/自动工作相关/test/'
#获取该目录下所有文件，存入列表中
fileNameList = os.listdir(path)
p = 0

for fileName in fileNameList:
    combinedBed = ['28', '6', '19', '47']
    assembleSofa = ['31', '15', '19', '39']
    filePath = path + fileName

    if fileName[0] == '.':
        continue

    p +=1
    readFile = open(filePath)

    fileContent = readFile.read()
    markingData = json.loads(fileContent)
    marking = markingData['tags']

    markingList = marking.split(';')

    a = 0
    for tag in combinedBed:
        b = markingList.count(tag)

        if b == 1:
            a += 1

    if a == 4 or a == 3:
        for removeTag in combinedBed:
            try:
                markingList.remove(removeTag)
            except:
                print("无移除对象")

        markingList.insert(0, 29)



    for tag in assembleSofa:
        b = markingList.count(tag)

        if b == 1:
            a += 1

    if a == 4 or a == 3:
        for removeTag in assembleSofa:
            try:
                markingList.remove(removeTag)
            except:
                print("无移除对象")

        markingList.insert(0, 32)




    # 把已经处理好的标签重新写入

    newMarking = ''

    for i in range(len(markingList)):
        x = i + 1

        newMarking = newMarking +  str(markingList[i])

        if x == len(markingList):
            continue

        newMarking = newMarking + ';'

    newTag = {"tags":""}

    newTag['tags'] = newMarking


    readFile.close()

    writeFile = open(filePath, 'w')

    writeFile.write(str(newTag))

    writeFile.close()


print(p)




