#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import time
import calendar
import datetime
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
import json
import mysql
import rili_a

app = Flask(__name__)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

@app.route("/hello")
def hello():    
    return "Hello World!"
@app.route("/2")
# 烨烨的详情排班表
def rili_days():
    return rili_a.rili_for("2018-07-23","2018-10-28")
@app.route("/3")
# 周末匹配烨烨的班次表
def weekdays_days():
    return rili_a.rili_weekdays("2018-07-01","2018-12-31")
@app.route('/4',methods=['GET'])
def start1():
    db = mysql.Mysql()
    return jsonify(db.queryData())

if __name__=="__main__":
    app.run(debug=True) 
