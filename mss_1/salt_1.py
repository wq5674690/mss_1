#!/usr/bin/python3
# _*_ coding:utf-8 _*_
import urllib,json
import urllib.request
import urllib.parse
import ssl
import importlib,sys
importlib.reload(sys)
# sys.setdefaultencoding('utf8')

ssl._create_default_https_context = ssl._create_unverified_context

class SaltAPI(object):
    __token_id = ''

    def __init__(self,dict1):

        self.__url = dict1['url']
        self.__user = dict1['user']
        self.__password = dict1['password']

    def token_id(self):
        """
            用户登陆和获取token
        :return:
        """
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.parse.urlencode(params)
        obj = urllib.parse.unquote(encode).encode('utf-8')
        content = self.postRequest(obj, prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError


    def postRequest(self,obj,prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}
        # headers = {'X-Auth-Token': self.__token_id,  'Content-type': 'application/json'}
        req = urllib.request.Request(url,obj,headers)
        opener = urllib.request.urlopen(req)
        content = json.loads(opener.read().decode('utf-8'))
        # print(obj)
        return content

    def list_all_key(self):
        """
            获取包括认证、未认证salt主机
        """

        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions, minions_pre

    def delete_key(self, node_name):
        '''
            拒绝salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.delete', 'match': node_name}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def accept_key(self,node_name):
        '''
            接受salt主机
        '''

        params = {'client': 'wheel', 'fun': 'key.accept', 'match': node_name}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret

    def salt_get_jid_ret(self,jid):
        """
            通过jid获取执行结果
        :param jid: jobid
        :return: 结果
        """
        params = {'client':'runner', 'fun':'jobs.lookup_jid', 'jid': jid}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def salt_running_jobs(self):
        """
            获取运行中的任务
        :return: 任务结果
        """
        params = {'client':'runner', 'fun': 'jobs.active'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def remote_noarg_execution_sigle(self, tgt, fun):
        """
            单台minin执行命令没有参数
        :param tgt: 目标主机
        :param fun:  执行模块
        :return: 执行结果
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # {'return': [{'salt-master': True}]}
        ret = content['return'][0]
        return ret

    def remote_execution_single(self, tgt, fun, arg):
        """
            单台minion远程执行，有参数
        :param tgt: minion
        :param fun: 模块
        :param arg: 参数
        :return: 执行结果
        """
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # {'return': [{'salt-master': 'root'}]}
        ret = content['return']
        return ret

    def remote_async_execution_module(self, tgt, fun, arg):
        """
            远程异步执行模块，有参数
        :param tgt: minion list
        :param fun: 模块
        :param arg: 参数
        :return: jobid
        """
        params = {'client': 'local_async', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # {'return': [{'jid': '20180131173846594347', 'minions': ['salt-master', 'salt-minion']}]}
        jid = content['return'][0]['jid']
        return jid

    def remote_execution_module(self, tgt, fun, arg=None):
        """
            远程执行模块，有参数
        :param tgt: minion list
        :param fun: 模块
        :param arg: 参数
        :return: dict, {'minion1': 'ret', 'minion2': 'ret'}
        """
        if arg:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        else:
            params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'expr_form': 'list'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        # print(content)
        # {'return': [{'salt-master': 'root', 'salt-minion': 'root'}]}
        ret = content['return'][0]
        return ret

    def salt_state(self, tgt, arg, expr_form):
        '''
        sls文件
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'state.sls', 'arg': arg, 'expr_form': expr_form}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

    def salt_alive(self, tgt):
        '''
        salt主机存活检测
        '''
        params = {'client': 'local', 'tgt': tgt, 'fun': 'test.ping'}
        obj = urllib.parse.urlencode(params).encode('utf-8')
        self.token_id()
        content = self.postRequest(obj)
        ret = content['return'][0]
        return ret

# if __name__ == '__main__':
#         # salt = SaltAPI(url="https://192.168.104.76:8000",user="salt-api",password="salt-api")
#         salt = SaltAPI({'url':"http://192.168.100.66:8000", 'user':"admin", 'password':"Baofoo@2017"})
#         minions, minions_pre = salt.list_all_key()
#         # 说明如果'expr_form': 'list',表示minion是以主机列表形式执行时，需要把list拼接成字符串，如下所示
#         minions = ['192.168.23.137']
#         # minions = '192.168.23.137'
#         # minions = '*'
#         hosts = map(str, minions)
#         salt_client = ",".join(hosts)
#         # salt_method = 'network.connect'
#         salt_method1 = 'cmd.run'
#         # salt_params = '192.168.90.13 26379'
#         # salt_params = ['192.168.90.14','26379']
#         salt_params1 = 'nc -w 3 192.168.90.13 -z 26379'
#         ret1 = salt.remote_execution_module(salt_client,salt_method1,salt_params1)
#         # ret1 = salt.remote_execution_module(salt_client,salt_method)
#         # ret2 = salt.salt_alive(salt_client)
#         print(ret1)
#         # print(ret2)
