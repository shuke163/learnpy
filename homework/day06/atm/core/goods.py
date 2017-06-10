#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import json
import time
from conf import settings
from core.auth import auth_login, login_user
from core.account import load_user_data,register_user,account_file

goods_path = os.path.join(settings.BASE_DIR, 'db', 'goods')
shop_car_dic={}
shopping_car_list = []  # 定义一个全局的购物车列表

shop_dict = json.load(open(goods_path, 'r', encoding='utf-8'))  # 从json文件中读取商品清单，并序列化为shop_dict字典
shop_type = list(shop_dict.keys())


def show_goods_type(type_id):
    """
    商品类型
    :return:
    """
    # choice_id = input("请输入类别id: ").strip()
    if type_id.isdecimal():
        type_id = int(type_id)
        if 0 < type_id <= len(shop_type):
            shop_type_list = shop_dict[shop_type[(type_id - 1)]]
            return shop_type_list
        else:
            print("对不起，输入的id不存在，请重新输入!")
    else:
        print("对不起，输入不合法，请输入一个整数!")

def shop_history_to_file(shop_record):
    history_file = settings.HISTORY_FILE
    if not os.path.isfile(history_file):
        # os.mknod(history_file)
        json.dump(shop_record, open(history_file, 'w',encoding='utf-8'),sort_keys=True, indent=4, ensure_ascii=False)
    else:
        shop_history_data = json.load(open(history_file, 'r', encoding='utf-8'))
        if login_user['name'] not in shop_history_data:
            shop_history_data.update(shop_record)
            print("写入的内容是1: ",shop_history_data)
            json.dump(shop_history_data, open(history_file, 'w',encoding='utf-8'),sort_keys=True,indent=4,ensure_ascii=False)
        else:
            print(shop_history_data[login_user['name']])
            print('购物车: ',shop_record[login_user['name']])
            shop_history_data[login_user['name']]=shop_history_data[login_user['name']] + (shop_record[login_user['name']])
            print("写入的内容是2: ", shop_history_data)
            json.dump(shop_history_data,open(history_file, 'w',encoding='utf-8'),sort_keys=True,indent=4,ensure_ascii=False)

def show_goods(shop_type_list):
    """
    功能:商品清单
    该方法返回一个列表，内容为登陆的用户购买物品的信息
    :return:
    """
    while True:
        page_num = input("请输入页码: , 返回(b|B), 退出(q|Q): ").strip()
        if page_num.isdecimal():
            page_num = int(page_num)
            # total_page_num = len(shop_type_list)
            pages_num = divmod(len(shop_type_list), 10)
            if pages_num[1] == 0:
                total_page_num = pages_num[0]
            else:
                total_page_num = pages_num[0] + 1
            if 1 <= page_num <= total_page_num:
                start_num = (page_num - 1) * 10
                end_num = page_num * 10
                shop_list = shop_type_list[start_num:end_num]
                # print(shop_list)
                if page_num == 1:  # 物品id处理
                    id = 1
                elif page_num > 1:
                    id = (page_num - 1) * 10 + 1
                print("\033[1;32m%-14s %-14s %-4s\033[0m" % ("物品ID:", "商品名称:", "商品价格:"))
                for item, ele in enumerate(shop_list, id):
                    print("%-15s %-15s %-5s" % (item, ele['name'], "$" + ele['price']))
            else:
                print("请输入1-%d之间的正整数" % (total_page_num))
                continue
        elif page_num.lower() == 'b':
            break
        elif page_num.lower() == 'q':
            print("\033[1;32m欢迎下次光临!\033[0m")
            exit()
        else:
            print("对不起,输入不合法,请输入一个正整数!")
            continue

@auth_login
def shopping_car():
    """
    功能:商品清单
    该方法返回一个列表，内容为登陆的用户购买物品的信息
    :return:
    """
    while True:
        print(" 商品类别 ".center(50, '*'))
        for i, ele in enumerate(shop_type, 1):
            print(i, ele)
        type_id = input("请输入类别id: ").strip()
        shop_type_list = show_goods_type(type_id)
        while True:
            page_num = input("请输入页码: ,返回(b|B): ,退出(q|Q): ").strip()
            if page_num.isdecimal():
                page_num = int(page_num)
                # total_page_num = len(shop_type_list)
                pages_num = divmod(len(shop_type_list), 10)
                if pages_num[1] == 0:
                    total_page_num = pages_num[0]
                else:
                    total_page_num = pages_num[0] + 1
                if 1 <= page_num <= total_page_num:
                    start_num = (page_num - 1) * 10
                    end_num = page_num * 10
                    shop_list = shop_type_list[start_num:end_num]
                    # print(shop_list)
                    if page_num == 1:       # 物品id处理
                        id = 1
                    elif page_num > 1:
                        id = (page_num - 1) * 10 + 1
                    print("\033[1;32m%-14s %-14s %-4s\033[0m" % ("物品ID:", "商品名称:", "商品价格:"))
                    for item, ele in enumerate(shop_list, id):
                        print("%-15s %-15s %-5s" % (item, ele['name'], "$" + ele['price']))

                    while True:
                        shop_id = input("加入购物车(id): ,返回(b|B),")
                        temp_shop_dic = {}
                        if shop_id.isdecimal():
                            shop_id = int(shop_id)
                            if start_num < shop_id <= end_num:
                                temp_shop_dic['goods_name'] = shop_type_list[(shop_id - 1)]['name']
                                temp_shop_dic['goods_price'] = shop_type_list[(shop_id - 1)]['price']
                                settings.logger.info("user: %s, Add goods: %s" % (login_user['name'], temp_shop_dic))
                                shopping_car_list.append(temp_shop_dic)
                                print("购物车: ", shopping_car_list)
                                shop_car_dic[login_user['name']]=shopping_car_list
                            else:
                                print('请输入%d-%d之间的整数' % ((start_num + 1), end_num))
                        elif shop_id.lower() == 'b':
                            break
                        else:
                            continue
                else:
                    print("请输入1-%d之间的正整数" % (total_page_num))
                    continue
            elif page_num.lower() == 'b':
                break
            elif page_num.lower() == 'q':
                if shop_car_dic:
                    shop_history_to_file(shop_car_dic)
                    print("\033[1;32m欢迎下次光临!\033[0m")
                    exit()
                else:
                    print("\033[1;32m欢迎下次光临!\033[0m")
                    exit()
            else:
                print("对不起,输入不合法,请输入一个正整数!")
                continue

@auth_login
def checkout():
    print("正在连接银行,请稍等......")
    time.sleep(1)
    account_id=input("请输入您的账号ID: ").strip()
    if account_id.isdecimal():
        if account_id == login_user['id']:
            print("\033[1;32m连接银行成功!\033[0m")
            car_data=json.load(open(settings.HISTORY_FILE,'r',encoding='utf-8'))
            if login_user['name'] in car_data:
                temp_price_li=[]
                for i in car_data[login_user['name']]:
                    temp_price_li.append(int(i['goods_price']))
                flag = False
                while not flag:
                    info="\033[1;31m当前账户余额: %d, 支付金额为: %d\033[0m"%(login_user['balance'],sum(temp_price_li))
                    if login_user['balance'] < sum(temp_price_li):
                        print(info)
                        user_choice=input("\n充值:1,信用卡支付:2, 请选择: ")
                        if user_choice.isdecimal():
                            if user_choice == "1":
                                recharge=input("请输入充值金额: ").strip()
                                if recharge.isdecimal():
                                    recharge = int(recharge)
                                    login_user['balance'] += recharge
                                    print(info)
                                    if login_user['balance'] < sum(temp_price_li):
                                        print("\033[1;31m余额不足,请继续充值!\033[0m")
                                        continue
                                    elif login_user['balance'] >= sum(temp_price_li):
                                        login_user['balance'] -= sum(temp_price_li)
                                        print("\033[1;32m支付成功,当前账户余额为: \033[0m%d" % login_user['balance'])
                                        settings.logger.info("user: %s,支付成功,当前账户余额为:%d"\
                                                              %(login_user['name'],login_user['balance']))
                                        return login_user
                            elif user_choice == "2":
                                if login_user['credit'] >= sum(temp_price_li):
                                    login_user['credit'] -= sum(temp_price_li)
                                    print("\033[1;32m支付成功,当前账户可用额度为: \033[0m%d" % login_user['credit'])
                                    settings.logger.info("user: %s,支付成功,当前账户可用额度为: %d" \
                                                         % (login_user['name'], login_user['balance']))
                                    return login_user
                                else:
                                    # print("\033[1;31m信用卡余额不足,请充值!\033[0m")
                                    settings.logger.warning("user: %s,信用卡余额不足,请充值!" % login_user['name'])
                                    flag = True
                            else:
                                print("请输入1或2选择支付方式!")
                                continue
                        else:
                            print("\033[1;31m输入不合法,请重新输入。\033[0m")
                            continue
                    else:
                        login_user['balance'] -= sum(temp_price_li)
                        print("\033[1;32m支付成功,当前账户余额为: \033[0m%d"%login_user['balance'])
                        settings.logger.info("user: %s,支付成功,当前账户余额为: %d" \
                                             % (login_user['name'], login_user['balance']))
                        return login_user
        else:
            print("\033[1;31m账号ID错误,连接银行失败!\033[0m")
    else:
        print("\033[1;31m输入不合法,连接银行失败!\033[0m")


def main(option):
    """
    功能: 方法调用
    该方法调用上面定义好的各函数，实现购物车的处理逻辑
    :return:
    """
    res = register_user()
    while True:
        menu_dic = {
            '1': show_goods,
            '2': shopping_car,
            '3': checkout
        }
        if option not in menu_dic:
            continue
        elif option == '1':
            print(" 商品类别 ".center(50, '*'))
            for i, ele in enumerate(shop_type, 1):
                print(i, ele)
            type_id = input("请输入类别id: ").strip()
            shop_type_list = show_goods_type(type_id)
            if shop_type_list:
                menu_dic[option](shop_type_list)  # 调用show_goods函数查看物品列表
        elif option == '2':     # 购物车
            menu_dic[option]()
        # elif option == '3':     # 注册
        #     menu_dic[option]()
        #     break
        elif option == "3":     # 结算
            save_user_info = checkout()
            if save_user_info:
                new_account_info = load_user_data()
                # print("更新前",new_account_info[login_user['id']])
                new_account_info[login_user['id']]['balance']=save_user_info['balance']
                new_account_info[login_user['id']]['credit']=save_user_info['credit']
                # print("更新后",new_account_info)
                json.dump(new_account_info, open(account_file, 'w',encoding='utf-8'),\
                          sort_keys=True,indent=4,ensure_ascii=False)
                break

if __name__ == "__main__":
    main()