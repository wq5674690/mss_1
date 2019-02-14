#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import os
import time
import psutil
# 引入日历模块
import calendar

# 使用方法 http://127.0.0.1:5000/yezi/5?time0=2019-01-01+-+2019-01-24
# time1 = request.args.get('time0')
# time0_str = time1['param']
#时间戳方式去计算班次
def work_time(time0):
    #初始班次时间搓
    curtime_1 = time.mktime(time.strptime("2018-08-28", "%Y-%m-%d"))
    curtime_2 = time.mktime(time.strptime("2018-08-29", "%Y-%m-%d"))
    curtime_0 = curtime_2 - curtime_1
    #格式化时间戳为本地的时间
    time_local = time.localtime(time0)
    #转换成新的时间格式
    dt = time.strftime("%Y-%m-%d",time_local)
    a = dt.split('-')
    print(a)
    data = calendar.weekday(int(a[0]),int(a[1]),int(a[2]))
    #班次表和星期表
    classes=('早夜班','下夜班','休 假','主 班')
    weekdays=('周一','周二','周三','周四','周五','周六','周日')
    # 计算班次周期
    b = int(abs(((time0-curtime_1)/curtime_0))%4)
    # 判断班次
    if b==2 and (data==6 or data ==5):
        return("%s/%s/%s,这天%s,上午班！"%(a[0],a[1],a[2],weekdays[data]))
    else:
        return("%s/%s/%s,这天%s,%s！"%(a[0],a[1],a[2],weekdays[data],classes[b]))

# today_time = datetime.datetime.today("%Y-%m-%d")
work_time('2019-01-20')