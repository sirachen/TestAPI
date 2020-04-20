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

from scripts.path_constants import CONFIG_MYSQL


class HandleConfig:
    '''
        Config配置文件的封装类
    '''

    def __init__(self, filename=CONFIG_MYSQL):
        '''
            filename : 要读取的配置文件名
        '''
        # 创建配置文件对象
        self.config = ConfigParser()
        # 读取配置文件
        self.config.read(filename, encoding='utf-8')

    def get_value(self, section, option):
        '''
            get_value 方法,会返回查到的配置文件的内容
            @section : config 方法中的区域名
            @option : config 方法中的键名
        '''
        # 返回 config.get 方法获取的内容
        return self.config.get(section=section, option=option)

    def get_int(self, section, option):
        '''
            get_int 方法,会返回查到的配置文件的内容以整数类型返回
            @section : config 方法中的区域名
            @option : config 方法中的键名
        '''
        # 返回 config.getint 方法获取的整数类型的内容
        return self.config.getint(section=section, option=option)

    def get_boolean(self, section, option):
        '''
            get_boolean 方法,会返回查到的配置文件的内容以boolean类型返回
            @section : config 方法中的区域名
            @option : config 方法中的键名
        '''
        # 返回 config.getboolean 方法获取的boolean类型的内容
        return self.config.getboolean(section=section, option=option)

    def get_float(self, section, option):
        '''
            get_float 方法,会返回查到的配置文件的内容以float类型返回
            @section : config 方法中的区域名
            @option : config 方法中的键名
        '''
        # 返回 config.getfloat 方法获取的float类型的内容
        return self.config.getfloat(section=section, option=option)

    @staticmethod
    def write_config(datas, filename):
        if isinstance(datas, dict):
            for value in datas.values():
                if isinstance(value, dict):
                    config = ConfigParser()
                    for key in datas:
                        config[key] = datas[key]
                    with open(filename, 'w') as write_file:
                        config.write(write_file)


if __name__ == '__main__':
    han = HandleConfig(CONFIG_MYSQL)
    req = han.get_value('mysql', 'mysql_is', 'BooL')
    print(req)
