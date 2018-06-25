#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time
import calendar
import datetime

#获取当前时间的时间戳
time_now = int(time.time())

## 当前日期的时间格式
curdate = datetime.date.today()

#本地时间转换成时间戳
def time_array(time0):
    #转换成时间数组
    time_array1 = time.strptime(time0, "%Y-%m-%d")
    #转换成时间戳
    time_stamp = time.mktime(time_array1)
    return(time_stamp)
#时间戳方式去计算班次
def work_time(time0):
    #初始班次时间搓
    curtime_1 = time.mktime(time.strptime("2018-04-20", "%Y-%m-%d"))
    curtime_2 = time.mktime(time.strptime("2018-04-21", "%Y-%m-%d"))
    curtime_0 = curtime_2 - curtime_1
    #格式化时间戳为本地的时间
    time_local = time.localtime(time0)
    #转换成新的时间格式   
    dt = time.strftime("%Y-%m-%d",time_local)
    a = dt.split('-')
    data = calendar.weekday(int(a[0]),int(a[1]),int(a[2]))
    #班次表和星期表
    classes=('连班','主班','夜班','下夜班','休假')
    weekdays=('周一','周二','周三','周四','周五','周六','周日')
    # 计算班次周期
    b = int(abs(((time0-curtime_1)/curtime_0))%5)
    # 判断班次
    if b==2 and (data ==1 or data ==3 or data==6):
        print("%s/%s/%s,这是%s,而这天是早夜班！"%(a[0],a[1],a[2],weekdays[data]))
    else:
        print("%s/%s/%s,这是%s,而这天是%s！"%(a[0],a[1],a[2],weekdays[data],classes[b]))

work_time(time_array("2018-06-25"))
work_time(time_now)
#时间格式的时间之差天数
def days_time(time1,time2):
    str1 = time1.split('-')
    str2 = time2.split('-')
    d1 = datetime.datetime(int(str1[0]),int(str1[1]),int(str1[2]))
    d2 = datetime.datetime(int(str2[0]),int(str2[1]),int(str2[2]))
    # d0 = (d1 – d2).days
    print((d1-d2).days)

# dt1 = "2018-06-05"
# dt2 = "2018-06-01"

# days_time(dt1,dt2)