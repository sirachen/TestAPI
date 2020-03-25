# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/24 下午3:04
 @File : handle_mysql.py
 @IDE  : PyCharm
------------------------------------
'''

from configparser import ConfigParser

import pymysql

import os

import scripts.path_constants


class HandleMySql:
    '''
        PyMysql 的封装类
    '''

    def __init__(self, filename):
        # 创建配置文件对象
        config = ConfigParser()
        # 读取配置文件的内容
        config.read(os.path.join(scripts.path_constants.CONFIGS_PATH, filename), encoding='utf-8')
        # 获取配置文件的内容
        section = 'mysql'
        host = config.get(section, 'mysql_host')
        user = config.get(section, 'mysql_user')
        password = config.get(section, 'mysql_password')
        port = config.getint(section, 'mysql_port')
        db = config.get(section, 'mysql_db')
        # 创建数据库连接
        self.connect = pymysql.connect(host=host,
                                       user=user,
                                       password=password,
                                       db=db,
                                       port=port,
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

    # 关闭方法
    def close(self):
        # 先关闭游标对象
        self.cursor.close()
        # 接着关闭与数据的连接
        self.connect.close()


if __name__ == '__main__':
    do = HandleMySql(scripts.path_constants.CONFIG_MYSQL)
    sql = "select * from member Where mobilephone = '17777788888'"
    print(do.do_execute(sql))
    do.close()
