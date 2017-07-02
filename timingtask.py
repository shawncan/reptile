#!/usr/local/bin/Python3
# -*- coding: utf-8 -*-

import time
from apscheduler.schedulers.blocking import BlockingScheduler
from qiubaiFeatured import QSBK


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour=20, minute=00)
def my_job():
    print(
        "{start_time}定时任务开始执行".format(start_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    spider = QSBK()
    spider.start()
    print(
        "{end_time}定时任务执行结束".format(end_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))

sched.start()
