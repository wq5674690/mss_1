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


'''salt配置'''
salt_config = {
        'v11': {'url': "http://192.168.33.50:8000", 'user': "jenkins", 'password': "baofoo@64"},
        'v12': {'url': "http://192.168.100.66:8000", 'user': "admin", 'password': "Baofoo@2017"},
        'v13': {'url': "http://172.20.50.20:8000", 'user': "jenkins", 'password': "oQBqo@AZJcFhuceF"},
        'v14': {'url': "http://192.168.101.66:8000", 'user': "jenkins", 'password': "baofoo@64"},
        'v15': {'url': "http://10.0.19.89:8000", 'user': "admin", 'password': "baofoo@64"},
    }


'''MySQL配置'''
mysql_config = {
    'host': '10.254.66.9',
    'port': 3306,
    'user': 'root',
    'password': 'baofoo@64',#密码1
    'db': 'test',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{mysql_config['user']}:{mysql_config['password']}@{mysql_config['host']}:{mysql_config['port']}/{mysql_config['db']}?{mysql_config['charset']}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_TEARDOWN = True
