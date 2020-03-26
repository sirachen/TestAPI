# -*- coding: utf-8 -*-
#  @Time    : 2019/8/8 16:54
#  @Author  : Anonymous
#  @File    : handle_parametric.py
import re
import os
from scripts.handle_mysql import HandleMySQL
from scripts.handle_config import HandleConfig
from scripts.handle_path_constants import CONFIGS_DIR


class HandleParametric:
    '''Excel用例中的变量参数化设计'''
    '''未注册手机号参数化模式'''
    unregistered_mobile_pattern = r"\${unregistered_mobilephone}"
    '''投资人账号参数化模式'''
    # 投资人手机号
    investors_login_mobile_pattern = r'\${investors_login_mobile}'
    # 投资人密码
    investors_login_pwd_pattern = r'\${investors_login_pwd}'
    # 投资人的memberId
    investors_member_id_pattern = r'\${investors_member_id}'
    '''借款人账号参数化模式'''
    # 借款人账号
    borrower_login_mobile_pattern = r'\${borrower_login_mobile}'
    # 借款人密码
    borrower_login_pwd_pattern = r'\${borrower_login_pwd}'
    # 借款人的memberId
    borrower_member_id_pattern = r'\${borrower_member_id}'
    '''审核员账号参数化模式'''
    # 审核员账号
    auditor_login_mobile_pattern = r'\${auditor_login_mobile}'
    # 审核员密码
    auditor_login_pwd_pattern = r'\${auditor_login_pwd}'
    # 审核员的memberId
    auditor_member_id_pattern = r'\${auditor_member_id}'
    '''loanId参数化'''
    loan_id_pattern = r'\${loan_id_pattern}'

    # 创建HandleMySQL()实例对象,创建数据库连接
    do_mysql = HandleMySQL()
    # 创建配置文件config.ini所在路径
    handle_config = HandleConfig(os.path.join(CONFIGS_DIR, 'config.ini'))
    # 创建配置文件account_information.ini所在路径
    handle_account_config = HandleConfig(os.path.join(CONFIGS_DIR, 'account_information.ini'))

    @classmethod
    def generate_unregistered_mobile_number(cls, data):
        '''
        生成未注册的手机号参数化
        :param data: 调用该方法时传入的带有需要进行参数化的手机号的请求数据
        :return:替换成含有程序随机生成的手机号的请求数据data
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.unregistered_mobile_pattern, data):
            # 创建数据库连接
            cls.do_mysql.__init__()
            # 将随机生成的手机号码进行替换操作后，再返回的值赋值给data
            data = re.sub(cls.unregistered_mobile_pattern, cls.do_mysql.generate_unregistered_phone_number(), data)
            # 关闭数据库连接
            cls.do_mysql.close_mysql()
        return data

    @classmethod
    def investors_mobile(cls, data):
        '''
        匹配investors的手机号进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.investors_login_mobile_pattern, data):
            # 对正常登录接口的手机号替换为账户信息account_information.ini中投资人account_investors的手机号
            data = re.sub(cls.investors_login_mobile_pattern,
                          cls.handle_account_config.get_value('account_investors', 'mobilephone'), data)
        return data

    @classmethod
    def investors_pwd(cls, data):
        '''
        匹配investors的密码进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.investors_login_pwd_pattern, data):
            # 对正常登录接口的密码替换为账户信息account_information.ini中投资人account_investors的密码
            data = re.sub(cls.investors_login_pwd_pattern,
                          cls.handle_account_config.get_value('account_investors', 'pwd'), data)
        return data

    @classmethod
    def investors_member_id(cls, data):
        '''
        匹配investors的memberId进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.investors_member_id_pattern, data):
            # 对正常登录接口的密码替换为账户信息account_information.ini中投资人account_investors的密码
            data = re.sub(cls.investors_member_id_pattern,
                          cls.handle_account_config.get_value('account_investors', 'id'), data)
        return data

    @classmethod
    def borrower_mobile(cls, data):
        '''
        匹配borrower的手机号进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.borrower_login_mobile_pattern, data):
            # 对正常登录接口的手机号替换为账户信息account_information.ini中投资人account_borrower的手机号
            data = re.sub(cls.borrower_login_mobile_pattern,
                          cls.handle_account_config.get_value('account_borrower', 'mobilephone'), data)
        return data

    @classmethod
    def borrower_pwd(cls, data):
        '''
        匹配borrower的密码进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.borrower_login_pwd_pattern, data):
            # 对正常登录接口的密码替换为账户信息account_information.ini中投资人account_borrower的密码
            data = re.sub(cls.borrower_login_pwd_pattern,
                          cls.handle_account_config.get_value('account_borrower', 'pwd'), data)
        return data

    @classmethod
    def borrower_member_id(cls, data):
        '''
        匹配borrower的memberId进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.borrower_member_id_pattern, data):
            # 对正常登录接口的密码替换为账户信息account_information.ini中投资人account_investors的密码
            data = re.sub(cls.borrower_member_id_pattern,
                          cls.handle_account_config.get_value('account_borrower', 'id'), data)
        return data

    @classmethod
    def auditor_mobile(cls, data):
        '''
        匹配auditor的手机号进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.auditor_login_mobile_pattern, data):
            # 对正常登录接口的手机号替换为账户信息account_information.ini中投资人account_borrower的手机号
            data = re.sub(cls.auditor_login_mobile_pattern,
                          cls.handle_account_config.get_value('account_auditor', 'mobilephone'), data)
        return data

    @classmethod
    def auditor_pwd(cls, data):
        '''
        匹配auditor的密码进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.auditor_login_pwd_pattern, data):
            # 对正常登录接口的密码替换为账户信息account_information.ini中投资人account_borrower的密码
            data = re.sub(cls.auditor_login_pwd_pattern,
                          cls.handle_account_config.get_value('account_auditor', 'pwd'), data)
        return data

    @classmethod
    def auditor_member_id(cls, data):
        '''
        匹配auditor的memberId进行参数化
        :return:
        '''
        # 先通过re.search()去data中查找，若找到参数化模式就开始进行替换操作
        if re.search(cls.auditor_member_id_pattern, data):
            # 对正常登录接口的密码替换为账户信息account_information.ini中投资人account_investors的密码
            data = re.sub(cls.auditor_member_id_pattern,
                          cls.handle_account_config.get_value('account_auditor', 'id'), data)
        return data

    @classmethod
    def loan_id(cls, data):
        if re.search(cls.loan_id_pattern, data):
            borrower_loan_Id = str(getattr(HandleParametric, 'loan_Id'))
            data = re.sub(cls.loan_id_pattern, borrower_loan_Id, data)
        return data

    '''接口参数化相关方法'''
    @classmethod
    def to_register_parameter(cls, data):
        '''
        注册接口批量参数化方法
        :param data: 传入的需要进行替换的请求数据data
        :return: 返回参数化替换完成的请求数据data
        '''
        # 注册接口中MobilePhone参数化
        data = cls.generate_unregistered_mobile_number(data=data)
        # 重复注册接口中MobilePhone参数化
        data = cls.investors_mobile(data=data)
        return data

    @classmethod
    def to_login_parameter(cls, data):
        '''
        登录、充值接口批量参数化方法
        :param data: 传入的需要进行替换的请求数据data
        :return: 返回参数化替换完成的请求数据data
        '''
        # 登录接口中MobilePhone参数化
        data = cls.investors_mobile(data=data)
        # 登录接口中pwd参数化
        data = cls.investors_pwd(data=data)
        return data

    @classmethod
    def to_add_parameter(cls, data):
        '''
        新增项目接口批量参数化方法
        :param data: 传入的需要进行替换的请求数据data
        :return: 返回参数化替换完成的请求数据data
        '''
        # 登录接口中MobilePhone参数化
        data = cls.borrower_mobile(data=data)
        # 登录接口中pwd参数化
        data = cls.borrower_pwd(data=data)
        # 新增项目时memberId参数化
        data = cls.borrower_member_id(data=data)
        return data

    @classmethod
    def to_invest_parameter(cls, data):
        '''
        投标接口批量参数化方法
        :param data: 传入的需要进行替换的请求数据data
        :return: 返回参数化替换完成的请求数据data
        '''
        # 投标接口中审核员MobilePhone参数化
        data = cls.auditor_mobile(data=data)
        # 投标接口中审核员pwd参数化
        data = cls.auditor_pwd(data=data)
        # 新增项目时memberId参数化
        data = cls.auditor_member_id(data=data)
        # 投标接口中项目loanId参数化
        data = cls.loan_id(data=data)
        # 投标接口中投资人投标时memberId参数化
        data = cls.investors_member_id(data=data)
        # 投标接口中投资人投标时memberId参数化
        data = cls.investors_pwd(data=data)
        return data


# if __name__ == '__main__':
    # test = HandleParametric()
    # data1 = "{'mobilephone': '${unregistered_mobilephone}', 'pwd': '123456789', 'regname': 'test_rabbit'}"
    # data2 = "{'mobilephone': '${unregistered_mobilephone}', 'pwd': '123456789', 'regname': 'test_rabbit'}"
    # data3 = "{'mobilephone': '${repeat_registration}', 'pwd': '123456789', 'regname': 'test_rabbit'}"
    # data4 = "{'mobilephone': '17611642608', 'pwd': '123456789', 'regname': 'test_rabbit'}"
    # print(test.to_parameter(data1))
    # print(test.to_parameter(data2))
    # print(test.to_parameter(data3))
    # print(test.to_parameter(data4))
