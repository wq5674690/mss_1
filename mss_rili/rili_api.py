#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
# 引入日历模块
import calendar

def rili(yy,mm,dd):

    # 将日期时间转为时间戳
    curtime_1 = time.mktime(time.strptime("2018-04-20", "%Y-%m-%d"))
    curtime_2 = time.mktime(time.strptime("2018-04-21", "%Y-%m-%d"))
    curtime_0 = curtime_2 - curtime_1
    curtime = time.mktime(time.strptime("%s-%s-%s" % (yy,mm,dd), "%Y-%m-%d"))
    data = calendar.weekday(yy,mm,dd)
    classes=('连班','主班','夜班','下夜班','休假')
    weekdays=('周一','周二','周三','周四','周五','周六','周日')
    # 计算班次周期
    a = int(abs(((curtime-curtime_1)/curtime_0))%5)
    # 判断班次
    if a==2 and (data ==1 or data ==3 or data==6):
        print("%s/%s/%s,这是%s,而这天是早夜班！"%(yy,mm,dd,weekdays[data]))
    else:
        print("%s/%s/%s,这是%s,而这天是%s！"%(yy,mm,dd,weekdays[data],classes[a]))

date1=input("请输入日期：").split('-')
rili(int(date1[0]),int(date1[1]),int(date1[2]))

