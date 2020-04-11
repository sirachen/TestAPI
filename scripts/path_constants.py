# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/24 下午2:58
 @File : path_constants.py
 @IDE  : PyCharm
------------------------------------
'''

import os

# 项目根目录
BASE_PATH = os.path.dirname(os.path.dirname(__file__))

# cases 目录
CASES_PATH = os.path.join(BASE_PATH, 'cases')

# configs目录
CONFIGS_PATH = os.path.join(BASE_PATH, 'configs')
CONFIG_LOG = os.path.join(CONFIGS_PATH, 'log_config.conf')
CONFIG_MYSQL = os.path.join(CONFIGS_PATH, 'mysql_config.conf')
CONFIG_REQUEST = os.path.join(CONFIGS_PATH, 'request_config.conf')
CONFIG_USER = os.path.join(CONFIGS_PATH, 'user_config.conf')

# datas目录
DATAS_PATH = os.path.join(BASE_PATH, 'datas')
DATA_CASES = os.path.join(DATAS_PATH, 'datas.xlsx')

# libs目录
LIBS_PATH = os.path.join(BASE_PATH, 'libs')

# logs目录
LOGS_PATH = os.path.join(BASE_PATH, 'logs')
LOG_FILE = os.path.join(LOGS_PATH, 'file.log')

# reports目录
REPORTS_PATH = os.path.join(BASE_PATH, 'reports')
REPORT_REGISTER_FILE = os.path.join(REPORTS_PATH, 'register_record.txt')
REPORT_LOGIN_FILE = os.path.join(REPORTS_PATH, 'login_record.txt')

# scripts目录
SCRIPTS_PATH = os.path.join(BASE_PATH, 'scripts')

pass