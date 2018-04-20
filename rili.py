#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import datetime
import os
import time
import psutil
# 引入日历模块
import calendar

datetime_dt = datetime.datetime.today()  # 获取当前日期和时间, 2017-10-26 10:03:28.693198
datetime_str = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")  # 将datetime 对象转换为字符串 , '2017/10/26 10:03:28'
datetime_str1 = datetime_dt.strftime("%Y/%m/%d")  # 将datetime 对象转换为字符串 , '2017/10/26'

# 默认每周的第一天是星期一，这里修改成星期天
calendar.setfirstweekday(calendar.SUNDAY)

# 显示日历，参数：年、字符长，行的间隔、每月之间的间隔
# print (calendar.calendar(2017,2,1,6))

# 输出某个月的日历
# print(calendar.month(2017,3))

# 输入指定年月
yy = int(input("输入年份: "))
mm = int(input("输入月份: "))
dd = int(input("输入日期: "))

# 格式化字符串转化为时间对象
curtime_1 = time.mktime(time.strptime("2018-04-20", "%Y-%m-%d"))
curtime_2 = time.mktime(time.strptime("2018-04-21", "%Y-%m-%d"))
curtime_0 = curtime_2 - curtime_1

# boolean = calendar.isleap(yy)  # x年是否为闰年
curtime = time.mktime(time.strptime("%s-%s-%s" % (yy,mm,dd), "%Y-%m-%d"))
data = calendar.weekday(yy,mm,dd)

classes=('连班','白班','夜班','下夜班','休假')
# print("初始时间戳:",curtime_1)
# print("一天的时间戳差为：",curtime_0)
# print("这是输入的时间戳",curtime)

# 将日期时间转为时间戳
time_s = datetime_dt.timestamp()
# print("现在的时间戳: {}".format(curtime))

# print("time_s=%s"%time_s)
a = int(abs(((curtime-curtime_1)/curtime_0))%5)

weekdays=('周一','周二','周三','周四','周五','周六','周日')
# print(weekdays[0])
# print(data)
# print(a)
if a==2 and data ==1 or 3 or 6:
    print("%s/%s/%s,这是%s,而这天是早夜班！"%(yy,mm,dd,weekdays[data]))
else:
    print("%s/%s/%s,这是%s,而这天是%s！"%(yy,mm,dd,weekdays[data],classes[a]))
# 显示日历
# # print(calendar.month(yy,mm))
# print(calendar.calendar(2018,w=4,l=1,c=8))

# calendar.weekday(year,month,day)


