#!/usr/bin/python
# -*- coding:utf-8 -*-

goods = [
    {"name": "电脑", "price": 1999},
    {"name": "鼠标", "price": 10},
    {"name": "游艇", "price": 20},
    {"name": "美女", "price": 998},
]

shopping_list = []                                # 购物车列表

while True:
    deposit = input("请输入您的总资产: ")
    if deposit.isdigit():                         # 判断用户输入是否是数字
        deposit = int(deposit)                    # 转化为整数
        while True:
            for index, item in enumerate(goods):  # 循环迭代打印商品清单
                print(index, item['name'])
            serial_num = input("请输入物品编号: ")
            if serial_num.isdigit():              # 判断用户输入的物品编号是否是数字
                serial_num = int(serial_num)      # 转化为整数
                if (serial_num >= 0) and (serial_num < len(goods)):         # 判断用户输入物品编号是否在物品清单中
                    if (deposit - goods[serial_num]['price']) >= 0:         # 判断余额是否足够
                        deposit = (deposit - goods[serial_num]['price'])    # 扣钱
                        shopping_list.append(goods[serial_num]['name'])     # 购买成功加入购物车列表
                    else:                                                   # 余额不足逻辑处理
                        print("\033[1;31mINFO: 对不起，您的余额不足：%d\033[0m" % (deposit - goods[serial_num]['price']))  # 输出余额
                        choice = input("充值请输入: 1, 继续浏览商品请按任意键, 退出请输入: q, 请选择: ")                       # 余额不足情况逻辑处理
                        if choice == '1':                                                                               # 用户进行充值
                            recharge = input("请输入充值金额: ")
                            if recharge.isdigit():
                                deposit = (deposit + int(recharge))                                                     # 将充值金额加入账户资产中
                                # print(deposit)
                        elif choice == "q":
                            print("您已经购买的商品清单是: %s" % (shopping_list))                                          # 退出程序并打印购物车清单
                            exit()
                        else:
                            continue                                                                                    # 继续选择物品清单
                else:
                    print("\033[1;31mINFO: 对不起,您输入的商品编号不存在!\033[0m")
            else:
                print("\033[1;31mERROR: 对不起，请输入商品编号!\033[0m")
    else:
        print("\033[1;31mERROR: 请输入数字!\033[0m")
