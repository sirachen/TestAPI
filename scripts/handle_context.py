# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/26 下午6:27
 @File : handle_context.py
 @IDE  : PyCharm
------------------------------------
'''

import re

from scripts.handle_mysql import HandleMysql

from scripts.handle_config import HandleConfig

from scripts.path_constants import CONFIG_USER


class Handle_Re:

    # 注册不存在手机号的参数化信息
    unregistered_mobilePhone = r"\${unregistered_mobilephone}"

    # 注册存在手机号的参数化信息
    investors_mobilePhone = r"\${investors_login_mobile}"

    # 登录已存在手机号的参数化信息
    # investors_login_mobile = r'\${investors_login_mobile}'
    # 登录已存在手机号密码的参数化信息
    investors_login_pwd = r"\${investors_login_pwd}"

    do_config = HandleConfig(CONFIG_USER)

    @classmethod
    def register_not_existed_replace(cls, data):
        '''
            不存在手机号进行参数化
        '''
        if re.search(cls.unregistered_mobilePhone, data):
            do_mysql = HandleMysql()
            data = re.sub(cls.unregistered_mobilePhone, do_mysql.create_not_existed_mobile(), data)
            do_mysql.close()
        return data

    @classmethod
    def register_have_existed_replace(cls, data):
        '''
            存在手机号进行参数化
        '''
        # if re.search(cls.investors_mobilePhone, data):
        #     do_mysql = HandleMysql()
        #     do_config = HandleConfig(CONFIG_MYSQL)
        #     sql = do_config.get_value('mysql', 'search_one_mobile')
        #     have_number = do_mysql.do_execute(sql=sql)
        #     if have_number:
        #         data = re.sub(cls.investors_mobilePhone,
        #                       have_number['MobilePhone'],
        #                       data)
        #     else:
        #         do_mysql.create_not_existed_mobile()
        #         cls.have_existed_replace(data)
        #     do_mysql.close()
        if re.search(cls.investors_mobilePhone, data):
            invest_user_mobile = cls.do_config.get_value('invest_user', 'mobile')
            data = re.sub(cls.investors_mobilePhone, invest_user_mobile, data)
        return data

    @classmethod
    def register_user_mobile_replace(cls, data):
        data = cls.register_not_existed_replace(data)
        data = cls.register_have_existed_replace(data)
        return data

    @classmethod
    def login_have_existed_mobile_replace(cls, data):
        if re.search(cls.investors_mobilePhone, data):
            invest_mobile = cls.do_config.get_value('invest_user', 'mobile')
            data = re.sub(cls.investors_mobilePhone, invest_mobile, data)
        return data

    @classmethod
    def login_have_existed_pwd_replace(cls, data):
        if re.search(cls.investors_login_pwd, data):
            invest_pwd = cls.do_config.get_value('invest_user', 'pwd')
            data = re.sub(cls.investors_login_pwd, invest_pwd, data)
        return data

    @classmethod
    def login_user_mobile_pwd_replace(cls, data):
        data = cls.login_have_existed_mobile_replace(data)
        data = cls.login_have_existed_pwd_replace(data)
        return data


if __name__ == '__main__':
    # do_re = Handle_Re()
    # one = do_re.register_user_mobile_replace('{"mobilephone": "${unregistered_mobilephone}","pwd":"123456","regname":"www"}')
    # print(one)
    # two = do_re.register_user_mobile_replace('{"mobilephone": "${investors_login_mobile}","pwd": "123456789","regname": "test_rabbit"}')
    # print(two)
    # three = do_re.login_user_mobile_pwd_replace('{"mobilephone":"${investors_login_mobile}","pwd":"${investors_login_pwd}"}')
    # print(three)
    pass

