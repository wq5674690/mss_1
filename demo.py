#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import time
# sentence = "Dear I love you forever"
# for char in sentence.split():
#    allChar = []
#    for y in range(12, -12, -1):
#        lst = []
#        lst_con = ''
#        for x in range(-30, 30):
#             formula = ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3
#             if formula <= 0:
#                 lst_con += char[(x) % len(char)]
#             else:
#                 lst_con += ' '
#        lst.append(lst_con)
#        allChar += lst
#    print('\n'.join(allChar))
#    time.sleep(1)

# import numpy as np
# import matplotlib.pyplot as plt
#
# x = np.linspace(-8 , 8, 1024)
# y1 = 0.618*np.abs(x) - 0.8* np.sqrt(64-x**2)
# y2 = 0.618*np.abs(x) + 0.8* np.sqrt(64-x**2)
# plt.plot(x, y1, color = 'r')
# plt.plot(x, y2, color = 'r')
# plt.show()

import itchat
import re

itchat.login()
friends = itchat.get_friends(update=True)[0:]
tList = []
for i in friends:
    signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    tList.append(signature)

# 拼接字符串
text = "".join(tList)

# jieba分词
import jieba
wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)

# wordcloud词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import PIL.Image as Image
my_wordcloud = WordCloud(background_color="white", max_words=2000,
                         max_font_size=40, random_state=42,
                         font_path = '/Library/Fonts/Songti.ttc').generate(wl_space_split)

plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()