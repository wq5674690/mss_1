#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from flask import  render_template
from flask import Flask
from app.main.views import *
from app.app01.views import *
from app.app02.views import *
import pymysql
import pymysql.cursors
app = Flask(__name__,static_url_path='')
app.register_blueprint(main,url_prefix='/main')
app.register_blueprint(app01,url_prefix='/app01')
app.register_blueprint(app02,url_prefix='/app02')

app.config.from_object(config)
db = SQLAlchemy(app=app)

# @app.route('/')
@app.route('/login')
@app.route('/login.html')
def login():
    return render_template('login.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__=='__main__':
  app.run(host='0.0.0.0',port=5001,debug=True)