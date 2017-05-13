#!/usr/bin/python
# -*- coding:utf-8 -*-

import os, sys, json, re


shopping_car_list = []     # 定义一个全局的购物车列表

path = os.path.dirname(os.path.realpath(__file__))  # 获取当前目录
os.chdir(path + '/db')  # 进入当前目录，因为存储用户信息的数据库文件在当前目录下
f = open("user_info", "r+")  # 以读模式打开用户信息数据库文件
data = f.read()
f.close()
user_info = data.split()
# print(user_info)

def user_dict():
    """
    该方法返回一个字典，每个元素为字典形式，内容为用户、密码、余额
    :return: user_info_list
    """
    user_info_list = []
    for items in user_info:
        temp = items.split('|')
        user_dict = {
            'name': temp[0],
            'passwd': temp[1],
            'balance': temp[2]
        }
        user_info_list.append(user_dict)
    # print(user_info_list)
    return user_info_list


def username_list():
    """
    该方法返回一个列表，内容为所有的用户名
    :return: username:['jack','alex','shuke','tony']
    """
    username = []
    user_info_list = user_dict()
    for item in user_info_list:
        username.append(item['name'])
    # print(username)
    return username

user_info_list = user_dict()
user_list = username_list()

def login(username):
    """
    该方法返回一个字典，内容为登陆的用户名及余额
    :return: login_user: {'name':username,'balance':balance}
    """
    login_user = {}
    flag = False
    while not flag:
        pwd = input("请输入密码：").strip()
        for item in user_info_list:
            if username == item['name'] and pwd == item['passwd']:
                print("欢迎光临，祝%s购物愉快！" % username)
                login_user['name']=item['name']
                login_user['balance']=item['balance']
                # print(login_user)
                flag = True
                return login_user
            elif username == item['name'] and pwd != item['passwd']:
                print("密码输入错误，请重新输入密码！")
                continue

def register_user():
    """
    功能: 注册新用户
    :return: 
    """
    flag = False
    while not flag:
        choice = input("您输入的用户名不存在，是否要进行注册？yes|no: ").strip()
        if choice == "yes":
            flag = True
            # break
        elif choice == "no":
            exit("Bye Bye!")
        else:
            print("请输入：yes|no")
            continue
    else:
        print("免费注册！".center(50, '*'))
        while True:
            register = input("用户名：")
            if not register.isalnum():
                print("用户名不合法，必须是纯字母或字母和数字的组合。")
                continue
            register_pwd = input("输入密码: ").strip()
            register_pwd_again = input("请确认密码: ").strip()
            if register_pwd == register_pwd_again:
                fo = open("user_info", "a")
                fo.write("\n{0}|{1}|{2}".format(register, register_pwd, 0))
                fo.close()
                break
            elif register_pwd != register_pwd_again:
                print("密码不一致，请重新输入！")

def auth_login():
    """
    功能:认证登录函数
    该方法返回一个字典，内容为登陆的用户名及余额
    :return: login_user: {'name':username,'balance':balance}
    """
    while True:
        username = input("请输入用户名：").strip()
        if username in user_list:
            login_user = login(username)
            return login_user
        else:
            register_user()
            exit("新用户注册成功，请重新运行程序进行登录!")

def shopping_car():
    """
    功能:购物车函数
    该方法返回一个列表，内容为登陆的用户购买物品的信息
    :return: shopping_car_list: ['奇异果', '芒果']
    """
    with open('ShoppingWall','r',encoding='Utf-8') as jsonfile:
        shop_dict = json.load(jsonfile)             # 从json文件中读取商品清单，并序列化为shop_dict字典
    # print("清单： %s" % shop_dict)                 # 读取所有的商品
    print(" 商品类别 ".center(50,'*'))
    shop_type = list(shop_dict.keys())
    # print(shop_type)
    while True:
        for i, ele in enumerate(shop_type, 1):
            print(i, ele)
        choice_id = input("请输入类别id: ").strip()
        if choice_id.isdecimal():
            choice_id = int(choice_id)
            if 0 < choice_id <= len(shop_type):
                shop_type_list = shop_dict[shop_type[(choice_id-1)]]
                # print(shop_type_list)             # 商品类别对应的列表
                while True:
                    page_num = input("请输入页码： ").strip()
                    if page_num.isdecimal():
                        page_num = int(page_num)
                        total_page_num = (len(shop_type_list) // 10)
                        if 0 < page_num <= (total_page_num):
                            start_num = (page_num - 1) * 10
                            end_num = page_num * 10
                            shop_list = shop_type_list[start_num:end_num]
                            if page_num == 1:
                                id = 1
                            else:
                                id = (page_num-1) * 10 + 1
                            print("\033[1;32m%-14s %-14s %-4s\033[0m" % ("物品ID:", "商品名称:", "商品价格:"))
                            for item,ele in enumerate(shop_list,id):
                                print("%-15s %-15s %-5s" % (item,ele['name'],"$"+ele['price']))
                            break
                        else:
                            print("请输入1-%d之间的正整数" % (total_page_num))
                            continue
                    else:
                        print("对不起,输入不合法,请输入一个正整数!")
                        continue
                while True:
                    shop_id = input("请选择需要购买的物品id: ")
                    if shop_id.isdecimal():
                        shop_id = int(shop_id)
                        if 0 < shop_id <= len(shop_type_list):
                            if (float(login_user['balance'])-float(shop_type_list[(shop_id-1)]['price'])) >= 0:
                                login_user['balance'] = (float(login_user['balance'])-float(shop_type_list[(shop_id-1)]['price']))
                                shopping_car_list.append(shop_type_list[(shop_id-1)]['name'])
                                # print(shopping_car_list)      # 购买成功后的购物车列表
                                # print(login_user['balance'])  # 购买后用户的余额
                            else:
                                print("\033[1;31mINFO: 对不起，您的余额不足: %d\033[0m" % (float(login_user['balance'])-float(shop_type_list[(shop_id-1)]['price'])) )
                                choice = input("充值请按任意键, 继续浏览商品请输入(b), 退出请输入(q),请选择: ")
                                if choice == "b":
                                    break
                                elif choice == "q":
                                    with open('user_info','w') as userfile:
                                        for value in user_info_list:
                                            if value['name'] == login_user['name']:
                                                info = '{name}|{passwd}|{balance}'.format(name=value['name'],
                                                                                          passwd=value['passwd'],
                                                                                          balance=login_user['balance'])
                                                # print(info)
                                            else:
                                                info = '{name}|{passwd}|{balance}'.format(name=value['name'],
                                                                                          passwd=value['passwd'],
                                                                                          balance=value['balance'])
                                            userfile.write(info+'\n')
                                    print("欢迎下次光临，再见！")
                                    # print(shopping_car_list)              # 购物车列表
                                    return shopping_car_list
                                else:
                                    recharge = input("请输入充值金额: ")
                                    if recharge.isdecimal():
                                        login_user['balance']=(float(login_user['balance'])+float(recharge))
                                        print("当前余额为:{0} ".format(login_user['balance']))
                                    else:
                                        print("\033[1;31mERROR: 请输入数字!\033[0m")
                        else:
                            print("对不起，输入商品不存在，请重新输入!")
                    else:
                        print("对不起，输入不合法，请重新输入!")
                else:
                    print("对不起，输入不合法，请重新输入!")
            else:
                print("对不起，输入的id不存在，请重新输入!")
                continue
        else:
            print("对不起，输入不合法，请输入一个整数!")


def shop_history_to_file():
    '''
    功能: 购物记录保存至文件
    该方法用于序列化用户的购物记录到shop_history文件中
    :return:无返回
    '''
    shopping_car_list = shopping_car()
    if shopping_car_list:
        fp = open('shop_history', 'r+', encoding='utf-8')
        data = fp.read()
        fp.seek(0,0)
        if len(data) == 0 and len(shopping_car_list) > 0:
            shop_history_dict = {}
            shop_history_dict[login_user['name']] = shopping_car_list
            data = json.dump(shop_history_dict,fp,sort_keys=True, indent=4, ensure_ascii=False)
            print("嘿,%s,购物历史记录保存成功..." % login_user['name'])
            fp.close()
        else:
            shop_history_dict = json.load(fp)
            # print('history:%s'% shop_history_dict)        # 购物记录历史清单，从shop_history文件中读取
            fp.seek(0,0)
            if login_user['name'] in shop_history_dict.keys() and len(shopping_car_list) > 0:
                for items in shopping_car_list:
                    shop_history_dict[login_user['name']].append(items)
                data = json.dump(shop_history_dict,fp,sort_keys=True, indent=4, ensure_ascii=False)
                print("嘿,%s,购物历史记录保存成功..." % login_user['name'])
                fp.close()
            else:
                shop_history_dict[login_user['name']] = shopping_car_list
                data = json.dump(shop_history_dict, fp, sort_keys=True, indent=4, ensure_ascii=False)
                print("嘿,%s,购物历史记录保存成功..." % login_user['name'])
                fp.close()

def shop_query(username):
    '''
    功能: 购物记录查询
    该方法从shop_history文件中查询用户商品购买记录(模糊查询)
    :return:无返回
    '''
    record = input("请输入查询的商品名称: ").strip()
    fp = open('shop_history', 'r', encoding='utf-8')
    data = fp.read()
    fp.seek(0, 0)
    if len(data):
        shop_log = json.load(fp)
        # print(list(shop_log.keys()))          # 用户名作为key
        if username in list(shop_log.keys()):
            for items in shop_log[username]:
                if record in items:
                    print(items)
    else:
        print("对不起,用户%s无购买记录!" % username)

login_user=auth_login()
def main():
    """
    功能: 方法调用
    该方法调用上面定义好的各函数，实现购物车的处理逻辑
    :return:
    """
    shop_history_to_file()
    while True:
        choice = input("购物记录查询请输入(query): ,退出程序请输入(exit): ").strip()
        if choice == "query":
            shop_query(login_user['name'])
            break
        elif choice == "exit":
            exit("Bye Bye!")
        else:
            continue

if __name__ == "__main__":
    main()