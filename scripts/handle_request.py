# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/24 下午4:13
 @File : handle_request.py
 @IDE  : PyCharm
------------------------------------
'''

import requests

from scripts.handle_config import HandleConfig

import scripts.path_constants


class HandleRequest:
    '''
        request 的封装类
    '''

    def __init__(self):
        # 创建 requests 的 session 会话
        self.session = requests.Session()

    # send_request 方法,来对接口进行访问
    def send_request(self, url, data, is_json=False, method='get'):
        '''
            url: 需要访问的url地址
            data: 需要传入的参数
            is_json: 返回内容是否为json格式
            method: 接口请求方法
        '''

        # 请求方式为get
        if method.lower() == "get":
            # 返回 session 的get方法执行后的内容
            return self.session.get(url, data)
        # 请求方式为post
        elif method.lower() == "post":
            if is_json:
                # is_json 为True ,代表传入的参数为json格式,返回 session 的post方法,传入json格式执行后的内容
                return self.session.post(url, json=data)
            else:
                # is_json 为False ,代表传入的参数为json格式,返回 session 的post方法
                return self.session.post(url, data=data)
        else:
            # 返回空内容
            return None
            print('暂不支持其他格式')

    # close_request 方法,用来关闭 Session 会话
    def close_request(self):
        self.session.close()


if __name__ == '__main__':
    do_config = HandleConfig(scripts.path_constants.CONFIG_REQUEST)
    mobile = do_config.get_value('user', 'mobile', type='int')
    pwd = do_config.get_value('user', 'password', type='int')

    login_url = do_config.get_value('url', 'login_url')
    login_data = {
        'mobilephone': mobile,
        'pwd': pwd
    }
    recharge_url = do_config.get_value('url', 'recharge_url')
    recharge_data = {
        'mobilephone': mobile,
        'amount': 100
    }
    do_handle_request = HandleRequest()
    login_req = do_handle_request.send_request(login_url, data=login_data, method='post')
    recharge_req = do_handle_request.send_request(recharge_url, data=recharge_data, method='post')

    print(login_req.json())
    print(recharge_req.json())

    register_url = do_config.get_value('url', 'register_url')
    register_req = do_handle_request.send_request(url=register_url,
                                                  data='{"mobilephone": "15913902765", "pwd": "123456789", "regname": "www"}',
                                                  method='post')
    print(register_req)

    pass