#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import *    #引入tkinter库
import calendar
# root = Tk()    #创建一个主窗口,Tk(className='aaa')定义一下参数值
# root.mainloop()    #主窗口的成员函数，主窗口运作起来，开始接受鼠标和键盘的操作。

# root = Tk(className='aaa')
# label = Label(root)
# label['text'] = 'This is a label.'
# label.pack()    #和控件的布局排版有关的设置
# root.mainloop()
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text=calendar.calendar(2018,w=4,l=1,c=8))
        self.helloLabel.pack()
        self.quitButton = Button(self, text='确认', command=self.quit)
        self.quitButton.pack()
        self.quitButton = Button(self, text='退出', command=self.quit)
        self.quitButton.pack()

app = Application()
# 设置窗口标题:
app.master.title(calendar.month(2018,4))
# 主消息循环:
app.mainloop()