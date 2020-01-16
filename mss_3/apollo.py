#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import json
from datetime import datetime
import time

urlApi = 'http://apollo.baofoo.com/'
appid= '187000001'
clusterName = ['default','baoxin']
token = '8daaa2b8d917003351dc869c47216799dc7d6b36'
namespaceName= ['application','OPERATION.mss-test','test']
headers= {'Content-Type':'application/json;charset=UTF-8','Authorization':f'{token}'}
# 添加配置的数据
data = {
    "key": "salt2",
    "value": "192.168.101.66",
    "comment": "鹏博士salt服务器",
    "dataChangeCreatedBy": "admin"
}
today_time = datetime.now().strftime('%Y%m%d%H%M%S')
# 发布配置的数据
data1 = {
    "releaseTitle": f"{today_time}-release",
    "releaseComment": "api生产发布",
    "releasedBy": "admin"
}
# 创建namespace的数据
data2 = {
    "name" :'mss20190830',
    "appId" :f'{appid}',
    "format": 'properties',
    "isPublic": True,
    "comment": 'default app namespace',
    "dataChangeCreatedBy": 'admin',

}
# 修改配置的数据
key1 = {
    "key": "salt1",
    "value": "192.168.101.127",
    "comment": "salt服务器",
    "dataChangeLastModifiedBy": "admin"
}
# 查询所有配置
def queryNamespaces():
    url = f'{urlApi}openapi/v1/envs/dev/apps/{appid}/clusters/{clusterName[1]}/namespaces'
    response=requests.get(url,headers=headers)
    apollo_dict= response.json()
    print(apollo_dict)
    return apollo_dict

# 新增namespace
def addNamespaces(data):
    url = f'{urlApi}openapi/v1/apps/{appid}/appnamespaces'
    print(url)
    print(json.dumps(data))  # 字典转json格式
    response = requests.post(url ,data=json.dumps(data), headers=headers)
    apollo_dict = response.json()
    print(apollo_dict)
    return apollo_dict

# 新增namespace配置
def addConfig(data):
    url = f'{urlApi}openapi/v1/envs/dev/apps/{appid}/clusters/{clusterName[1]}/namespaces/{namespaceName[0]}/items'
    print(url)
    print(json.dumps(data))  # 字典转json格式
    response = requests.post(url ,data=json.dumps(data), headers=headers)
    apollo_dict = response.json()
    print(apollo_dict)
    return apollo_dict

# 修改namespace配置
def updateConfig(data):
    url = f'{urlApi}openapi/v1/envs/dev/apps/{appid}/clusters/{clusterName[1]}/namespaces/{namespaceName[0]}/items/salt1'
    print(url)
    print(json.dumps(data))  # 字典转json格式
    response = requests.put(url ,data=json.dumps(data), headers=headers)
    print(response)
    return response

# 发布namespace配置
def releasesConfig(data):
    url = f'{urlApi}openapi/v1/envs/dev/apps/{appid}/clusters/{clusterName[1]}/namespaces/{namespaceName[0]}/releases'
    print(url)
    print(json.dumps(data))  # 字典转json格式
    response = requests.post(url ,data=json.dumps(data), headers=headers)
    apollo_dict = response.json()
    print(apollo_dict)
    return apollo_dict

# addConfig(data)
releasesConfig(data1)