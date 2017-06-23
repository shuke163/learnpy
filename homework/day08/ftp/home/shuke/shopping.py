#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, json
# import demjson
import re

shopping_car_list = []     # 定义一个全局的购物车列表
# shop_record = {}           # 购物记录字典
login_user={}

path = os.path.dirname(os.path.realpath(__file__))  # 获取当前目录
os.chdir(path + '/db')  # 进入当前目录，因为存储用户信息的数据库文件在当前目录下
f = open("user_info", "r+")  # 以读模式打开用户信息数据库文件
data = f.read()
f.close()
# print(data)
user_info = data.split()

