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

from scripts.path_constants import CONFIG_USER, CONFIG_MYSQL


class Handle_Re:

    # 不存在手机号的参数化信息
    unregistered_mobilePhone = r"\${unregistered_mobilephone}"

    # 存在手机号的参数化信息
    investors_mobilePhone = r'\${investors_login_mobile}'

    do_config = HandleConfig(CONFIG_USER)

    @classmethod
    def not_existed_replace(cls, data):
        '''
            不存在手机号进行参数化
        '''
        if re.search(cls.unregistered_mobilePhone, data):
            do_mysql = HandleMysql()
            data = re.sub(cls.unregistered_mobilePhone, do_mysql.create_not_existed_mobile(), data)
            do_mysql.close()
        return data

    @classmethod
    def have_existed_replace(cls, data):
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
        data = cls.not_existed_replace(data)
        data = cls.have_existed_replace(data)
        return data


if __name__ == '__main__':
    do_re = Handle_Re()
    one = do_re.register_user_mobile_replace('{"mobilephone": "${unregistered_mobilephone}","pwd":"123456","regname":"www"}')
    print(one)
    two = do_re.register_user_mobile_replace('{"mobilephone": "${investors_login_mobile}","pwd": "123456789","regname": "test_rabbit"}')
    print(two)
    pass

