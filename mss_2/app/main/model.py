#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *


class User(db.Model):  # 继承SQLAlchemy.Model对象，一个对象代表了一张表
    id= db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # id 整型，主键，自增，唯一
    login_name = db.Column(db.String(64), nullable = False)  # 名字 字符串长度为20
    passwd = db.Column(db.String(64), nullable = False)  # 名字 字符串长度为20
    phone = db.Column(db.String(20), nullable = False)  # 名字 字符串长度为20
    email = db.Column(db.String(64), nullable = False)  # 名字 字符串长度为20
    role = db.Column(db.String(64), nullable = False)  # 名字 字符串长度为20
    gen_time = db.Column(db.DateTime, nullable = False)
    state = db.Column(db.Boolean, default = False)  # 名字 字符串长度为20

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
