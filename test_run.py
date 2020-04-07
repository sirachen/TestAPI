# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/28 下午9:09
 @File : test_run.py
 @IDE  : PyCharm
------------------------------------
'''

import unittest

import os

from libs.HTMLTestRunnerNew import HTMLTestRunner

from datetime import datetime

from scripts.path_constants import REPORTS_PATH, CONFIG_USER, CASES_PATH

from scripts.handle_user import generate_user_config


if not os.path.exists(CONFIG_USER):
    generate_user_config()

one_suite = unittest.defaultTestLoader.discover(CASES_PATH)

# %Y-%m-%d %H:%M:%S     年-月-日-时-分-秒
# %Y-%m-%d              年-月-日

time_now = REPORTS_PATH + '/report_' + datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S') + '.html'
save_file = open(time_now, mode='wb')
two_runner = HTMLTestRunner(stream=save_file,
                            title='测试报告',
                            verbosity=2,        # 2 为最详细
                            description='报告输出完成',
                            tester='by:want')
two_runner.run(one_suite)
save_file.close()
