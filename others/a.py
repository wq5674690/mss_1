#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re

with open("a") as file:
    for line in file.readlines():
        line = line.strip()

        print(line)

        # if "2" not in line:
        #     print ('test')
        #     continue
        # app, ip = re.split("-2|_2", line, maxsplit=1)
        #
        # print(app, "192.168.2"+ip)