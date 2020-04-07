# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/5 下午6:13
 @File : test_register.py
 @IDE  : PyCharm
------------------------------------
'''

import unittest

from scripts.handle_excel import HandleExcel

from scripts.handle_context import Handle_Re

from scripts.handle_config import HandleConfig

from scripts.handle_request import HandleRequest

from libs.ddt import ddt, data

from scripts.path_constants import DATA_CASES, REPORT_REGISTER_FILE, CONFIG_REQUEST


@ddt
class TestCaseRegister(unittest.TestCase):
    handleExcel = HandleExcel(DATA_CASES, 'register')
    cases = handleExcel.get_cases()

    do_config = HandleConfig(CONFIG_REQUEST)
    head_url = do_config.get_value('url', 'head_url')
    do_request = HandleRequest()

    # 用例执行通过信息
    pass_result = do_config.get_value('result', 'pass_result')
    # 用例执行不通过信息
    fail_result = do_config.get_value('result', 'fail_result')

    @classmethod
    def setUpClass(cls):
        log_filename = REPORT_REGISTER_FILE
        cls.one_file = open(log_filename, mode='a', encoding='utf-8')
        cls.one_file.write('{:=^40s}\n'.format('开始执行用例'))

    @classmethod
    def tearDownClass(cls):
        cls.one_file.write('{:=^40s}\n\n'.format('用例执行结束'))
        cls.one_file.close()

    @data(*cases)
    def test_register(self, one_case):

        # 注册接口的url
        url = self.head_url + one_case['url']

        # 对用例中的数据进行参数化
        new_data = Handle_Re.register_user_mobile_replace(one_case['input_data'])

        method = one_case['method']

        # 发送注册接口的请求
        result_real = self.do_request.send_request(url=url, data=eval(new_data), method=method).text

        msg = one_case['title']

        try:
            # self.assertIn(result_except, result_real, msg=msg)
            self.one_file.write('{},执行的结果为:{}\n'.format(msg, self.pass_result))
            self.handleExcel.write_cell(row=one_case['case_id'] + 1,
                                        column=6,
                                        expected=msg,
                                        actual=result_real,
                                        result=self.pass_result)
        except AssertionError as err:
            self.one_file.write('{}执行的结果为:{},具体的异常为:{}\n'.format(msg, self.fail_result, err))
            self.handleExcel.write_cell(row=one_case['case_id'] + 1,
                                        column=6,
                                        expected=msg,
                                        actual=result_real,
                                        result=self.fail_result)
            raise err
        self.do_request.close_request()


if __name__ == '__main__':
    unittest.main()
