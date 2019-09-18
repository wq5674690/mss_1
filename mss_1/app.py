#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
# from datetime import datetime
from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
from flask import  render_template
from flask import  url_for
from werkzeug.utils import secure_filename
import json
import sys,time
import rili_a,baf
import salt_1
import salt_2
import pymysql
import pymysql.cursors
import re,os
import config
import importlib,sys
importlib.reload(sys)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
import requests
from bs4 import BeautifulSoup
import city_dict


app = Flask(__name__,static_url_path='')
#静态模板index.html等都放在‘/home/ronny/mywebsite/static/'下。　路由不用再加’/static/index.html‘而是'index.html'就好
app.config.from_object(config)
db = SQLAlchemy(app=app)

class User(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    id= db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # id 整型，主键，自增，唯一
    login_name = db.Column(db.String(64), nullable = False)  # 名字 字符串长度为20
    passwd = db.Column(db.String(64), nullable = False)  # 名字 字符串长度为20
    phone = db.Column(db.String(20), nullable = False)  # 名字 字符串长度为20
    email = db.Column(db.String(64), nullable = False)  # 名字 字符串长度为20
    role = db.Column(db.String(64), nullable = False)  # 名字 字符串长度为20
    gen_time = db.Column(db.DateTime, nullable = False)
    state = db.Column(db.Boolean, default = False)

    __tablename__ = 'user'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名

    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return '< %r, %r, %r, %r, %r, %r, %r, %r>' % (self.id, self.login_name, self.passwd,self.phone,self.email,self.role,self.gen_time,self.state)

class Apollo(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    ap_id= db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # id 整型，主键，自增，唯一
    ap_date_time = db.Column(db.DateTime)
    ap_env = db.Column(db.String(128))
    ap_db_name = db.Column(db.String(128))
    ap_w_url = db.Column(db.String(128))
    ap_w_user = db.Column(db.String(128))
    ap_w_passwd = db.Column(db.String(128))
    ap_r_url = db.Column(db.String(128))
    ap_r_user = db.Column(db.String(128))
    ap_r_passwd = db.Column(db.String(128))
    ap_str_date = db.Column(db.String(128))

    __tablename__ = 'ap'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名

    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return f'<{self.ap_id},{self.ap_date_time},{self.ap_env},{self.ap_db_name},{self.ap_w_url},{self.ap_w_user},{self.ap_w_passwd},{self.ap_r_url},{self.ap_r_user},{self.ap_r_passwd},{self.ap_str_date}>'

class Salt(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    id= db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # id 整型，主键，自增，唯一
    date = db.Column(db.DateTime, nullable = False)
    url = db.Column(db.String(128), nullable = False)
    user = db.Column(db.String(128), nullable = False)
    password = db.Column(db.String(128), nullable = False)

    __tablename__ = 'salt'  # 该参数可选，不设置会默认的设置表名，如果设置会覆盖默认的表名

    def __repr__(self):  # 输出方法，与__str__类似，但是能够重现它所代表的对象
        return f'<{self.id},{self.date},{self.url},{self.user},{self.password}>'
    # 把对象格式转换成json格式
    def to_json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict

# @app.route('/')
@app.route('/index2.html')
def index2():
    # return app.send_static_file('index.html')
    return render_template ('index2.html', contents=[i for i in range(10)])

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s!</h1>' % name

@app.route('/welcome.html',methods=['POST','GET'])
def welcome():
    params = request.form
    city = params.get('city')
    print(city)
    cityname = '上海'
    city_name = city_dict.city_dict.get(cityname)
    print(city_name)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    # a=time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
    resp1 = requests.get("https://api.lovelive.tools/api/SweetNothings")
    if resp1.status_code == 200:
        print('获取土味情话...')
        b = resp1.text
    resp2 = requests.get('http://open.iciba.com/dsapi')
    if resp2.status_code == 200 :
        print('获取格言信息（双语）...')
        conentJson = resp2.json()
        content = conentJson.get('content')
        note = conentJson.get('note')
    print('获取天气信息...')
    weather_url = f'http://t.weather.sojson.com/api/weather/city/{city_name}'
    resp = requests.get(url=weather_url)
    if resp.status_code == 200:
        weatherJson = resp.json()
        # 今日天气
        today_weather = weatherJson.get('data').get('forecast')[1]
        # 今日日期
        today_time = time.strftime('%Y{y}%m{m}%d{d} %H:%M:%S', time.localtime(time.time())).format(y='年', m='月', d='日')
        # today_time = datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', m='月', d='日')
        # 今日天气注意事项
        notice = today_weather.get('notice')
        # 温度
        high = today_weather.get('high')
        high_c = high[high.find(' ') + 1:]
        low = today_weather.get('low')
        low_c = low[low.find(' ') + 1:]
        temperature = f"温度 : {low_c}/{high_c}"
        # 风
        fx = today_weather.get('fx')
        fl = today_weather.get('fl')
        wind = f"{fx} : {fl}"
        # 空气指数
        aqi = today_weather.get('aqi')
        aqi = f"空气 : {aqi}"
        today_msg = f"{today_time}\n{notice}。\n{temperature}\n{wind}\n{aqi}"
        # print(today_msg)
    sysversion = sys.version
    sysname = sys.platform
    return render_template('welcome.html', cityname=cityname,b=b, content=content, note=note  ,today_time=today_time,notice=notice,temperature=temperature,wind=wind,aqi=aqi,sysversion=sysversion,sysname=sysname)

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

#默认路径访问登录页面
@app.route('/login')
@app.route('/login.html')
def login():
    return render_template('login.html')

#默认路径访问注册页面
@app.route('/regist')
def regist():
    return render_template('admin-add.html')

@app.route('/order-add.html')
def order_add():
    return render_template('order-add.html')

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
    time1 = request.args.get('time0')
    time_str = time1.split(' - ')
    begin_time = time_str[0]
    end_time = time_str[1]
    res = rili_a.rili_weekdays(begin_time,end_time)
    return render_template('top.html', name=res)

@app.route('/sql/4',methods=['GET'])
def start1():
    db = config.Mysql()
    return jsonify(db.queryData())

@app.route('/salt/1',methods=['post'])
def salt_conn1():
    myfrom= request.form
    v1 = salt_1.SaltAPI(Salt.query.get(1).to_json())
    v2 = salt_1.SaltAPI(Salt.query.get(2).to_json())
    v3 = salt_1.SaltAPI(Salt.query.get(3).to_json())
    v4 = salt_1.SaltAPI(Salt.query.get(4).to_json())
    v5 = salt_1.SaltAPI(Salt.query.get(5).to_json())
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

@app.route('/salt/2',methods=['post'])
def salt_conn2():
    # params = request.args
    myfrom= request.form
    v1 = salt_2.SaltApi(Salt.query.get(1).to_json())
    v2 = salt_2.SaltApi(Salt.query.get(2).to_json())
    v3 = salt_2.SaltApi(Salt.query.get(3).to_json())
    v4 = salt_2.SaltApi(Salt.query.get(4).to_json())
    v5 = salt_2.SaltApi(Salt.query.get(5).to_json())
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

@app.route('/salt/3',methods=['post'])
def salt_conn3():
    # params = request.args
    myfrom= request.form
    v1 = salt_2.SaltApi(Salt.query.get(1).to_json())
    v2 = salt_2.SaltApi(Salt.query.get(2).to_json())
    v3 = salt_2.SaltApi(Salt.query.get(3).to_json())
    v4 = salt_2.SaltApi(Salt.query.get(4).to_json())
    v5 = salt_2.SaltApi(Salt.query.get(5).to_json())
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

@app.route('/upload', methods=['POST', 'GET'])
def upload():
  if request.method == 'POST':
    f = request.files['file']
    basepath = os.path.dirname(__file__) # 当前文件所在路径
    upload_path = os.path.join(basepath, 'static/uploads',secure_filename(f.filename)) #注意：没有的文件夹一定要先创建，不然会提示没有该路径
    f.save(upload_path)
    return redirect(url_for('upload'))
  return render_template('upload.html')

@app.route('/sql/1',methods=['GET'])
def start3():
    # 连接数据库
    connect = pymysql.connect(**config.mysql_config)
    cur = connect.cursor()
    sql = "SELECT * FROM runoob_tbl"
    cur.execute(sql)
    u = cur.fetchall()
    print(u)
    connect.close()
    return render_template('1.html', u=u)

@app.route('/order-list.html', methods=['POST', 'GET'])
@app.route('/ap', methods=['POST', 'GET'])
def orderlist():
    params = request.args
    page = int(params.get('page', 1))
    per_page = int(params.get('per_page', 10))
    start = params.get('start')
    end = params.get('end')
    if params.get('start') or params.get('end') or params.get('ap_env') or params.get('ap_w_url') or params.get('ap_r_url'):
        if start =='' and end =='':
            ap_env = '%' + params.get('ap_env') + '%'
            ap_w_url = '%' + params.get('ap_w_url') + '%'
            ap_r_url = '%' + params.get('ap_r_url') + '%'
            paginate = Apollo.query.filter(Apollo.ap_env.like(ap_env)).filter(Apollo.ap_w_url.like(ap_w_url)).filter(Apollo.ap_r_url.like(ap_r_url)).order_by(desc('ap_id')).paginate(page, per_page, error_out=False)
            stus = paginate.items
            print(stus)
            len_s = len(stus)
            return render_template('order-list.html', paginate=paginate, stus=stus, len_s=len_s)
        else:
            ap_env = '%'+params.get('ap_env')+'%'
            ap_w_url = '%'+params.get('ap_w_url')+'%'
            ap_r_url = '%' + params.get('ap_r_url') + '%'
            paginate = Apollo.query.filter(Apollo.ap_date_time.between(start, end)).filter(Apollo.ap_env.like(ap_env)).filter(Apollo.ap_w_url.like(ap_w_url)).filter(Apollo.ap_r_url.like(ap_r_url)).order_by(desc('ap_id')).paginate(page, per_page, error_out=False)
            stus = paginate.items
            print(stus)
            len_s = len(stus)
            return render_template('order-list.html', paginate=paginate, stus=stus, len_s=len_s)
    else:
        paginate = Apollo.query.order_by(desc('ap_id')).paginate(page, per_page, error_out=False)
        stus = paginate.items
        print(stus)
        len_s = len(stus)
        return render_template('order-list.html',paginate=paginate, stus=stus ,len_s=len_s)

@app.route('/apollo_select', methods=['POST', 'GET'])
def apollo_select():
    params  = request.args
    ap_id = params['ap_id']
    connect = pymysql.connect(**config.mysql_config)
    cur = connect.cursor()
    sql = ("SELECT * FROM ap WHERE ap_id= '%s';" %ap_id)
    cur.execute(sql)
    u = cur.fetchall()
    print(u)
    str2 = baf.apolloF(u[0])
    a=('OPERATION.' + u[0]['ap_db_name'])
    print(str2.af())
    b = a + '<br>' + '<br>' + str2.af()
    connect.commit()
    return b

@app.route('/ap_select', methods=['POST', 'GET'])
def apollo_select1():
    params  = request.args
    ap_id = params['ap_id']
    stu = Apollo.query.get(ap_id)
    print(stu)
    print(type(stu))
    a = jsonify(stu)
    print(a)
    # print(json_stu)
    return '转化成功'

@app.route('/apollo_update.html', methods=['POST', 'GET'])
@app.route('/apollo_update', methods=['POST', 'GET'])
def apollo_update():
    aab  = request.args
    ap_id = aab['ap_id']
    connect = pymysql.connect(**config.mysql_config)
    cur = connect.cursor()
    sql = (f"SELECT * FROM ap WHERE ap_id= '{ap_id}';")
    cur.execute(sql)
    u = cur.fetchall()
    connect.close()
    return render_template('order-update.html',u=u)

@app.route('/apollo_update2', methods=['POST', 'GET'])
def apollo_update2():
    if request.method == 'POST':
        my_from = request.form
        print(my_from)
        ap_id = my_from['ap_id']
        env = my_from['env']
        db_name = my_from['db_name']
        w_url = my_from['w_url']
        w_user = my_from['w_user']
        w_passwd = my_from['w_passwd']
        r_url = my_from['r_url']
        r_user = my_from['r_user']
        r_passwd = my_from['r_passwd']
        str_date = my_from['str_date']
        connect = pymysql.connect(**config.mysql_config)
        sql = (f"UPDATE ap SET ap_db_name = '{db_name}',ap_env='{env}',ap_w_url='{w_url}',ap_w_user='{w_user}',ap_w_passwd='{w_passwd}',  \
              ap_r_url='{r_url}',ap_r_user='{r_user}',ap_r_passwd='{r_passwd}',ap_str_date='{str_date}' WHERE ap_id = '{ap_id}' ")
        print(sql)
        cur = connect.cursor()
        cur.execute(sql)
        connect.commit()
    return '修改成功'

@app.route('/apollo_delete', methods=['POST', 'GET'])
def apollo_delete():
    aa  = request.args
    ap_id = aa['ap_id']
    connect = pymysql.connect(**config.mysql_config)
    cur = connect.cursor()
    sql = ("DELETE FROM ap WHERE ap_id= '%s';" %ap_id)
    print(sql)
    cur.execute(sql)
    connect.commit()
    return str('删除成功')

@app.route('/apollo_insert', methods=['POST', 'GET'])
def apollo_insert():
    # aa  = request.args
    if request.method == 'POST':
        my_from = request.form
        connect = pymysql.connect(**config.mysql_config)
        cur = connect.cursor()
        today_time = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
        env = my_from['env']
        db_name = my_from['db_name']
        w_url = my_from['w_url']
        w_user = my_from['w_user']
        w_passwd = my_from['w_passwd']
        r_url = my_from['r_url']
        r_user = my_from['r_user']
        r_passwd = my_from['r_passwd']
        str_date = my_from['str_date']
        sql = ("insert into ap(ap_date_time,ap_env,ap_db_name,ap_w_url,ap_w_user,ap_w_passwd,ap_r_url,ap_r_user,ap_r_passwd,ap_str_date) \
        VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (today_time,env,db_name,w_url,w_user,w_passwd,r_url,r_user,r_passwd,str_date))
        cur.execute(sql)
        #u = cur.fetchall()
        connect.commit()
    return str('创建成功')

# 使用装饰器的形式去捕获指定的错误码和异常
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html'),404

@app.route('/adminlist', methods=['POST', 'GET'])
def adminlist():
    params = request.args
    page = int(params.get('page', 1))
    per_page = int(params.get('per_page', 10))
    start = params.get('start')
    end = params.get('end')
    if params.get('start') or params.get('end') or params.get('login_name') :
        if start =='' and end =='':
            loginname = '%' + params.get('login_name') + '%'
            paginate = User.query.filter(User.login_name.like(loginname)).order_by(desc('id')).paginate(page, per_page, error_out=False)
            stus = paginate.items
            print(stus)
            len_s = len(stus)
            return render_template('admin-list.html', paginate=paginate, stus=stus, len_s=len_s)
        else:
            loginname = '%'+params.get('login_name')+'%'
            paginate = User.query.filter(User.gen_time.between(start, end)).filter(User.login_name.like(loginname)).order_by(desc('id')).paginate(page, per_page, error_out=False)
            stus = paginate.items
            print(stus)
            len_s = len(stus)
            return render_template('admin-list.html', paginate=paginate, stus=stus, len_s=len_s)
    else:
        paginate = User.query.order_by(desc('id')).paginate(page, per_page, error_out=False)
        stus = paginate.items
        print(stus)
        len_s = len(stus)
        return render_template('admin-list.html',paginate=paginate, stus=stus ,len_s=len_s)

@app.route('/adminadd')
def adminadd():
    return render_template('admin-add.html')

@app.route('/admininsert', methods=['POST', 'GET'])
def admin_insert():
    if request.method == 'GET':
        my_from = request.args
        gen_time = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
        login_name = my_from['login_name']
        passwd = my_from['passwd']
        phone = my_from['phone']
        email = my_from['email']
        role = my_from['role']
        xjt = User(login_name=login_name, passwd=passwd, phone=phone, email=email, gen_time=gen_time, role=role )
        db.session.add(xjt)
        db.session.commit()
        print(xjt)
    return '200'

@app.route('/adminedit',methods=['POST', 'GET'])
def adminedit():
    if request.method == 'GET':
        params = request.args
        id = params.get('id')
        ret = User.query.get(id)
        return render_template('admin-edit.html',ret=ret)
    elif request.method == 'POST':
        my_from = request.form
        print(my_from)
        login_name = my_from['login_name']
        passwd = my_from['passwd']
        phone = my_from['phone']
        email = my_from['email']
        role = my_from['role']
        ret = User.query.filter_by(login_name=login_name).first()
        ret.passwd = passwd
        ret.phone = phone
        ret.email = email
        ret.role = role
        db.session.commit()
        print(ret)
        return '修改成功'
    else:
        return '方法不对'

@app.route('/admindel',methods=['POST', 'GET'])
def admindel():
    if request.method == 'GET':
        params = request.args
        id = params.get('id')
        db.session.query(User).filter(User.id == id ).delete()
        db.session.commit()
        return '删除成功'

if __name__=="__main__":
    app.run(host='0.0.0.0',port=6999,debug=True)


