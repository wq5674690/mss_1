#!/usr/bin/python
# -*- coding: utf-8 -*-
import calendar
import datetime
class MyCalendar(calendar.HTMLCalendar):
    def lastmonth(self, theyear, themonth):
        '''上个月的最后一天'''
        first = datetime.date(day=1, month=themonth, year=theyear)
        lastMonth = first - datetime.timedelta(days=1)
        return lastMonth.strftime("/log/%Y-%m/-%d")
    def nextmonth(self, theyear, themonth):
        '''下个月的第一天'''
        last = datetime.date(day=calendar.mdays[themonth], month=themonth, year=theyear)
        nextMonth = last + datetime.timedelta(days=1)
        return nextMonth.strftime("/log/%Y-%m/-%d")

    def formatday(self, day, weekday):
        if day == 0:
            #加入td的css
            return '<td class="out"> </td>' # day outside month
        else:
            return '<td><a href="./-%d">%d</a></td>' % (day, day)

    def formatweek(self, theweek):
        s = ''.join(self.formatday(d, wd) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatweekday(self, day):
        return '<th>%s</th>' % calendar.day_abbr[day] #day_abbr 改为 calendar.day_abbr

    def formatweekheader(self):
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        #加入th的css
        return '<thead><tr>%s</tr></thead>' % s

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = '%s %s' % (calendar.month_name[themonth], theyear) #month_name 改为 calendar.month_name
        else:
            s = '%s' % calendar.month_name[themonth] #month_name 改为 calendar.month_name
        #加入标题栏的css
        return '<caption>\
<span class="prev"><a href=%s>prev</a></span>\
<span class="next"><a href=%s>next</a></span>\
%s</caption>' % (self.lastmonth(theyear, themonth),self.nextmonth(theyear, themonth),s)

    def formatmonth(self, theyear, themonth, withyear=True):
        v = ['<link rel="stylesheet" href="css/style.css">']
        a = v.append
        a('<table class="cal">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
c = MyCalendar(calendar.SUNDAY)
chunk=c.formatmonth(2018,12)
f=open("c.html","w+")
f.write(chunk)
f.close
