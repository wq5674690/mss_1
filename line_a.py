#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
with open("line_a") as file:
    line_a = [item.strip('\n') for item in file.readlines()]
    # for line_a in file.readlines():
        # line_a = line_a.strip()
        # str_a[] = line_a
        # print(line_a)
        # print(str_a)
        # print(line_a)
    # print("====分隔线==")
# line_a = line_a.split('\n')

with open("line_b") as file:
    line_b = [item.strip('\n') for item in file.readlines()]
    # for line_b in file.readlines():
    #     line_b = line_b.strip()
    #     # str_b[] = line_b
    #     # print(line_b)
    # print("====分隔线==")
with open("line_c") as file:
    line_c = [item.strip('\n') for item in file.readlines()]
    # for line_c in file.readlines():
    #     line_c = line_c.strip()
        # print(line_c)
        # str_c[] = line_c
for a in line_a:
    if a in line_b and a in line_c:
        print(a + '#这是准生产')
    else:
        print(a + '#这是生产')

# print(line_a)
# print(line_b)
# print(line_c)