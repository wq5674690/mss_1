#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask

'''配置数据库'''
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Fianna'
# 这里登陆的是root用户，要填上自己的密码，MySQL的默认端口是3306，填上之前创建的数据库名jianshu,连接方式参考 \
# http://docs.sqlalchemy.org/en/latest/dialects/mysql.html
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/test'
# 设置这一项是每次请求结束后都会自动提交数据库中的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 实例化
db = SQLAlchemy(app)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False, server_default='', unique=True)
    def __repr__(self):
        return '<Role %r>' % self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), nullable=False, unique=True, server_default='', index=True)
    role_id = db.Column(db.Integer, nullable=False, server_default='0')
    def __repr__(self):
        return '<User %r,Role id %r>' %(self.username,self.role_id)