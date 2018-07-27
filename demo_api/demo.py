#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from flask import Flask  
from flask import request
from flask import redirect
from flask import jsonify
import json
import mysql

app = Flask(__name__)

@app.route('/',methods=['GET'])
def start():
    db = mysql.Mysql()
    return jsonify(db.queryData())

if __name__=="__main__":
    app.run(debug=True)
