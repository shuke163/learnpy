#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/7/11 0011

import os
import sys

BASE_DIR = os.path.normpath(os.path.join(
        os.path.abspath(__file__),
        os.pardir,
        os.pardir,
))
sys.path.append(BASE_DIR)

from core.login import Auth_show_info
from core import execcom
from core import manage

if __name__ == '__main__':
    print("#" * 100)
    print("###", "\033[1;33mWelcome to command system\033[0m".center(103, ' '), "###")
    print("#" * 100)
    while True:
        login_user = input("请输入用户名: ").strip()
        login_pwd = input("请输入密码: ").strip()
        if not login_user or not login_pwd: continue
        if login_user != "admin":
            obj = Auth_show_info(login_user, login_pwd)
            res = obj.show_user_info()
            if not res: continue
            obj.show_host()
            all_host_dic = obj.get_host_info()
            if not all_host_dic:
                continue
            else:
                execcom.main(all_host_dic)              # 普通用户执行命令函数
        elif login_user == "admin":
            manage.main(login_user,login_pwd)           # 管理员用户修改表数据操作函数