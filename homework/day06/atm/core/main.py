#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
from conf import settings
from core import goods
from core.auth import *
from core.account import load_user_data, account_file, register_user


def user_info():
    """
    账户信息
    :return:
    """
    user_data = load_user_data()
    user_id = input("请输入要查询的账户ID： ").strip()
    if user_id.isdecimal() and user_id in user_data:
        temp_dic = user_data[user_id]
        temp_info = """
        账户ID: {},
        用户名: {},
        密码: ***,
        余额: {},
        注册日期: {},
        过期时间: {},
        信用额度: {},
        还款日期: {},
        账户状态: {}
        """.format(user_id, temp_dic['username'], temp_dic['balance'], temp_dic['enroll_date'], \
                   temp_dic['expire_date'], temp_dic['credit'], temp_dic['pay_day'], temp_dic['status'])
        print(temp_info)
    else:
        print("\033[1;31m输入的ID不存在,请联系管理员进行查询!\033[0m")


def repayment(credit_num=15000):
    """
    还款
    :return:
    """
    if login_user['credit'] < credit_num:
        consume_num = credit_num - login_user['credit']
        print("当前账户: %s, 余额: %d,需还款金额: %d " % (login_user['name'], login_user['balance'], consume_num))
        settings.logger.info("user: %s,余额: %d,需还款金额: %d" % (login_user['name'], login_user['balance'], consume_num))
        if login_user['balance'] < consume_num:
            print("您的账户余额不足,请进行充值!")
            return
        else:
            while True:
                inp = input("请确认是否进行还款操作(y|n): ").strip()
                if inp.lower() == "y":
                    new_user_data = load_user_data()
                    if login_user['id'] in new_user_data:
                        login_user['credit'] += consume_num
                        login_user['balance'] -= consume_num
                        print("\033[1;32m还款成功,正在保存修改...\033[0m")
                        settings.logger.info("user: %s,还款金额: %d,还款成功!" % (login_user['name'], consume_num))
                        new_user_data[login_user['id']]['credit'] = login_user['credit']
                        new_user_data[login_user['id']]['balance'] = login_user['balance']
                        json.dump(new_user_data, open(account_file, 'w', encoding='utf-8'), \
                                  sort_keys=True, indent=4, ensure_ascii=False)
                        break
                elif inp.lower() == "n":
                    pass
                    break
                else:
                    print("\033[1;31m请输入(y|Y)或(n|N),谢谢!\033[0m")
                    continue
    elif login_user['credit'] == credit_num:
        print("信用卡未消费,可用额度为: %d" % login_user['credit'])
    elif login_user['credit'] > credit_num:
        print("请联系管理员更改您的账户可用额度!")


def transfer_acc():
    """
    转账
    :return:
    """
    user_data = load_user_data()
    while True:
        inp_id = input("请输入对方的账户ID: ").strip()
        if inp_id.isdecimal() and inp_id in user_data:
            transfer_amount = input("请输入转账金额: ").strip()
            if transfer_amount.isdecimal():
                transfer_amount = int(transfer_amount)
                if transfer_amount <= login_user['balance']:
                    login_user['balance'] -= transfer_amount
                    print("\033[1;32m转账成功,银子已经存入对方账户余额!\033[0m")
                    settings.logger.info("user: %s,转入账户: %s,转账金额: %d" % \
                                         (login_user['name'], user_data[inp_id]['username'], transfer_amount))
                    user_data[login_user['id']]['balance'] = login_user['balance']
                    user_data[inp_id]['balance'] = user_data[inp_id]['balance'] + transfer_amount
                    # print(user_data)
                    json.dump(user_data, open(account_file, 'w', encoding='utf-8'), \
                              sort_keys=True, indent=4, ensure_ascii=False)
                    break
                else:
                    print("\033[1;31m余额不足,转账失败!\033[0m")
                    break
            else:
                print("\033[1;31m请输入一个正整数\033[0m")
                continue
        elif inp_id not in user_data:
            print("\033[1;31m对方账户不存在,请重新输入!\033[0m")
            continue


def register():
    """
    注册
    :return:
    """
    reg = register_user()
    reg.register()


def acc_frozen():
    if login_user['name'] != "admin":
        print("\033[1;31m请使用管理员账号进行操作!\033[0m")
    else:
        new_user_data = load_user_data()
        acc_id=input("请输入需要冻结的账户ID: ").strip()
        if acc_id.isdecimal() and acc_id in new_user_data:
            new_user_data[acc_id]['status'] = 1
            # print(user_data)
            print("\033[1;32m当前账户: %s,冻结账户: %s\033[0m"%(login_user['name'],new_user_data[acc_id]['username']))
            settings.logger.info("user: %s,冻结账户: %s" % (login_user['name'], new_user_data[acc_id]['username']))
            json.dump(new_user_data, open(account_file, 'w', encoding='utf-8'), \
                      sort_keys=True, indent=4, ensure_ascii=False)
        else:
            print("\033[1;31m输入不合法或账户ID不存在!\033[0m")


# 没用
def sign_out():
    """
    退出
    :return:
    """
    print("\033[1;32m再见,祝您工作顺利,生活愉快!\033[0m")


@auth_login
def account_manage():
    print(" 账户管理中心 ".center(50, '*'), end="")
    info = """
        1. 账户信息
        2. 冻结账户
        3. 注册
        4. 还款
        5. 转账
        6. 退出
    """
    menu_acc = {
        "1": user_info,
        "2": acc_frozen,
        "3": register,
        "4": repayment,
        "5": transfer_acc,
        "6": sign_out
    }
    print(info)
    while True:
        choice = input("请输入您的选择: ").strip()
        if choice in menu_acc:
            if choice != "6":
                menu_acc[choice]()
            else:
                print("\033[1;32m再见,祝您工作顺利,生活愉快!\033[0m")
                break
        else:
            print("\033[1;31m请输入1-6之间的整数!\033[0m")


def run():
    info = '''
        1. 商品列表
        2. 购物车
        3. 结算
        4. 账户管理中心
    '''
    print('*' * 50)
    print(info)
    print('*' * 50)
    menu_index = ['1', '2', '3']
    choice = input("请输入您的选择: ").strip()
    if choice.isdecimal() and choice in menu_index:
        goods.main(choice)
    elif choice == "4":         # 账户管理中心
        account_manage()
    else:
        print("\033[1;31m请输入1-4之间的整数!\033[0m")


# run()
