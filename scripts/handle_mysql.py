# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/24 下午3:04
 @File : handle_mysql.py
 @IDE  : PyCharm
------------------------------------
'''

import pymysql

import random

import re

from scripts.path_constants import CONFIG_MYSQL

from scripts.handle_config import HandleConfig


class HandleMysql:
    '''
        PyMysql 的封装类
    '''

    def __init__(self):
        # 创建配置文件对象
        self.config = HandleConfig(CONFIG_MYSQL)
        # 读取配置文件的内容
        # self.config.read(CONFIG_MYSQL, encoding='utf-8')
        # 获取配置文件的内容
        section = 'mysql'
        # 创建数据库连接
        self.connect = pymysql.connect(host=self.config.get_value(section, 'mysql_host'),
                                       user=self.config.get_value(section, 'mysql_user'),
                                       password=self.config.get_value(section, 'mysql_password'),
                                       db=self.config.get_value(section, 'mysql_db'),
                                       port=self.config.get_int(section, 'mysql_port'),
                                       charset='utf8',
                                       cursorclass=pymysql.cursors.DictCursor)
        # 创建游标对象
        self.cursor = self.connect.cursor()

    # sql语句执行方法
    def do_execute(self, sql, args=None, is_one_data=True):
        '''
            @sql : 传入要执行的sql语句
            @args: sql语句有占位符需传入其他参数
            @is_one_data: sql语句查询的是否是单条数据,默认为True
        '''
        # 执行传入的sql语句,和可变参数
        self.cursor.execute(sql, args=args)
        # 提交要执行的sql语句对数据库进行操作
        self.connect.commit()
        # 如果is_one_data为True,则代表该sql语句会返回一条数据
        if is_one_data:
            # 则 fetchone 返回执行sql语句后的数据
            return self.cursor.fetchone()
        # 如果is_one_data为True,则代表该sql语句返回的数据不止为一条
        else:
            # 则 fetchall 返回执行sql语句后的所有数据
            return self.cursor.fetchall()

    @staticmethod
    def create_mobile():
        '''
            创建手机号码的静态类
        '''
        # 定义一些3位数开头的手机号码
        head_number = ['130', '131', '132', '138', '139', '150', '159',  '176', '185']
        # 调用 random.choice() 方法在 head_number 列表中随机选择一个
        head_mobile_number = random.choice(head_number)
        # 调用 random.sample() 方法在0-9中随机出8个数字
        other_mobile_number = random.sample('0123456789', 8)
        # 将选出的号码开头和随机出的8个数字进行组合,生成一个手机号码
        mobile_number = head_mobile_number+''.join(other_mobile_number)
        # 并将该手机号码返回
        return mobile_number

    def is_existed_mobile(self, mobile):
        '''
            判断手机号码是否存在的方法
        '''
        # 定义一个查询号码的sql语句
        sql = "SELECT * FROM member WHERE MobilePhone = %s;"
        # 调用 do_execute() 方法来执行该sql语句,获取查询的结果
        # 如果返回的是个字典,就代表已经注册,返回True
        if self.do_execute(sql, args=(mobile,)):
            return True
        # 返回None就代表还没有注册,返回False
        else:
            return False

    def create_not_existed_mobile(self):
        '''
            创建一个不存在的手机号码
        '''
        # 进行一个 while 循环,来生成手机号
        while True:
            # mobile 接收调用 create_mobile() 方法返回的手机号码
            mobile = self.create_mobile()
            # 调用 is_existed_mobile(mobile) 来判断创建的手机号是否存在
            if not self.is_existed_mobile(mobile):
                # 如果不存在,将 break 跳出循环
                break
        # 并将该手机号码插入到数据库中
        # 准备好插入的sql语句
        '''
            sql = "INSERT INTO `future`.`member`(`Id`," \
              " `RegName`," \
              " `Pwd`," \
              " `MobilePhone`," \
              " `Type`," \
              " `LeaveAmount`) VALUES (1," \
              " 'want'," \
              " 'want'," \
              " %s," \
              " 1," \
              " 0)"
        '''
        return mobile

    # 关闭方法
    def close(self):
        # 先关闭游标对象
        self.cursor.close()
        # 接着关闭与数据库的连接
        self.connect.close()


if __name__ == '__main__':
    # do = HandleMySql(scripts.path_constants.CONFIG_MYSQL)
    # sql = "select * from member Where mobilephone = '17777788888'"
    # print(do.do_execute(sql))
    # do.close()

    # do = HandleMySql(scripts.path_constants.CONFIG_MYSQL)
    # do.is_existed_mobile()

    do = HandleMysql()
    # print('不存在的手机号码为：{}'.format(do.create_not_existed_mobile()))
    # do.create_mobile()
    do.is_existed_mobile('17777788888')
    do.create_not_existed_mobile()
    pass
