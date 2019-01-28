#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time
import calendar
import datetime
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from flask import  render_template
import json
import mysql
import rili_a
import rili_b

# app = Flask(__name__)

app = Flask(__name__,static_url_path='')
#静态模板index.html等都放在‘/home/ronny/mywebsite/static/'下。　路由不用再加’/static/index.html‘而是'index.html'就好
@app.route('/')
def index():
    # return app.send_static_file('index.html')
    return render_template ('index.html', contents=[i for i in range(10)])

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s!</h1>' % name

# @app.route('/1')
# def hello():
#     return jsonify(request.args)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return do_the_login()
#     else:
#         return show_the_login_form()

#默认路径访问登录页面
@app.route('/login.html')
def login():
    return render_template('login.html')

#默认路径访问注册页面
@app.route('/regist')
def regist():
    return render_template('regist.html')


@app.route("/yezi/2")
def rili_days():
    # 使用方法 http://127.0.0.1:5000/2?begin_time=2018-09-09&end_time=2018-11-09
    # 烨烨的详情排班表
    params = request.args
    begin_time = params.get('begin_time')
    datetime_dt = datetime.datetime.today()
    today_time = datetime_dt.strftime("%Y/%m/%d")
    if not begin_time:
        begin_time = today_time.replace("/","-",3)
    end_time = params.get('end_time')
    if not end_time:
        end_time = today_time.replace("/","-",3)
    res = rili_a.rili_for(begin_time, end_time)
    # print(res)
    return render_template('top.html', name=res)

@app.route("/yezi/3")
def weekdays_days():
    # 周末匹配烨烨的班次表
    params = request.args
    begin_time = params.get('begin_time')
    datetime_dt = datetime.datetime.today()
    today_time = datetime_dt.strftime("%Y/%m/%d")
    if not begin_time:
        begin_time = today_time.replace("/","-",3)
    end_time = params.get('end_time')
    if not end_time:
        end_time = today_time.replace("/","-",3)
    res = rili_a.rili_weekdays(begin_time, end_time)
    # print(res)
    return render_template('top.html', name=res)

@app.route("/yezi/5")
def weekdays_days_test():
    # 周末匹配烨烨的班次表
    # 使用方法 http://127.0.0.1:5000/yezi/5?time0=2019-01-01+-+2019-01-24
    time1 = request.args.get('time0')
    time_str = time1.split(' - ')
    begin_time = time_str[0]
    end_time = time_str[1]
    res = rili_a.rili_weekdays(begin_time,end_time)
    return render_template('top.html', name=res)

@app.route('/sql/4',methods=['GET'])
def start1():
    db = mysql.Mysql()
    return jsonify(db.queryData())

if __name__=="__main__":
    app.run(debug=True) 
