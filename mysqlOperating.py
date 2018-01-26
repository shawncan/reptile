#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import pymysql
import logging
import configparser


class MYSQL(object):

    def __init__(self):
        conf = configparser.ConfigParser()
        conf.read("/Users/wangjiacan/Desktop/代码/Profile/localConfiguration.ini")

        self.host = conf.get("localServer", "host")
        self.port = int(conf.get("localServer", "port"))
        self.user = conf.get("localServer", "user")
        self.password = conf.get("localServer", "password")
        self.dbName = conf.get("localServer", "dbname")

    def getCursor(self):
        # 建立数据库链接
        self.db = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.dbName, charset='utf8')

        # 创建游标对象
        cursor = self.db.cursor()

        # 返回游标对象
        return cursor

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

    def executeOperation(self,sql):
        # 操作状态
        operatingStatus = 0

        # 建立连接获取游标对象
        cur = self.getCursor()

        try:
            # 执行SQL语句
            cur.execute(sql)

            # 提交修改
            self.db.commit()
        except Exception as e:
            print(e)

            # 错误回滚
            self.db.rollback()

            # 更改操作状态
            operatingStatus = 1

        # 关闭游标
        cur.close()

        # 关闭数据库连接
        self.db.close()

        return operatingStatus

