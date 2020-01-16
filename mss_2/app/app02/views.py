#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from flask import Blueprint
from app.app02 import *
from flask import request
from flask import jsonify
from flask import render_template
import datetime
from app.app02.rili_a import rili_for,rili_weekdays
from app.app02.salt_1 import *
from app.app02.salt_2 import *
import config
import os
from werkzeug.utils import secure_filename
app02=Blueprint('app02',__name__,static_url_path='')

@app02.route('/')
def show():
    return render_template('index2.html', contents=[i for i in range(10)])

@app02.route("/yezi/2")
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
    res = rili_for(begin_time, end_time)
    # print(res)
    return render_template('top.html', name=res)

@app02.route("/yezi/3")
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
    res = rili_weekdays(begin_time, end_time)
    # print(res)
    return render_template('top.html', name=res)

@app02.route("/yezi/5")
def weekdays_days_test():
    # 周末匹配烨烨的班次表
    # 使用方法 http://127.0.0.1:5000/yezi/5?time0=2019-01-01+-+2019-01-24
    time1 = request.args.get('time0')
    time_str = time1.split(' - ')
    begin_time = time_str[0]
    end_time = time_str[1]
    res = rili_weekdays(begin_time,end_time)
    return render_template('top.html', name=res)


@app02.route('/salt/1',methods=['post', 'GET'])
def salt_conn1():
    # params = request.args
    myfrom= request.form
    v1 = SaltAPI(config.salt_config['v11'])
    v2 = SaltAPI(config.salt_config['v12'])
    v3 = SaltAPI(config.salt_config['v13'])
    v4 = SaltAPI(config.salt_config['v14'])
    v5 = SaltAPI(config.salt_config['v15'])
    # print(type(myfrom['salt_v']))
    if myfrom['salt_v'] == 'salt1':
        salt = v1
    elif myfrom['salt_v'] == 'salt2' :
        salt = v2
    elif myfrom['salt_v'] == 'salt3' :
        salt = v3
    elif myfrom['salt_v'] == 'salt4' :
        salt = v4
    else:
        salt = v5
    minions = myfrom['minions']
    salt_method1 = myfrom['salt_method']
    salt_params1 = myfrom['salt_params']
    ret1 = salt.remote_execution_module(minions, salt_method1, salt_params1)
    print(ret1)
    return jsonify(ret1)

@app02.route('/salt/2',methods=['post', 'GET'])
def salt_conn2():
    # params = request.args
    myfrom= request.form
    v1 = SaltApi(config.salt_config['v11'])
    v2 = SaltApi(config.salt_config['v12'])
    v3 = SaltApi(config.salt_config['v13'])
    v4 = SaltApi(config.salt_config['v14'])
    v5 = SaltApi(config.salt_config['v15'])
    #
    if myfrom['salt_v'] == 'salt1':
        salt = v1
    elif myfrom['salt_v'] == 'salt2' :
        salt = v2
    elif myfrom['salt_v'] == 'salt3' :
        salt = v3
    elif myfrom['salt_v'] == 'salt4' :
        salt = v4
    else:
        salt = v5
    minions = myfrom['minions']
    salt_params1 = []
    salt_params1.append(myfrom['salt_ip'])
    salt_params1.append(myfrom['salt_post'])
    ret1 = salt.salt_command(minions, 'network.connect', salt_params1)
    return jsonify(ret1)

@app02.route('/salt/3',methods=['post', 'GET'])
def salt_conn3():
    # params = request.args
    myfrom= request.form
    v1 = SaltApi(config.salt_config['v11'])
    v2 = SaltApi(config.salt_config['v12'])
    v3 = SaltApi(config.salt_config['v13'])
    v4 = SaltApi(config.salt_config['v14'])
    v5 = SaltApi(config.salt_config['v15'])
    if myfrom['salt_v'] == 'salt1':
        salt = v1
    elif myfrom['salt_v'] == 'salt2' :
        salt = v2
    elif myfrom['salt_v'] == 'salt3' :
        salt = v3
    elif myfrom['salt_v'] == 'salt4' :
        salt = v4
    else:
        salt = v5
    minions = myfrom['minions']
    salt_params1 = []
    salt_params1.append('salt://files/2/' + myfrom['salt_ip'])
    salt_params1.append(myfrom['salt_post'])
    print(salt_params1)
    ret1 = salt.salt_command(minions, 'cp.get_file', salt_params1)
    return jsonify(ret1)

@app02.route('/upload', methods=['POST', 'GET'])
def upload():
  if request.method == 'POST':
    f = request.files['file']
    basepath = os.path.dirname(__file__) # 当前文件所在路径
    # print(basepath)
    upload_path = os.path.join(basepath, 'uploads',secure_filename(f.filename)) #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)
    return '上传成功'
  return render_template('upload.html')