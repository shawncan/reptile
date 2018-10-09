#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import openpyxl
import os
import sys
import configparser
import pymysql
import re


class BillingDataImport(object):
    #===========================================================================
    # '''
    # '''
    #===========================================================================
    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("/Users/wangjiacan/Desktop/sourceCode/configurationFile/localConfiguration.ini")

        self.host = conf.get("localServer", "host")
        self.port = int(conf.get("localServer", "port"))
        self.user = conf.get("localServer", "user")
        self.password = conf.get("localServer", "password")
        self.dbName = conf.get("localServer", "dbname")

        self.fileAddress = ''
        self.tableName = ''
        self.excelInfoList = []


    def getCursor(self):
        # 建立数据库链接
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.dbName, charset='utf8')

        # 创建游标对象
        cursor = self.db.cursor()

        # 返回游标对象
        return cursor


    def executeOperation(self, sql):
        # 创建游标对象
        cur = self.getCursor()

        # 操作状态
        operatingStatus = 0

        try:
            # 执行SQL语句
            cur.execute(sql)

            # 提交修改
            self.db.commit()
        except Exception as error:
            print(error)

            # 错误回滚
            self.db.rollback()

            # 更改操作状态
            operatingStatus = 1

        # 关闭游标
        cur.close()

        # 关闭数据库连接
        self.db.close()

        return operatingStatus


    def queryOperation(self,sql):
        # 建立连接获取游标对象
        cur = self.getCursor()

        # 执行SQL语句
        cur.execute(sql)

        # 获取查询数据
        # fetch*
        # all 所有数据, one 取结果的一行, many(size),去size行
        dataList = cur.fetchall()

        # 关闭游标
        cur.close()

        # 关闭数据库连接
        self.db.close()

        # 返回查询数据
        return dataList


    def writeIP(self):
        # 写入sql语句
        write_sql = """
        insert into azy_taskData (account, quantity) VALUES ("{account}", "{quantity}")
        """
        # 查询sql语句
        inquire_sql = """
        select * from azy_taskData WHERE account = "{account}" 
        """

        # 循环插入ip数据
        for infoData in self.excelInfoList:
            # 提取每个字典数据
            account = infoData["账号"]
            quantity = infoData["数量"]

            # 查询是否已存在ip信息
            searchResult = self.queryOperation(inquire_sql.format(account=account))

            # 插入ip信息
            if not searchResult:
                self.executeOperation(write_sql.format(account=account, quantity=quantity))
            else:
                continue


    def readExcel(self):
        """
        """
        readWorkbook = openpyxl.load_workbook(self.fileAddress)

        self.tableName = input("输入需要导入的表名：")
        readSheet = readWorkbook[self.tableName]

        for row in readSheet.rows:
            excelInfo = {'账号': '', '数量': ''}

            account = row[0].value
            quantity = row[1].value

            if not account:
                continue

            excelInfo['账号'] = re.findall(r"[A-Za-z0-9]{13}", account)[0]
            excelInfo['数量'] = quantity

            self.excelInfoList.append(excelInfo)


    def detailsProcessing(self):

        for infoData in self.excelInfoList:
            details = infoData["账号"]

            infoData["账号"] = details

        self.writeIP()


    def start(self):
        self.fileAddress = input("输入需要导入的文件名：")

        if not os.path.exists(self.fileAddress):
            print("{name}文件未找到，请确认：1.文件名是否输入正确。2.导入文件与脚本文件是否放在一起。".format(name=self.fileAddress))
            sys.exit()

        self.readExcel()

        if self.tableName == "official":
            self.writeIP()
            sys.exit()

        self.detailsProcessing()


if __name__ == '__main__':
    extract = BillingDataImport()
    extract.start()