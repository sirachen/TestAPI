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
    # 注册接口:不存在手机号的参数化信息
    register__unregistered_mobile = r"\${unregistered_mobile}"
    # 注册接口:存在手机号的参数化信息
    register__investors_mobile = r"\${investors_login_mobile}"

    # 登录接口:已存在手机号的参数化信息
    login__investors_login_mobile = r"\${investors_login_mobile}"
    # 登录接口:已存在手机对应的密码的参数化信息
    login__investors_login_pwd = r"\${investors_login_pwd}"

    # 充值接口:已存在手机号码参数化信息
    recharge__investors_login_mobile = r"\${investors_login_mobile}"
    # 充值接口:已存在手机对应的密码的参数化信息
    recharge__investors_login_pwd = r"\${investors_login_pwd}"

    # 加标接口:管理员手机号码参数化信息
    add__borrower_login_mobile = r"\${borrower_login_mobile}"
    # 加标接口:管理员密码参数化信息
    add__borrower_login_pwd = r"\${borrower_login_pwd}"
    # 加标接口:借款人id参数化信息
    add__borrower_member_id = r"\${borrower_member_id}"

    # 投资接口:管理员手机号参数化信息
    invest__admin_login_mobile = r"\${admin_login_mobile}"
    # 投资接口:管理员密码参数化信息
    invest__admin_login_pwd = r"\${admin_login_pwd}"
    # 投资接口:借款人ID
    invest__borrow_member_id = r"\${borrow_id}"
    # 投资接口:标ID参数化信息
    invest__loan_id = r"\${loan_id}"
    # 投资接口:投资人id
    invest__investors_id = r"\${investors_login_id}"
    # 投资接口:投资人密码
    invest__investors_pwd = r"\${investors_login_pwd}"

    do_config = HandleConfig(CONFIG_USER)

    @classmethod
    def register_not_existed_replace(cls, data):
        '''
            不存在手机号进行参数化
        '''
        if re.search(cls.register__unregistered_mobile, data):
            do_mysql = HandleMysql()
            data = re.sub(cls.register__unregistered_mobile, do_mysql.create_not_existed_mobile(), data)
            do_mysql.close()
        return data

    @classmethod
    def register_have_existed_replace(cls, data):
        '''
            存在手机号进行参数化
        '''
        if re.search(cls.register__investors_mobile, data):
            invest_user_mobile = cls.do_config.get_value('invest_user', 'mobile')
            data = re.sub(cls.register__investors_mobile, invest_user_mobile, data)
        return data

    @classmethod
    def register_parameterization(cls, data):
        # 注册参数化
        data = cls.register_not_existed_replace(data)
        data = cls.register_have_existed_replace(data)
        return data

    @classmethod
    def login_have_existed_mobile_pwd_replace(cls, data):
        if re.search(cls.login__investors_login_mobile, data):
            invest_mobile = cls.do_config.get_value('invest_user', 'mobile')
            data = re.sub(cls.login__investors_login_mobile, invest_mobile, data)
        if re.search(cls.login__investors_login_pwd, data):
            invest_pwd = cls.do_config.get_value('invest_user', 'pwd')
            data = re.sub(cls.login__investors_login_pwd, invest_pwd, data)
        return data

    @classmethod
    def login_parameterization(cls, data):
        # 登录参数化
        data = cls.login_have_existed_mobile_pwd_replace(data)
        return data

    @classmethod
    def recharge_have_existed_mobile_pwd_replace(cls, data):
        if re.search(cls.recharge__investors_login_mobile, data):
            invest_mobile = cls.do_config.get_value('invest_user', 'mobile')
            data = re.sub(cls.recharge__investors_login_mobile, invest_mobile, data)
        if re.search(cls.recharge__investors_login_pwd, data):
            invest_pwd = cls.do_config.get_value('invest_user', 'pwd')
            data = re.sub(cls.recharge__investors_login_pwd, invest_pwd, data)
        return data

    @classmethod
    def recharge_parameterization(cls, data):
        # 充值参数化
        data = cls.recharge_have_existed_mobile_pwd_replace(data)
        return data

    @classmethod
    def add_admin_user_mobile_pwd_replace(cls, data):
        '''
            加标:对管理员手机号码和密码进行参数化
        '''
        # 在传入的data数据中查找是否存在 borrower_login_mobile = r"\${borrower_login_mobile}" 的内容
        if re.search(cls.add__borrower_login_mobile, data):
            # 获取管理员的手机号码
            borrow_admin_user_mobile = cls.do_config.get_value('admin_user', 'mobile')
            # 对传入的data数据进行参数化, 在 data 数据里把 cls.borrower_login_mobile 的内容修改为 borrow_admin_user_mobile
            data = re.sub(cls.add__borrower_login_mobile, borrow_admin_user_mobile, data)
        # 在传入的data数据中查找是否存在 borrower_login_pwd = r"\${borrower_login_pwd}" 的内容
        if re.search(cls.add__borrower_login_pwd, data):
            # 获取管理员的密码
            borrow_admin_user_pwd = cls.do_config.get_value('admin_user', 'pwd')
            # 对传入的data数据进行参数化, 在 data 数据里把 cls.borrower_login_pwd 的内容修改为 borrow_admin_user_pwd
            data = re.sub(cls.add__borrower_login_pwd, borrow_admin_user_pwd, data)
        # 把最后参数化的内容返回
        return data

    @classmethod
    def add_borrow_id_replace(cls, data):
        '''
            加标:对借款人id进行参数化
        '''
        if re.search(cls.add__borrower_member_id, data):
            borrow_user_id = cls.do_config.get_value('borrow_user', 'user_id')
            data = re.sub(cls.add__borrower_member_id, borrow_user_id, data)
        return data

    @classmethod
    def add_parameterization(cls, data):
        # 管理员信息:手机号码和密码参数化
        data = cls.add_admin_user_mobile_pwd_replace(data)
        # 借款人信息:id参数化
        data = cls.add_borrow_id_replace(data)
        return data

    @classmethod
    def invest_admin_user_mobile_pwd_replace(cls, data):
        if re.search(cls.invest__admin_login_mobile, data):
            exists_admin_mobile = cls.do_config.get_value('admin_user', 'mobile')
            data = re.sub(cls.invest__admin_login_mobile, exists_admin_mobile, data)
        if re.search(cls.invest__admin_login_pwd, data):
            exists_admin_pwd = cls.do_config.get_value('admin_user', 'pwd')
            data = re.sub(cls.invest__admin_login_pwd, exists_admin_pwd, data)
        return data

    @classmethod
    def invest_borrow_id_replace(cls, data):
        if re.search(cls.invest__borrow_member_id, data):
            exists_borrow_id = cls.do_config.get_value('borrow_user', 'user_id')
            data = re.sub(cls.invest__borrow_member_id, exists_borrow_id, data)
        return data

    @classmethod
    def invest_investor_id_pwd_replace(cls, data):
        if re.search(cls.invest__investors_id, data):
            investor_id = cls.do_config.get_value('invest_user', 'user_id')
            data = re.sub(cls.invest__investors_id, investor_id, data)
        if re.search(cls.invest__investors_pwd, data):
            investor_pwd = cls.do_config.get_value('invest_user', 'pwd')
            data = re.sub(cls.invest__investors_pwd, investor_pwd, data)
        return data

    @classmethod
    def invest_loan_id_replace(cls, data):
        if re.search(cls.invest__loan_id, data):
            loan_id = str(getattr(Handle_Re, "loan_id"))
            data = re.sub(cls.invest__loan_id, loan_id, data)
        return data

    @classmethod
    def invest_parameterization(cls, data):
        data = cls.invest_admin_user_mobile_pwd_replace(data)
        data = cls.invest_borrow_id_replace(data)
        data = cls.invest_investor_id_pwd_replace(data)
        data = cls.invest_loan_id_replace(data)
        return data


if __name__ == '__main__':
    do_re = Handle_Re()
    one = do_re.register_parameterization('{"mobile": "${unregistered_mobile}", "pwd": "123456", "regname": ""}')
    print(one)
    # two = do_re.register_user_mobile('{"mobilephone": "${investors_login_mobile}","pwd": "123456789","regname": "test_rabbit"}')
    # print(two)
    # three = do_re.login_user_mobile_pwd('{"mobilephone":"${investors_login_mobile}","pwd":"${investors_login_pwd}"}')
    # print(three)
    # four = do_re.add_admin_user_mobile_pwd_borrow_id('{"memberId":"${borrower_member_id}","title":"测试新增项目","amount":"1000000","loanRate":"-14.0","loanTerm":"6","loanDateType":"0","repaymemtWay":"5","biddingDays":"8"}')
    # print(four)
    # five = do_re.invest_parameterization('{"memberId":"${borrow_id}","title":"borrower新增项目","amount":"1000000","loanRate":"18.0","loanTerm":"6","loanDateType":"0","repaymemtWay":"5","biddingDays":"8"}')
    # print(five)
    # six = do_re.invest_parameterization('{"mobilephone":"${admin_login_mobile}","pwd":"${admin_login_pwd}"}')
    # print(six)
    # seven = do_re.invest_parameterization('{"mobilephone":"${admin_login_mobile}","pwd":"${admin_login_pwd}"}')
    # print(seven)
    pass

