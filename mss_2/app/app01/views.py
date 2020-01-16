#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from flask import  render_template
from flask import Blueprint
import config
from app.app01.GFWeather import *


app01=Blueprint('app01',__name__,static_url_path='')

@app01.route('/')
def show():
    return 'app01.hello'

@app01.route('/love')
def love():
    GFWeather().run()
#     return '登录成功'