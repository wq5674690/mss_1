#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from flask import Blueprint
from app.main.apl import *
from app.main.model import *
from flask import request
from flask import jsonify
from flask import render_template
import config

main=Blueprint('main',__name__,static_url_path='')

@main.route('/dd')
def show2():
    return 'dd.hello'

# @main.route('/city')
# # @main.route('/city.html')
# def city():
#     return render_template('city.html')
