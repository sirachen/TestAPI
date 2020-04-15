# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/4/11 下午3:57
 @File : test_02_login.py
 @IDE  : PyCharm
------------------------------------
'''

import unittest

from libs.ddt import ddt, data

from scripts.handle_request import HandleRequest

from scripts.handle_config import HandleConfig

from scripts.handle_excel import HandleExcel

from scripts.handle_log import HandleLog

from scripts.path_constants import DATA_CASES, CONFIG_REQUEST, REPORT_LOGIN_FILE

from scripts.handle_context import Handle_Re


@ddt
class TestCaseLogin(unittest.TestCase):

    do_request = HandleRequest()

    do_config = HandleConfig(CONFIG_REQUEST)

    do_excel = HandleExcel(DATA_CASES, 'login')
    cases = do_excel.get_cases()

    do_log = HandleLog

    do_re = Handle_Re

    pass_result = do_config.get_value('result', 'pass_result')

    fail_result = do_config.get_value('result', 'fail_result')

    @classmethod
    def setUpClass(cls):
        cls.one_file = open(REPORT_LOGIN_FILE, mode='a', encoding='utf-8')
        cls.one_file.write('{:=^40s}\n'.format('开始执行用例'))

    @classmethod
    def tearDownClass(cls):
        cls.one_file.write('{:=^40s}\n\n'.format('用例执行结束'))
        cls.one_file.close()

    @data(*cases)
    def test_login(self, one_case):
        # 拼接完整的url
        url = self.do_config.get_value('url', 'head_url') + one_case['url']
        # 获取请求方式
        method = one_case['method']
        # 获取input_data数据
        input_data = one_case['input_data']
        # 对excel的input_data数据进行参数化
        new_data = self.do_re.login_user_mobile_pwd_replace(input_data)
        # 发送请求接收请求后的结果
        result_real = self.do_request.send_request(url=url, data=eval(new_data), method=method).text

        try:
            self.one_file.write('{},执行的结果为:{}\n'.format(one_case['title'], self.pass_result))
            self.do_excel.write_cell(row=one_case['case_id'] + 1,
                                     column=7,
                                     actual=result_real,
                                     result=self.pass_result)
        except AssertionError as err:
            self.one_file.write('{}执行的结果为:{},具体的异常为:{}\n'.format(one_case['title'], self.fail_result, err))
            self.do_excel.write_cell(row=one_case['case_id'] + 1,
                                     column=7,
                                     actual=result_real,
                                     result=self.fail_result)
            raise err
        self.do_request.close_request()


if __name__ == '__main__':
    unittest.main()
