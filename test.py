#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import os
import json

class Reviewkujiale(object):
    def __init__(self):
        self.standard = '/Users/wangjiacan/Desktop/自动工作相关/原始任务/'
        self.review = '/Users/wangjiacan/Desktop/自动工作相关/eeec3ab5cb261/原始任务/'
        self.standardList = []
        self.reviewList = []

        self.correct = 0
        self.error = 0


    def fileList(self, path):
        fileList = os.listdir(path)
        newFileList = []

        for i in fileList:
            if i == '.DS_Store':
                continue

            newFileList.append(i)

        newFileList.sort()
        return newFileList

    def result(self):
        for i in range(len(self.standardList)):
            standardFile = self.standard +self.standardList[i]
            reviewFile = self.review + self.reviewList[i]

            standardJson = open(standardFile, encoding='utf-8')
            reviewJson = open(reviewFile, encoding='utf-8')

            standardValue = json.load(standardJson)['tags']
            reviewValue = json.load(reviewJson)['tags']

            if standardValue == reviewValue:
                self.correct +=1
                os.remove(reviewFile)
            else:
                self.error +=1


    def new_result(self):
        for i in range(len(self.standardList)):
            standardFile = self.standard +self.standardList[i]
            reviewFile = self.review + self.reviewList[i]

            standardJson = open(standardFile, encoding='utf-8')
            reviewJson = open(reviewFile, encoding='utf-8')

            standardValue = json.load(standardJson)['tags'][0:2]
            reviewValue = json.load(reviewJson)['tags'][0:2]

            if standardValue == reviewValue:
                self.correct +=1
                os.remove(reviewFile)
            else:
                self.error +=1

    def newResult(self):
        for i in range(len(self.standardList)):
            standardFile = self.standard + self.standardList[i]
            reviewFile = self.review + self.reviewList[i]

            standardJson = open(standardFile, encoding='utf-8')
            reviewJson = open(reviewFile, encoding='utf-8')

            standardValue = json.load(standardJson)['tags']
            reviewValue = json.load(reviewJson)['tags']

            standardList = standardValue.split(';')
            reviewList = reviewValue.split(';')

            shuju = 0

            for a in standardList:
                b = reviewList.count(a)

                if b == 0:
                    shuju += 1
                    break

            if shuju != 0:
                self.correct +=1
                os.remove(reviewFile)
            else:
                self.error +=1



    def start(self):
        self.standardList = self.fileList(self.standard)
        self.reviewList = self.fileList(self.review)

        self.newResult()

        correctRate = (self.correct / 100)

        print(correctRate)


if __name__ == '__main__':
    extract = Reviewkujiale()
    extract.start()