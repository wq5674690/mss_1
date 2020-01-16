#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask
import pymysql.cursors
import importlib,sys
importlib.reload(sys)
#
# '''配置数据库'''
app = Flask(__name__)

'''MySQL漫道云配置'''
# mysql_config = {
#     'host': '10.254.66.9',
#     'port': 3306,
#     'user': 'root',
#     'password': 'baofoo@64',#密码1
#     'db': 'test',
#     'charset': 'utf8',
#     'cursorclass': pymysql.cursors.DictCursor,
# }

'''MySQL本地配置'''
mysql_config = {
    # 'host': '127.0.0.1',
    'host': 'mysql.mss.com',
    'port': 3306,
    'user': 'root',
    'password': '123456',#密码1
    'db': 'test',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}


SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['db']}?{mysql_config['charset']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_TEARDOWN = True
