#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import os

path='/Users/wangjiacan/Desktop/打标样本数据/'
#获取该目录下所有文件，存入列表中
f = os.listdir(path)

n = 0

for i in f:

    # 设置旧文件名（就是路径+文件名）
    oldname = path + i

    # 设置新文件名
    newname = path + '15_' + i[2:]

    # 用os模块中的rename方法对文件改名
    os.rename(oldname, newname)
    print(oldname, '======>', newname)

    n += 1