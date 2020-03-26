# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/26 下午6:27
 @File : handle_re.py
 @IDE  : PyCharm
------------------------------------
'''

import re

from scripts.handle_mysql import HandleMySql


class Handle_Re:

    # 不存在手机号的参数化信息
    unregistered_mobilephone = r'\${unregistered_mobilephone}'

    # 存在手机号的参数化信息
    registered_mobilephone = r'\${investors_login_mobile}'

    @classmethod
    def not_existed_replace(cls, data):
        '''
            不存在手机号进行参数化
        '''
        if re.search(cls.unregistered_mobilephone, data):
            do_mysql = HandleMySql()
            data = re.sub(cls.unregistered_mobilephone,
                          do_mysql.create_not_existed_mobile(),
                          data)
            do_mysql.close()
        return data

    @classmethod
    def have_existed_replace(cls, data):
        '''
            存在手机号进行参数化
        '''
        if re.search(cls.registered_mobilephone, data):
            do_mysql = HandleMySql()
            have_number = do_mysql.do_execute(sql='SELECT member.MobilePhone FROM member LIMIT 1')
            data = re.sub(cls.unregistered_mobilephone,
                          have_number,
                          data)
            do_mysql.close()
        return data


if __name__ == '__main__':
    do_re = Handle_Re()
    one = do_re.not_existed_replace('{"mobilephone":"${unregistered_mobilephone}","pwd":"123456","regname":"hahahha"}')
    print(one)
    # two = do_re.have_existed_replace('{"mobilephone": "${investors_login_mobile}", "pwd": "123456789", "regname": "test_rabbit"}')
    # print(two)