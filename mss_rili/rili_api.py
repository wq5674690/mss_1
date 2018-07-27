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
    return time_stamp
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
        return("%s/%s/%s,这天%s,早夜班！"%(a[0],a[1],a[2],weekdays[data]))
    else:
        return("%s/%s/%s,这天%s,%s！"%(a[0],a[1],a[2],weekdays[data],classes[b]))

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
    # print("\n======这是烨烨的详情排班表======\n")
    msg = "\n======这是烨烨的详情排班表======\n"
    for i in range(0,days_time(time0,time1)+1):
        t1 = data_time(time0) + datetime.timedelta(days=i)
        d1 = timedelta_days(str(t1))
        rili0 = work_time(time_array(d1))
        msg += "%s \n" % rili0
    return msg
# 遍历日期并打印周末匹配烨烨的班次
def rili_weekdays(time0,time1):

    # print("\n======周末匹配烨烨的班次表======\n")
    msg = "\n======周末匹配烨烨的班次表======\n"
    for i in range(0,days_time(time0,time1)+1):
        t1 = data_time(time0) + datetime.timedelta(days=i)
        d1 = timedelta_days(str(t1))
        rili0 = work_time(time_array(d1))
        b = rili0.split(',')
        c = b[1].split('这天')
        if b[2] == "下夜班！" and c[1] == "周六":
        # if b[2] == "下夜班！":
            #print(rili0)
            msg += "%s \n" % rili0
        elif b[2] == "休假！" and c[1] == "周日":
            # print(rili0)
            msg += "%s \n" % rili0
        else:
            pass
    return msg

# rili_for("2018-06-25","2018-06-28")
print("\n======这是烨烨的工作排班表======")
# print()
print('''
    请选择类型编号：
    1、烨烨的详情排班表！
    2、周末匹配烨烨班次表！
    ''')
a=input("输入的编号为：" )

if int(a)==1:
    print()
    print(rili_for(input("请输入第一个日期："),input("请输入第二个日期：")))
elif int(a)==2:
    print()
    print(rili_weekdays(input("请输入第一个日期："),input("请输入第二个日期：")))
else:
    print()
    print("您输入的编号有误！")
# rili_for(input("请输入第一个日期："),input("请输入第二个日期："))
# rili_weekdays(input("请输入第一个日期："),input("请输入第二个日期："))


