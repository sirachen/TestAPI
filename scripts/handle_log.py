# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/24 下午4:49
 @File : handle_log.py
 @IDE  : PyCharm
------------------------------------
'''
import os

import logging

from scripts.handle_config import HandleConfig

import scripts.path_constants

from scripts.path_constants import CONFIG_LOG


class HandleLog:

    '''
        log日志封装类
    '''
    def __init__(self):
        '''
            读取 /home/want/PycharmProjects/TestAPI/configs/log_config.conf
            目录下的配置文件
        '''
        do_config = HandleConfig(CONFIG_LOG)

        # 创建日志收集器对象
        self.log = logging.getLogger(do_config.get_value('log', 'log_name'))

        # 设置日志收集器对象收集等级
        self.log.setLevel(do_config.get_value('log', 'log_level'))

        # 创建控制台渠道
        console_handler = logging.StreamHandler()

        # 创建文件渠道
        file_handler = logging.FileHandler(os.path.join(scripts.path_constants.LOGS_PATH,
                                                        do_config.get_value('log', 'file_name')), encoding='utf-8')

        # 设置控制台渠道的等级
        console_handler.setLevel(do_config.get_value('log', 'console_level'))
        file_handler.setLevel(do_config.get_value('log', 'file_level'))

        # 设置输出格式
        console_formatter = logging.Formatter(do_config.get_value('log', 'console_formatter'))
        file_formatter = logging.Formatter(do_config.get_value('log', 'file_formatter'))

        # 绑定控制台渠道和输出格式
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)

        # 给收集器添加handler
        self.log.addHandler(console_handler)
        self.log.addHandler(file_handler)

    def get_logs(self):
        '''
        获取log信息
        '''
        return self.log


do_log = HandleLog().get_logs()

if __name__ == '__main__':
    log = HandleLog().get_logs()
    log.debug('debug')
    log.error('error')
    log.info('info')
    log.warning('warning')
    log.critical('critical')