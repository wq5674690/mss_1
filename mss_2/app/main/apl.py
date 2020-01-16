#!/usr/bin/python3
# -*- coding: UTF-8 -*-


import os

class apolloF:
    # def __init__(self, db_name, w_url, r_url, w_user, r_user, w_passwd, r_passwd, str_date=None):
    def __init__(self, dict):
        self.__db_name = dict['ap_db_name']
        self.__w_url = dict['ap_w_url']
        self.__w_user = dict['ap_w_user']
        self.__w_passwd = dict['ap_w_passwd']
        self.__r_url = dict['ap_r_url']
        self.__r_user = dict['ap_r_user']
        self.__r_passwd = dict['ap_r_passwd']
        self.__str_date = dict['ap_str_date']


    def dbFormart(self, db_name):
        str1 = db_name
        str2 = str1.lower()
        str3 = str2.replace('_', '.')
        return str3

    def af(self):
        start_str = '''
库名.db.driver=com.mysql.jdbc.Driver<br>
库名.db.write.url=写库url<br>
库名.db.write.username=写库用户名<br>
库名.db.write.password=写库密码<br>
库名.db.read.url=读库url<br>
库名.db.read.username=读库用户名<br>
库名.db.read.password=读库密码<br>
库名.db.initialPoolSize=1<br>
库名.db.minPoolSize=1<br>
库名.db.maxPoolSize=20<br>
库名.db.acquireIncrement=5<br>
库名.db.idleConnectionTestPeriod=60<br>
库名.db.maxIdleTime=180<br>
库名.db.maxStatements=0<br>
库名.db.connectionTimeout=500<br>
库名.db.idleTimeout=600000<br>
库名.db.maxLifetime=1800000<br>
库名.db.connectionTestQuery=SELECT 1 FROM DUAL<br>
            '''
        str1 = start_str.replace('库名', self.dbFormart(self.__db_name))
        str2 = str1.replace('写库url', ("jdbc:mysql://%s:3306/%s%s") % (self.__w_url, self.__db_name, self.__str_date))
        str3 = str2.replace('写库用户名', self.__w_user)
        str4 = str3.replace('写库密码', self.__w_passwd)
        str5 = str4.replace('读库url', ("jdbc:mysql://%s:3306/%s%s") % (self.__r_url, self.__db_name, self.__str_date))
        str6 = str5.replace('读库用户名', self.__r_user)
        str7 = str6.replace('读库密码', self.__r_passwd)
        return str7

def  main():
    str = {
        'ap_id':'1',
        'ap_date_time':'',
        'ap_env':'test',
        'ap_db_name':'CIF_OMS',
        'ap_w_url':'bx-cif-w',
        'ap_w_user':'cif123_w',
        'ap_w_passwd':'abc123456_w',
        'ap_r_url':'bx-cif-r',
        'ap_r_user':'oms123_r',
        'ap_r_passwd':'cba123456_r',
        'ap_str_date':'?useSSL=false',
    }
    str2 = apolloF(str)
    print('OPERATION.' + str['ap_db_name'],end='')
    print(str2.af())

if __name__ == '__main__':
    main()