#!/usr/bin/env python
#-*- coding:utf-8 -*-

from core import account

login_user={'id':None,'name':None,'status':False,'balance':0,'credit':0}

# 普通账户认证装饰器
def auth_login(func):
    def wrapper(*args,**kwargs):
        if login_user['name'] and login_user['status']:
            print('用户登陆状态为: ',login_user)
            res = func(*args,**kwargs)
            return res
        else:
            user_name = input("username: ").strip()
            user_pwd = input("password: ")
            user_info_li = account.id_and_user()            # 调用id_and_user()函数
            # print('用户信息列表: ',user_info_li)
            for item in user_info_li:
                if user_name == item['username'] and user_pwd == item['password'] and item['status'] == 0:
                    login_user['id']=item['id']
                    login_user['name']=item['username']
                    login_user['status']=True
                    login_user['balance']=int(item['balance'])
                    login_user['credit']=int(item['credit'])
                    print('\033[1;32m登陆成功!\033[0m')
                    print('用户登陆状态为: ', login_user)
                    res = func(*args, **kwargs)
                    return res
                    break
                elif user_name == item['username'] and item['status'] == 1:
                    print("\033[1;31m账户已经被冻结,请联系管理员进行解冻!\033[0m")
                    exit()
            else:
                print("\033[1;31m用户名或密码错误,请检查!\033[0m")
    return wrapper

# 管理员账户认证装饰器,暂时没用
def admin_auth(func):
    def wrapper(*args,**kwargs):
        if login_user['name'] and login_user['status']:
            print('用户登陆状态为: ',login_user)
            res = func(*args,**kwargs)
            return res
        else:
            user_name = input("username: ").strip()
            user_pwd = input("password: ")
            user_info_li = account.id_and_user()            # 调用id_and_user()函数
            # print('用户信息列表: ',user_info_li)
            for item in user_info_li:
                if user_name == item['username'] and user_pwd == item['password'] and user_name == 'admin':
                    login_user['id']=item['id']
                    login_user['name']=item['username']
                    login_user['status']=True
                    login_user['balance']=int(item['balance'])
                    login_user['credit']=int(item['credit'])
                    print('\033[1;32m管理员账户,登陆成功!\033[0m')
                    print('用户登陆状态为: ', login_user)
                    res = func(*args, **kwargs)
                    return res
                    break
                elif user_name != "admin":
                    print("\033[1;31m请使用管理员账号进行登陆!\033[0m")
                    break
            else:
                print("\033[1;31m用户名或密码错误,请检查!\033[0m")
    return wrapper














