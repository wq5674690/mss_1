#!/usr/bin/python3
# -*- coding: utf-8 -*-
from blog2 import app

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
