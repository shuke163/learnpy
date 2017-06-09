#!/usr/bin/env python
# -*- coding:utf-8 -*-

from conf import settings
import json
import os

account_file = os.path.join(settings.DATABASE['path'], 'accounts','accounts.json')


def load_user_data(user_db_info=account_file):
    """
    读取所有的用户信息并返回
    :param user_db_info: 参数为account_file路径
    :return: user_data
    """
    user_data_dic = json.load(open(account_file, 'r',encoding='utf-8'))
    # print(user_data)
    return user_data_dic


def id_and_user():
    """
    得到一个列表内容为,元素内容为字典，字典内容为id,username,password
    :return:
    """
    user_info_li = []
    id_dic = {}
    user_data_dic = load_user_data()
    for i in user_data_dic:
        id_dic = {
            'id': i,
            'username': user_data_dic[i]['username'],
            'password': user_data_dic[i]['password'],
            'balance': user_data_dic[i]['balance'],
            'credit': user_data_dic[i]['credit'],
            'status': user_data_dic[i]['status']
        }
        user_info_li.append(id_dic)
    return user_info_li


def query_user(user_name):
    """
    根据用户输入的用户名查询用户是否存在，返回True 或者 False
    :param user_inp: 用户输入
    :param user_data_func: 查询用户信息的函数
    :return:
    """
    account_list = []
    account_dic = load_user_data()
    for id in account_dic:
        account_list.append((account_dic[id]['username']))
    # print(account_list)
    if user_name in account_list:
        return True
    else:
        return False


def auth_login():
    pass


class register_user(object):
    '''
    注册用户
    '''

    def __init__(self, balance=0, expire_date="2021-01-01", enroll_date="2016-01-02", credit=15000, status=0,
                 pay_day=22):
        self.balance = balance
        self.expire_date = expire_date
        self.enroll_date = enroll_date
        self.credit = credit
        self.status = status
        self.pay_day = pay_day

    def register(self):
        new_user_dic = {}
        while True:
            register = input("用户名：")
            if not register.isalnum():
                print("\033[1;31m用户名不合法，必须是纯字母或字母和数字的组合。\033[0m")
                continue
            register_pwd = input("输入密码: ").strip()
            register_pwd_again = input("请确认密码: ").strip()
            user_data_dic = load_user_data()
            if register_pwd == register_pwd_again:
                id_num = max(user_data_dic)
                new_id = str(int(id_num) + 1)
                new_user_dic[new_id] = {"username": register, "password": register_pwd, "balance": self.balance, \
                                        "expire_date": self.expire_date, "enroll_date": self.enroll_date, \
                                        "credit": self.credit, "status": self.status, "pay_day": self.pay_day}
                user_data_dic.update(new_user_dic)
                # print(user_data_dic)           # 新增注册用户后的json内容
                json.dump(user_data_dic, open(account_file, 'w',encoding='utf-8'),\
                          sort_keys=True,indent=4,ensure_ascii=False)
                print("\033[1;32m注册成功!\033[0m")
                break
            elif register_pwd != register_pwd_again:
                print("\033[1;31m密码不一致，请重新输入！\033[0m")


# reg_user = register_user()
# reg_user.register('shuke','123')
# id_and_user()
