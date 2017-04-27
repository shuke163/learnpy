#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys

path = os.path.dirname(os.path.realpath(__file__))  # 获取当前目录
os.chdir(path)                          # 进入当前目录，因为存储用户信息的数据库文件在当前目录下

f = open("user_info", "r")              # 以读模式打开用户信息数据库文件
data = f.read()
f.close()                               # 关闭文件句柄

user_info_str = data.split()            # 用户信息列表，以"\n"为分割符
user_info = []                          # 用于存放用户所有信息的字典列表
lock_user = []                          # 用于存放锁定用户的账号列表
username = []                           # 用于存放用户名的列表

for item in user_info_str:
    temp = item.split('|')              # 迭代列表中每个元素，并以"|"分割成新的列表
    user_info_dic = {                   # 从列表中取出每个元素，并放入字典中
        'name': temp[0],
        'passwd': temp[1],
        'times': temp[2]
    }
    user_info.append(user_info_dic)     # 将存放用户信息的字典放入新的列表中
    username.append(temp[0])            # 将所有账号放入用户名列表中
    if int(temp[2]) >= 3:               # 判断该用户是否处于锁定状态，如果是，那么放入锁定用户的列表中
        lock_user.append(temp[0])

# print(user_info)
while True:                             # 输入用户名密码登陆逻辑
    name = input("请输入用户名: ")
    if name not in lock_user:           # 判断用户输入的用户名是否锁定列表中
        if name in username:            # 判断用户输入的用户名是否存在
            passwd = input("请输入密码: ")
            for item in user_info:      # 迭代用于存放用户所有信息的字典列表uer_info
                if name == item['name'] and passwd == item['passwd']:   # 判断用户名密码，正确允许登陆
                    item['times'] = 0                                   # 剩余验证次数清零
                    print("\033[1;32m登陆成功!\033[0m")
                    # print(user_info)
                elif name == item['name'] and passwd != item['passwd']:  # 判断用户名密码
                    item['times'] = (int(item['times']) + 1)             # 密码错误，剩余验证次数加1
                    if int(item['times']) >= 3:                          # 判断如果剩余验证次数大于等于3，那么放入锁定用户的列表中
                        lock_user.append(item['name'])
                        # print(lock_user)
                    print("\033[1;31mERROR: 密码错误，剩余%d次机会，请再想想...\033[0m" % (3 - int(item['times'])))  # 剩余验证次数
        else:
            print("\033[1;31mERROR: 用户不存在!\033[0m")
    else:
        print("\033[1;31mERROR:用户:%s 已经被锁定,暂时不允许登陆...\033[0m" % name)
        # print(lock_user)
        while True:
            back_quit = input("返回: 'b|B'或 退出：'q|Q': ")            # 账户被锁定时用户选择
            if back_quit == 'b' or back_quit == 'B':                   # 跳出循环，重新输入
                break
            elif back_quit == 'q' or back_quit == 'Q':                 # 判断用户选择是否退出程序
                f = open('user_info', 'w')
                for value in user_info:                                # 将更新后的存放用户所有信息的字典列表内容写入数据库文件中
                    userinfo_str = value['name'] + '|' + value['passwd'] + '|' + str(value['times'])   # 拼接字符串
                    f.write(userinfo_str + '\n')
                    # print(userinfo_str)
                f.close()     # 关闭文件句柄
                exit()        # 退出程序
