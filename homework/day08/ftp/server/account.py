#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Zhaofengfeng'

from conf.settings import DATABASE
import json

account_file = DATABASE['user_db_file']


def load_user_data(user_db_info=account_file):
    """
    读取所有的用户信息并返回
    :param user_db_info: 参数为account_file路径
    :return: user_data
    """
    user_data_dic = json.load(open(account_file, 'r',encoding='utf-8'))
    return user_data_dic


def id_and_user():
    """
    得到一个列表,元素内容为字典,字典内容为id,username,password
    :return:
    """
    user_info_li = []
    # id_dic = {}
    user_data_dic = load_user_data()
    for i in user_data_dic:
        id_dic = {
            'id': i,
            'username': user_data_dic[i]['username'],
            'password': user_data_dic[i]['password'],
            'quota_space': user_data_dic[i]['quota_space']
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

# user = id_and_user()
# print(user)