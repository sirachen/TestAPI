# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/4/15 下午5:55
 @File : test_03_recharge.py
 @IDE  : PyCharm
------------------------------------
'''

from libs.ddt import ddt, data
import unittest
import json

from scripts.handle_excel import HandleExcel
from scripts.handle_request import HandleRequest
from scripts.handle_mysql import HandleMysql
from scripts.handle_config import HandleConfig
from scripts.path_constants import REPORTS_ALL_PATH, CONFIG_REQUEST
from scripts.handle_context import Handle_Re


@ddt
class TestRecharge(unittest.TestCase):
    do_config = HandleConfig(CONFIG_REQUEST)
    do_re = Handle_Re()
    do_request = HandleRequest()
    do_excel = HandleExcel(sheetname='recharge')
    cases = do_excel.get_cases()
    pass_result = do_config.get_value('result', 'pass_result')
    fail_result = do_config.get_value('result', 'fail_result')

    @classmethod
    def setUpClass(cls):
        cls.do_mysql = HandleMysql()
        cls.one_file = open(REPORTS_ALL_PATH, mode='a+', encoding='utf-8')
        cls.one_file.write('{:=^40s}\n'.format('开始执行充值接口用例'))

    @classmethod
    def tearDownClass(cls):
        cls.do_mysql.close()
        cls.one_file.write('{:=^40s}\n\n'.format('充值接口用例执行结束'))
        cls.one_file.close()

    @data(*cases)
    def test_recharge(self, one_case):
        # 拼接头部 url 和表格中的接口具体内容
        new_url = self.do_config.get_value('url', 'head_url') + one_case['url']
        # 获取表格中的请求方法
        method = one_case['method']
        # 获取表格中的接口请求数据
        # input_data = one_case['input_data']
        # 获取表格中check_sql 字段是否有内容
        have_sql = one_case['check_sql']
        if have_sql:
            # 如果 check_sql 的内容不为空
            #     SELECT LeaveAmount FROM member WHERE MobilePhone="${investors_login_mobile}"
            # 对sql语句进行参数化,并替换check_sql
            have_sql = self.do_re.recharge_parameterization(have_sql)
            # 去数据库查询充值之前的金额
            recharge_before_amount = self.do_mysql.do_execute(have_sql)
            # 对获取到的数据进行转换,获取到的是decimal格式
            recharge_before_amount = float(recharge_before_amount['LeaveAmount'])
            recharge_before_amount = round(recharge_before_amount, 2)

        # 对获取的数据进行参数化
        new_data = self.do_re.recharge_parameterization(one_case['input_data'])

        # 向接口发送请求数据
        result_data = self.do_request.send_request(url=new_url, data=eval(new_data), method=method).text

        try:
            self.assertIn(one_case['expected'], result_data, msg='充值接口请求成功')
            if have_sql:
                # 再次请求数据库,查询充值之后的金额
                mysql_data = self.do_mysql.do_execute(have_sql)
                # 将金额转换为float类型的数
                # 再将金额转换成float格式的数再次转换成带2位小数的数
                recharge_after_amount = round(float(mysql_data['LeaveAmount']), 2)

                # 将表格中的数据转换成字典格式
                # recharge_amount_dict = json.loads(new_data, encoding='utf-8')
                # 获取到所充值的金额
                recharge_amount = float(json.loads(new_data, encoding='utf-8')['amount'])
                real_amount = round(float(recharge_before_amount + recharge_amount), 2)
                self.assertEqual(real_amount,
                                 recharge_after_amount,
                                 msg='数据库中充值的数据有误')
            self.one_file.write('{},执行的结果为:{}\n'.format(one_case['title'], self.pass_result))
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
