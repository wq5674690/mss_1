#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import datetime
import os
# 引入日历模块
import calendar

datetime_dt = datetime.datetime.today()  # 获取当前日期和时间, 2017-10-26 10:03:28.693198
datetime_str = datetime_dt.strftime("%Y/%m/%d %H:%M:%S")  # 将datetime 对象转换为字符串 , '2017/10/26 10:03:28'
datetime_str1 = datetime_dt.strftime("%Y/%m/%d")  # 将datetime 对象转换为字符串 , '2017/10/26'

dir_1 = "/Users/mengshishang/mms/file/others_file"
directory = os.path.exists(dir_1)  #是否存在这个文件夹和文件

if (directory):
    print(datetime_str,'\n'+"文件夹已存在")
else:
    print(datetime_str,'\n'+"文件夹不存在")
    os.mkdir(dir_1)



# 输入指定年月
yy = int(input("输入年份: "))
mm = int(input("输入月份: "))

# 显示日历
print(calendar.month(yy,mm))


