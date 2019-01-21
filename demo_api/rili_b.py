#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import calendar
import datetime
import  flask
import json

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
    return time_stamp

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
    data = calendar.weekday(int(a[0]),int(a[1]),int(a[2]))
    #班次表和星期表
    classes=("早夜班","下夜班","休 假","主 班")
    weekdays=("周一","周二","周三","周四","周五","周六","周日")
    # 计算班次周期
    b = int(abs(((time0-curtime_1)/curtime_0))%4)
    # 判断班次
    date_1 = dt.replace("-","/",3)
    dict_1 = {}
    dict_1['date'] = date_1
    dict_1['weekdays'] = weekdays[data]
    # js = json.dumps(dict_1, sort_keys=True, indent=4, separators=(',', ':'))
    if b==2 and (data==6 or data ==5):
        dict_1['classes'] = "上午班"
        js = json.dumps(dict_1, sort_keys=True, indent=4)
        return(js)
    else:
        dict_1['classes'] = classes[b]
        js = json.dumps(dict_1, sort_keys=True, indent=4)
        return(js)

# 字符格式转时间格式
def data_time(time0):
    str0 = time0.split("-")
    d0 = datetime.datetime(int(str0[0]),int(str0[1]),int(str0[2]))
    return d0

#时间格式的时间之差天数
def days_time(time1,time2):
    d1 = data_time(time1)
    d2 = data_time(time2)
    return (d2-d1).days

#时间格式的值精确到天数
def timedelta_days(time0):
    timeArray = time.strptime(time0, "%Y-%m-%d %H:%M:%S")
    #转换成新的时间格式(2016-05-05)
    dt_new = time.strftime("%Y-%m-%d",timeArray)
    return dt_new

# 遍历日期并打印班次
def rili_for(time0,time1):
    # print()
    # print("\n======这是烨烨的详情排班表======\n")
    msg = "\n======这是烨烨的详情排班表======" + flask.Markup()
    # print()
    for i in range(0,days_time(time0,time1)+1):
        t1 = data_time(time0) + datetime.timedelta(days=i)
        d1 = timedelta_days(str(t1))
        rili0 = work_time(time_array(d1))
        # print(rili0)
        msg += flask.Markup(rili0) + flask.Markup()
    return msg

# 遍历日期并打印周末匹配烨烨的班次
def rili_weekdays(time0,time1):
    # print("======周末匹配烨烨的班次表======")
    msg1 = "\n======周末匹配烨烨的班次表======" + flask.Markup('<br />')
    for i in range(0,days_time(time0,time1)+1):
        t1 = data_time(time0) + datetime.timedelta(days=i)
        d1 = timedelta_days(str(t1))
        rili0 = work_time(time_array(d1))
        b = rili0.split(',')
        c = b[1].split('这天')
        if b[2] == "下夜班！" and c[1] == "周六":
        # if b[2] == "下夜班！":
            # print(rili0)
            msg1 += flask.Markup(rili0) + flask.Markup('<br />')
        elif b[2] == "上午班！" and c[1] == "周日":
            # print(rili0)
            msg1 += flask.Markup(rili0) + flask.Markup('<br />')
        else:
            pass
    return msg1


print(rili_for('2019-01-20','2019-01-21'))