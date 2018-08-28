import sqlite3
import pandas as pd

conn=sqlite3.connect('%s' %'.../MM.sqlite') #连接数据库
cur=conn.cursor()
query = "SELECT name FROM sqlite_master WHERE type='table' order by name" #查询所有表名

a = pd.read_sql(query, conn)

result = []
for i in a.name: #开始遍历所有表查找女票(的聊天记录)藏身之处
    query3 = "SELECT * FROM %s" %(i)
    r = pd.read_sql(query3, conn)
    if 'Message' in r.columns:
        for j in r.Message:
            if 'xxxxxx' in j: #注1，关键的一步
                result.append(i)

query4 = "SELECT * FROM %s" %(result[0]) #注1那步完成得好，result就会只有一个元素
text = pd.read_sql(query4, conn)
text = list(text.Message) #注2

full_text = '\n'.join(text) #将text这个列表合并成字符串，以回车符分隔
f = open('.../聊天记录.txt', 'w')
f.write(full_text)
f.close()
