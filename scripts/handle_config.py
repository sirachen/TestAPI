# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/24 下午3:45
 @File : handle_config.py
 @IDE  : PyCharm
------------------------------------
'''

from configparser import ConfigParser

import os

from scripts.path_constants import CONFIG_MYSQL


class HandleConfig:
    '''
        Config配置文件的封装类
    '''

    def __init__(self, filename):
        '''
            filename : 要读取的配置文件名
        '''
        # 创建配置文件对象
        self.config = ConfigParser()
        # 读取配置文件
        self.config.read(filename, encoding='utf-8')

    def get_value(self, section, option, type=None):
        '''
            get_value 方法,会返回查到的配置文件的内容
            @section : config 方法中的区域名
            @option : config 方法中的键名
        '''

        # 默认 type 为 None ,即为默认get方法
        if type is None:
            # 返回 config.get 方法获取的内容
            return self.config.get(section=section, option=option)
        # 转换 type 的内容全部为小写,type 内容为 int时
        elif type.lower() == 'int':
            # 返回 config.getint 方法获取的正数内容
            return self.config.getint(section=section, option=option)
        elif type.lower() == 'bool':
            return self.config.getboolean(section=section, option=option)
        elif type.lower() == 'float':
            return self.config.getfloat(section=section, option=option)


if __name__ == '__main__':
    han = HandleConfig(CONFIG_MYSQL)
    req = han.get_value('mysql', 'mysql_is', 'BooL')
    print(req)
