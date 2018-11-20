#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import time

accountInformation = [
    {'账号': 'external.user2@163.com', '密码': '4AZcXEk6'},
    {'账号': 'external.user3@163.com', '密码': 'NxpDYluC'},
    {'账号': 'external.user4@163.com', '密码': 'OtkL010L'},
    {'账号': 'external.user5@163.com', '密码': 'SGL2k1FU'},
    {'账号': 'external.user6@163.com', '密码': 'CdDNyZbR'},
    {'账号': 'external.user7@163.com', '密码': 'VPFjfVOK'},
    {'账号': 'external.user8@163.com', '密码': 'qDDaKwnJ'},
    {'账号': 'external.user9@163.com', '密码': '4PixFJeK'},
    {'账号': 'external.user10@163.com', '密码': 'ykbonHkY'},
    {'账号': 'external.user11@163.com', '密码': 'dmiOJeJp'},
    {'账号': 'external.user12@163.com', '密码': 'm5kO9xdG'},
    {'账号': 'external.user13@163.com', '密码': 'nKFg48Ww'},
    {'账号': 'external.user14@163.com', '密码': 'SJvoFCz6'},
    {'账号': 'external.user15@163.com', '密码': 'jzIJJO4M'},
    {'账号': 'external.user16@163.com', '密码': '45vHAx2J'},
    {'账号': 'external.user17@163.com', '密码': '8oYeRAuz'},
    {'账号': 'external.user18@163.com', '密码': 'MpSSmYwz'},
    {'账号': 'external.user19@163.com', '密码': 'rkOL8uWB'},
    {'账号': 'external.user20@163.com', '密码': 'uOPsFRUE'},
    {'账号': 'external.user21@163.com', '密码': 'lrJFZmgS'},
]

numbering = time.strftime("%Y%m%d", time.localtime())


for i in accountInformation:
    account = i['账号']
    password = i['密码']

    code = '编号：{productId}，账号：{score}，密码：{page}'.format(productId=numbering, score=account, page=password)
    print(code)


