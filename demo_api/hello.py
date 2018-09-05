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

app = Flask(__name__)

app = Flask(__name__,static_url_path='')
#静态模板index.html等都放在‘/home/ronny/mywebsite/static/'下。　路由不用再加’/static/index.html‘而是'index.html'就好
@app.route('/')
def index():
    return app.send_static_file('cat.html')

@app.route('/1')
def hello():
    return jsonify(request.args)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()
@app.route("/hello")
def hello2():
    return "Hello World!"
@app.route("/2")
def rili_days():
    # 使用方法 http://127.0.0.1:5000/2?begin_time=2018-09-09&end_time=2018-11-09
    # 烨烨的详情排班表
    params = request.args
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = '2018-08-28'
    end_time = params.get('end_time')
    if not end_time:
        end_time = "2018-10-28"
    res = rili_a.rili_for(begin_time, end_time)
    # print(res)
    return render_template('index.html', name=res)

@app.route("/3")
def weekdays_days():
    # 使用方法 http://127.0.0.1:5000/3?begin_time=2018-09-09&end_time=2018-11-09
    params = request.args
    begin_time = params.get('begin_time')
    if not begin_time:
        begin_time = '2018-08-28'
    end_time = params.get('end_time')
    if not end_time:
        end_time = "2018-10-28"
    res = rili_a.rili_weekdays(begin_time, end_time)
    # print(res)
    return render_template('index.html', name=res)
    # 周末匹配烨烨的班次表
    # return rili_a.rili_weekdays("2018-08-28","2018-12-31")
@app.route('/4',methods=['GET'])
def start1():
    db = mysql.Mysql()
    return jsonify(db.queryData())
# @app.route("/index.html")
# def index():
#      return static/index.html
if __name__=="__main__":
    app.run(debug=True) 
