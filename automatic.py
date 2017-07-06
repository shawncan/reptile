#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

from crontab import CronTab
 
# 创建当前用户的crontab，当然也可以创建其他用户的，但得有足够权限
my_user_cron  = CronTab(user=True)
 
# 创建任务
job = my_user_cron.new(command='python /opt/wjc/tqiubaiFeatured.py >> /opt/wjc/automatic.log')
 
# 设置任务执行周期，每两分钟执行一次
job.setall('00 20 * * * *')
 
# 同时可以给任务设置comment，这样就可以根据comment查询，很方便
job.set_comment("tqiubaiFeatured.py正在运行")
 
# 根据comment查询，当时返回值是一个生成器对象，不能直接根据返回值判断任务是否#存在，如果只是判断任务是否存在，可直接遍历my_user_cron.crons
iter = my_user_cron.find_comment('tqiubaiFeatured.py正在运行')
 
# 任务的disable和enable， 默认enable
job.enable(False)
job.enable()
 
# 最后将crontab写入配置文件
my_user_cron.write()