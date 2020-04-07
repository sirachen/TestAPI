# coding=utf-8
'''
------------------------------------
 @Auth : want
 @Time : 2020/3/28 下午8:04
 @File : handle_user.py
 @IDE  : PyCharm
------------------------------------
'''

from scripts.handle_config import HandleConfig

from scripts.path_constants import CONFIG_REQUEST, CONFIG_USER

from scripts.handle_request import HandleRequest

from scripts.handle_mysql import HandleMysql


def create_new_user(regname, pwd='123456'):
    '''
        新建用户的封装类
    '''
    do_config = HandleConfig(CONFIG_REQUEST)
    do_request = HandleRequest()
    do_mysql = HandleMysql()
    register_url = do_config.get_value('url', 'register_url')
    sql = "SELECT Id FROM member WHERE MobilePhone = %s"
    while True:
        mobile = do_mysql.create_not_existed_mobile()
        data = {"regname": regname, "mobilephone": mobile, "pwd": pwd}
        do_request.send_request(url=register_url,
                                data=data,
                                method='post')
        result = do_mysql.do_execute(sql, args=(mobile,))
        if result:
            user_id = result['Id']
            break

    user_dict = {
        regname: {
            "user_id": user_id,
            "mobile": mobile,
            "pwd": pwd,
            "regname": regname
        }
    }
    do_mysql.close()
    do_request.close_request()
    return user_dict


def generate_user_config():
    '''
        生成三个用户
    '''
    user_dicts = {}
    user_dicts.update(create_new_user('admin_user'))
    user_dicts.update(create_new_user('invest_user'))
    user_dicts.update(create_new_user('borrow_user'))
    # 将创建的三个账号写入配置文件
    HandleConfig.write_config(user_dicts, CONFIG_USER)


if __name__ == '__main__':
    generate_user_config()

    pass


