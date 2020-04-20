# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/4/16 下午5:21
 @File : test_04_add.py
 @IDE  : PyCharm
------------------------------------
'''

from ddt import ddt, data
import unittest

from scripts.handle_config import HandleConfig
from scripts.handle_request import HandleRequest
from scripts.handle_excel import HandleExcel
from scripts.handle_context import Handle_Re
from scripts.handle_mysql import HandleMysql
from scripts.path_constants import CONFIG_REQUEST, REPORTS_ALL_PATH


@ddt
class TestAdd(unittest.TestCase):

    do_re = Handle_Re()

    do_request = HandleRequest()

    do_config = HandleConfig(CONFIG_REQUEST)

    # 初始化HandleExcel对象
    do_excel = HandleExcel(sheetname='add')
    # 获取所有的用例
    cases = do_excel.get_cases()

    pass_result = do_config.get_value('result', 'pass_result')
    fail_result = do_config.get_value('result', 'fail_result')

    @classmethod
    def setUpClass(cls):
        cls.do_mysql = HandleMysql()
        cls.one_file = open(REPORTS_ALL_PATH, mode='a+', encoding='utf-8')
        cls.one_file.write('{:=^40s}\n'.format('开始执行加标接口用例'))

    @classmethod
    def tearDownClass(cls):
        cls.do_mysql.close()
        cls.one_file.write('{:=^40s}\n\n'.format('加标接口用例执行结束'))
        cls.one_file.close()

    @data(*cases)
    # 对所有用例进行拆包
    def test_add(self, one_case):
        # 获得单个的用例,获取单个用例的请求数据
        # data = one_case['input_data']
        # 对请求数据进行参数化,获取到参数化后的数据
        new_data = self.do_re.add_parameterization(one_case['input_data'])
        # 获取请求的url地址
        url = self.do_config.get_value('url', 'head_url') + one_case['url']
        # 获取接口请求方式
        method = one_case['method']
        # 对接口发送请求,获取请求后的返回数据
        result_data = self.do_request.send_request(url=url, data=eval(new_data), method=method).text
        # 获取接口请求成功的标识
        # expected = one_case['expected']
        try:
            self.assertIn(one_case['expected'], result_data, msg='加标接口请求成功')
            self.one_file.write('{}执行的结果为:{}\n'.format(one_case['title'], self.pass_result))
            self.do_excel.write_cell(row=one_case['case_id'] + 1,
                                     column=7,
                                     actual=result_data,
                                     result=self.pass_result)
        except AssertionError as err:
            self.one_file.write('{}执行的结果为:{},具体的异常为:{}\n'.format(one_case['title'], self.fail_result, err))
            self.do_excel.write_cell(row=one_case['case_id'] + 1,
                                     column=7,
                                     actual=result_data,
                                     result=self.fail_result)
            raise err
        self.do_request.close_request()


if __name__ == '__main__':
    unittest.main()
