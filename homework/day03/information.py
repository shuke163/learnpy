#!/usr/bin/python
# -*- coding:utf-8 -*-

from prettytable import PrettyTable
import os

info = """
帮助:
    该程序目前只完成部分功能，后期需要进行优化处理...
    1.查询语言实例:
        a.删除仅支持根据id判断('>','<','=','<=','>=')以及limit关键字
        select * from db.emp limit 10
        select * from db.emp where id > 20
        select id,name,age from db.emp where id <= 15
    2.插入数据实例:
        insert into db.emp values Bigbang,22,17233786749,ops,2012-01-10
    3.更新实例:
        update db.emp set dept=Market where dept = IT(未完成)
    4.删除实例:
        a.删除仅支持根据id判断('>','<','=')以及like关键字
        delect from db.emp where id > 30
        delect from db.emp where id = 30
        delect from db.emp where name like 娟
"""
# print(info)

path = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.join(path, 'db')
os.chdir(pwd)
print('路径: {}'.format(os.getcwd()))

db_info = []  # 定义一个全局的数据库列表


def log(level, log):
    if level == "info":
        print("\033[1;32mINFO：{}\033[0m".format(log))
    elif level == "error":
        print("\033[1;31mERROR: {}\033[0m".format(log))
    else:
        print("未知错误级别")


def db_data():
    """
    功能: 读取db文件，并返回一个列表
    :return: db_info  列表每一个元素为字典，字典内容为每一行数据
    """
    db_info = []
    field_keys = ['id', 'name', 'age', 'phone', 'dept', 'enroll_data']
    with open('emp', 'r', encoding='utf-8') as db_file:
        data = db_file.readlines()
        # print(data)  # 读取文件生成列表
    for item in data:
        filed_values = item.strip().split(',')
        temp_dict = dict(zip(field_keys, filed_values))
        db_info.append(temp_dict)
        # print(db_info)
    return db_info

# 获取文件内容
# db_info = db_data()
# print(db_info)
# print(len(db_info))


# operation = "delect from db.emp where id > 30"

def where(*args):
    """
    以where关键字分割用户输入的字符串，以where关键字分割
    :param args: operation，用户输入的sql字符串
    :return: 返回一个字符串(where关键字后面的条件语句,无where返回None)
    """
    temp = args[0]
    if "where" in temp:
        condition = temp.partition('where')
        # print("condition",condition)
        return condition[2]     # 返回字符串
    elif "where" not in temp:
        condition = temp.split()
        # print("condition",condition)
        return condition        # 返回列表

# where条件过滤后返回的字符串或者列表
# where_str = where(operation)
# print("where_str: ",where_str)

# 根据条件判断分割后返回列表
def judge():
    """
    将where子句后面的条件取出，以空格分割，返回列表的形式
    :return: temp_con
    """
    keys_list = ['and','like','limit','not','or']
    for item in keys_list:
        if item in where_str:
            temp_con = where_str.strip().split()
            # print("在 judge 函数中: ", temp_con)
            return temp_con
    if isinstance(where_str,list):
        temp_con = where_str
        # print("在 judge 函数中: ", temp_con)
        return temp_con
    else:
        temp_con = where_str.strip().split()
        # print("在 judge 函数中: ", temp_con)
        return temp_con

# judge()
def show_result(show_list):
    """
    功能: 用于展示输出的结果
    :param show_list: 列表
    :return: 展示表格的一个对象
    """
    # print(show_list)
    show = []
    x = PrettyTable(["id", "name", "age", "phone", "dept", "enroll_data"])
    x.align['id'] = "1"
    x.padding_width = 1
    for ele in show_list:
        show.append(ele['id'])
        show.append(ele['name'])
        show.append(ele['age'])
        show.append(ele['phone'])
        show.append(ele['dept'])
        show.append(ele['enroll_data'])
        x.add_row(show)
        # print(show)
        show.clear()
    return x

# tab = show_result(db_info)
# print(tab)
def id_or_age(select_sql):
    """
    功能: 根据id和age作为where条件来输出
    :param select_sql: 列表
    :return: 无返回
    """
    if select_sql[5] == "id" or select_sql[5] == "age":
        result = []
        num = int(select_sql[7])
        if select_sql[6] == ">":
            for item in db_info:
                if int(item[select_sql[5]]) > num:
                    result.append(item)
        elif select_sql[6] == "<":
            for item in db_info:
                if int(item[select_sql[5]]) < num:
                    result.append(item)
        elif select_sql[6] == "=":
            for item in db_info:
                if int(item[select_sql[5]]) == num:
                    result.append(item)
        elif select_sql[6] == ">=":
            for item in db_info:
                if int(item[select_sql[5]]) >= num:
                    result.append(item)
        elif select_sql[6] == "<=":
            for item in db_info:
                if int(item[select_sql[5]]) <= num:
                    result.append(item)
        print("=" * 50)
        print(result)
        show_tab = show_result(result)  # 将查询得到的列表传入show_result函数格式化输出展示
        print(show_tab)
        print("select successful,total %d rows;" % len(result))


def insert(operation):
    """
    功能: 检验数据合法性，并将数据写入db文件
    :return:无
    """
    insert_data = operation.split(" ")
    # print(insert_data)
    data = insert_data[4]
    len_data = data.split(',')
    if len(len_data) == 5:
        content = ("\n%d,%s" % (int(len(db_info)+1), data))
        print(content)
        print(content.strip().split(','))
        with open('emp', 'a+', encoding='utf-8') as db_file:
            db_file.write(content)
        log("info", "数据写入成功!")
        # db_info = db_data()
    else:
        log("error", "请检查您的sql语句,参数错误,eg: insert into db.emp values Eric,22,17233786749,opt,2012-01-10")

# insert(operation)

def delect(*where_list):
    """
    功能: 根据id和like关键字判断进行删除文件内容
    :param where_list: judge()函数--->temp_con列表
    :return: db_to_file
    """
    delect_ele = []    # 定义一个空列表，用于存放需要删除的数据
    db_to_file = []    # 定义一个空列表，用于存放需要保存的数据
    # print('where_list',where_list)
    sql_list = list(where_list)
    # print("where后面的条件为: ",sql_list)
    # 处理条件为空的情况
    if len(sql_list) == 0 and operation.endswith("db.emp"):
        with open('emp.bak', 'r+', encoding='utf-8') as db_file:
            db_file.truncate()
        delect_ele = db_info
        return db_to_file,delect_ele
    # 根据'id'进行处理
    elif 'id' in sql_list:
        if 'id' in sql_list:
            id_index = sql_list.index('id')
        temp = sql_list[id_index:(id_index + 3)]
        # print(temp)
        id_num = int(temp[2])
        # 大于的情况
        if temp[1] == ">":
            for item in db_info:
                if int(item['id']) > id_num:
                    split_index = db_info.index(item)
                    # print(split_index)
                    db_to_file = db_info[0:split_index]
                    delect_ele = db_info[split_index:]
                    break
            return db_to_file, delect_ele                       # 以元组的形式返回2个列表
        # 等于的情况
        elif temp[1] == "=":
            for item in db_info:
                if int(item['id']) == id_num:
                    db_info.remove(item)
                    db_to_file = db_info
                    delect_ele = item
                    break
            return db_to_file, delect_ele  # 以元组的形式返回2个列表
        # 小于的情况
        elif temp[1] == "<":
            for item in db_info:
                if int(item['id']) == id_num:
                    split_index = db_info.index(item)
                    print(split_index)
                    # db_to_file = db_info[0:split_index]
                    db_to_file = db_info[split_index:]
                    delect_ele = db_info[0:split_index]
                    break
            return db_to_file, delect_ele                       # 以元组的形式返回2个列表
    # 根据like处理关键字的情况
    elif 'like' in sql_list:
        id_index = sql_list.index('like')
        temp = sql_list[(id_index-1):(id_index + 2)]
        print("like 匹配的字符串: ",temp)
        for item in db_info:
            if temp[2] in item[temp[0]]:
                delect_ele.append(item)
            else:
                db_to_file.append(item)
        return db_to_file, delect_ele                       # 以元组的形式返回2个列表

# delect(*judge())

def update(where_con):
    """
    功能: 更新文档内容
    :param where_con: where条件,where_str字符串
    :return:
    """

def select():
    """
    功能: 查询文件内容，支持id或age字段作为过滤条件
    :return: 无
    """
    field = []
    # 根据空格分隔用户输入
    select_sql = operation.strip().split()
    # print("select语句分割: ",select_sql)
    print("*" * 80)
    # 查询所有
    if "*" in select_sql and select_sql[-1].endswith("db.emp"):
        show_tab = show_result(db_info)
        print(show_tab)
        print("select successful,total %d rows;" % len(db_info))
    # limit过滤
    elif "*" in select_sql and "limit" in select_sql[4]:
        temp_num = int(select_sql[5])
        result_list = db_info[0:temp_num]
        show_tab = show_result(result_list)
        print(show_tab)
        print("select successful,total %d rows;" % temp_num)
    # 根据id和age来处理
    elif select_sql[1] == "*" and "where" in select_sql:
        if select_sql[5] == "id" or select_sql[5] == "age":
            id_or_age(select_sql)

    # 处理查询指定字段的逻辑
    elif select_sql[1] != "*":
        temp = select_sql[1]
        # print('temp: ', temp)
        if operation.endswith("db.emp"):
            field = temp
        elif "where" in operation:
            field = select_sql[4:]
            # print("sql_field:",field )
            field = temp.split(',')+field
        # print("根据逗号分割后的列表为:",field)
        index_n = field.index("where")
        temp_field = field[0:index_n]
        # print("temp_field:",temp_field)
        #根据id和age来处理
        if select_sql[5] == "id" or select_sql[5] == "age":
            x = PrettyTable(temp_field)
            x.align['id'] = "1"
            x.padding_width = 1
            temp_list = []          # 存放查询结果的列表
            ele_dict = {}
            num = int(select_sql[7])
            if select_sql[6] == ">":
                for item in db_info:
                    if int(item[select_sql[5]]) > num:
                        for i in temp_field:
                            ele_dict[i] = item[i]
                            temp_list.append(ele_dict[i])
                            # print("排序后: ",temp_list)
                        x.add_row(temp_list)
                        temp_list.clear()
                print(x)
            elif select_sql[6] == "<":
                for item in db_info:
                    if int(item[select_sql[5]]) < num:
                        for i in temp_field:
                            ele_dict[i] = item[i]
                            temp_list.append(ele_dict[i])
                            # print("排序后: ",temp_list)
                        x.add_row(temp_list)
                        temp_list.clear()
                print(x)
            elif select_sql[6] == "=":
                for item in db_info:
                    if int(item[select_sql[5]]) == num:
                        for i in temp_field:
                            ele_dict[i] = item[i]
                            temp_list.append(ele_dict[i])
                            # print("排序后: ",temp_list)
                        x.add_row(temp_list)
                        temp_list.clear()
                print(x)
            elif select_sql[6] == ">=":
                for item in db_info:
                    if int(item[select_sql[5]]) >= num:
                        for i in temp_field:
                            ele_dict[i] = item[i]
                            temp_list.append(ele_dict[i])
                            # print("排序后: ",temp_list)
                        x.add_row(temp_list)
                        temp_list.clear()
                print(x)
            elif select_sql[6] == "<=":
                a = []
                for item in db_info:
                    if int(item[select_sql[5]]) <= num:
                        for i in temp_field:
                            ele_dict[i] = item[i]
                            temp_list.append(ele_dict[i])
                            # print("排序后: ",temp_list)
                        x.add_row(temp_list)
                        temp_list.clear()
                print(x)
            else:
                log('info','查询的条件不成立,请检查!')


def chang_to_file(to_do):
    """
    功能: 将删除delect函数返回的列表写入db文件中
    :param to_do: delect()函数返回的列表,列表共2个元素，元素1:需要写入文件的数据，元素2：删除的数据
    :return:
    """
    # print('to_file: ', to_do)
    if not to_do:
        to_file = None
        show_out = None
    else:
        to_file = to_do[0]  # 需要写回文件的列表数据
        show_out = to_do[1]  # 需要删除的列表数据
        # print('删除内容：', show_out)
        if to_file:
            with open("emp", 'w', encoding='utf-8') as fo:
                for i in to_file:
                    to_file_str = "{id},{name},{age},{phone},{dept},{enroll_data}\n".format(id=i['id'],
                                                                                            name=i['name'], age=i['age'],
                                                                                            phone=i['phone'],
                                                                                            dept=i['dept'],
                                                                                            enroll_data=i['enroll_data'])
                    # print(to_file_str)
                    fo.write(to_file_str)
    x = PrettyTable(["id", "name", "age", "phone", "dept", "enroll_data"])
    x.align['id'] = "1"
    x.padding_width = 1
    table_list = []             # 定义一个空列表，存放行信息
    if isinstance(show_out,list):
        if not show_out:
            log('info','没有匹配到对应的条件!')
        else:
            tab = show_result(show_out)         # 调用show_result函数输出
            print(tab)
            print("delect successful,total %d rows;" % len(show_out))
    elif isinstance(show_out,dict):
            table_list.append(show_out['id'])
            table_list.append(show_out['name'])
            table_list.append(show_out['age'])
            table_list.append(show_out['phone'])
            table_list.append(show_out['dept'])
            table_list.append(show_out['enroll_data'])
            x.add_row(table_list)
            table_list.clear()
            print(x)
            print("delect successful,total 1 rows;")
    elif not to_file:
        tab = show_result(db_info)          # 调用show_result函数输出
        print(tab)
        print("delect successful,total %d rows" % len(db_info))
    elif not show_out:
        log('error','条件不成立，请检查!')

# chang_to_file(delect(*judge()))


if __name__ == '__main__':
    while True:
        choice = """
        1. 查询(select)
        2. 插入(insert)
        3. 更新(update)
        4. 删除(delect)
        """
        print(choice)
        user_choice = input("请输入您的选择,帮助(h/H),退出(exit): ").strip()
        #
        # print(where_str)
        try:
            if user_choice.isdigit():
                user_choice = int(user_choice)
                operation = input("sql> ")
                db_info = db_data()
                where_str = where(operation)
                if user_choice == 1:
                    select()
                elif user_choice == 2:
                    insert(operation)
                elif user_choice == 3:
                    pass
                elif user_choice == 4:
                    chang_to_file(delect(*judge()))
                else:
                    log('error','请选择1-4')
            elif user_choice.lower() == 'h':
                print(info)
            elif user_choice.lower() == 'exit':
                exit("Bye Bye!")
            else:
                    log('error','请输入您的选择!')
        except AttributeError as e:
            log('error','请重新输入!')