#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

def query(content):
    '''
    功能: 根据用户传入的域名查找相关的配置信息，返回一个列表
    :param content: 用户输入的域名
    :return: data
    '''
    res_list = []
    content = 'backend %s' % content
    with open('haproxy.conf', 'r', encoding='utf-8') as fo:
        flag = False
        for line in fo:
            line = line.strip()
            if line.startswith('backend') and content == line:
                flag = True
                continue
            if flag:
                res_list.append(line)
                flag = False
                continue
        return res_list

def add(content):
    '''
    功能: 获取用户输入内容并写入文件
    :param content:
    :return:
    '''
    # 用于存放写入文件内容的列表
    data_list = []
    data_dic = eval(content)
    # print('转化为字典: ', data_dic)
    backend = data_dic.get('backend')
    server = data_dic.get('record')
    server_con = "server {} {} weight {} maxconn {}".format(server['server'], server['server'], server['weight'],
                                                            server['maxconn'])
    query_list = query(backend)
    if server_con in query_list:
        print('\033[1;31m内容已存在!\033[0m')
    else:
        ele = 'backend %s' % backend
        data_list.append(ele)
        data_list.append(server_con)
        with open('haproxy.conf','a+',encoding='utf-8') as fo:
            for item in data_list:
                if item.strip().startswith('backend'):
                    fo.write('\n')
                    fo.write("\n%s\n" % item)
                else:
                    fo.write('\t\t%s' % item)
            print('\033[1;32m写入成功!\033[0m')

def remove(content):
    """
    功能: 查找到用户输入的内容并删除
    :param content:
    :return:
    """
    data_dic = eval(content)
    backend_con = data_dic.get('backend')
    server_dic = data_dic.get('record')
    data = "server {} {} weight {} maxconn {}".format(server_dic['server'], server_dic['server'],
                                                      server_dic['weight'], server_dic['maxconn'])
    match = "backend %s" % backend_con
    data_list = query(backend_con)
    # print("query: ", data_list)
    if not data_list or data not in data_list:
        print("\033[1;31m内容不存在!\033[0m")
        return
    elif data in data_list:
        flag = False
        with open('haproxy.conf', encoding='utf-8') as read_f, open('ha.swap', 'w', encoding='utf-8') as write_f:
            for line in read_f:
                line = line.strip()
                if line.startswith('backend') and match == line:
                    flag = True
                    continue
                if flag and data == line:
                    flag = False
                    continue
                elif flag and data != line:
                    flag = False
                    write_f.write('%s\n' % match)
                if not flag:
                    write_f.write('%s\n' % line)
            print('删除成功!')
    os.rename("haproxy.conf","haproxy.conf_bak")
    os.rename("ha.swap","haproxy.conf")


if __name__ == '__main__':
    info = """
    1. 查询
    2. 增加
    3. 删除
    4. 退出
    """
    print(info)
    menu_dic = {
        '1': query,
        '2': add,
        '3': remove,
        '4': exit
    }
    while True:
        choice = input("请选择您需要操作的id: ").strip()
        if not choice or choice not in menu_dic: continue
        if choice == '4': break
        content = input("请输入内容: ").strip()
        # content = "{'backend': 'www.oldboy.org','record':{'server': '100.1.7.9','weight': 20,'maxconn': 300}}"
        # content = "www.oldboy.org"
        if choice == '1':
            res_list = menu_dic[choice](content)  # 用choice作为key，从字典中获取到对应的函数对象后加()，即调用函数，将content作为参数传入函数
            if res_list:
                print("\033[1;32m查询的结果为:\033[0m %s" % res_list)
            else:
                print("\033[1;31m未查找到内容\033[0m")
        else:
            menu_dic[choice](content)
