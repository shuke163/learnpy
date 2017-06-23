#!/usr/bin/env python
# -*- coding:utf-8 -*-

from core.main import *
import os
import time

class Tea_view():
    """
    讲师管理试图
    """

    def __init__(self):
        tea_info = """
        1. 选择班级
        2. 查看学员列表
        3. 修改学员成绩
        4. 退出
        """
        print(tea_info)

    @staticmethod
    def action():
        menu_dic = {
            '1': Tea_view.choose_cla,
            '2': Tea_view.show_student,
            '3': Tea_view.change_record,
        }
        while True:
            choice = input('请选择: ').strip()
            if not choice: continue
            if choice.isdecimal() and choice in menu_dic:
                menu_dic[choice]()
            elif choice == '4':
                print("\033[1;32m再见!\033[0m")
                break

    @staticmethod
    def choose_cla():
        cla_obj = Classes.get_all_obj(classes_path)
        for i, item in enumerate(cla_obj, 1):
            print(i, item)
        choice_cla = input("请输入选择上课的班级ID: ").strip()
        if choice_cla.isdecimal():
            choice_cla = int(choice_cla)
            if 0 < choice_cla <= len(cla_obj):
                print("\033[1;32m老湿,快去%s上课吧,同学们都在等你呢!\033[0m" % cla_obj[choice_cla - 1])

    @staticmethod
    def show_student():
        stu_obj = Student.get_all_obj(student_path)
        print("\033[1;32mid\t\t姓名\t\t年龄\033[0m")
        for i, item in enumerate(stu_obj, 1):
            print("{}\t\t{}\t\t{}".format(i, item.name, item.age))

    @staticmethod
    def change_record():
        stu_dic = {}
        stu_obj = Student.get_all_obj(student_path)
        for item in stu_obj:
            temp_dic = {
                item.name: item.stu_nid,
            }
            stu_dic.update(temp_dic)
        # print(stu_dic)        # 获取学员名称及
        print("\033[1;35mID\t\tname\033[0m")
        for i, keys in enumerate(stu_dic.keys(), 1):
            print("{}\t\t{}".format(i, keys))
        choice_id = input("请选择学员ID: ").strip()
        if choice_id.isdecimal():
            choice_id = int(choice_id)
            name_li = list(stu_dic.keys())
            stu_name = name_li[choice_id - 1]
            if 0 < choice_id <= len(stu_dic):
                print("修改前,该学员的成绩为: 10分")  # BUG需要处理,下面需将修改后的信息pickle.dump到对应的学员文件中保存修改
                change_record = input("请输入修改后的分数: ").strip()
                if change_record.isdecimal():
                    change_record = int(change_record)
                    if 0 < change_record <= 150:
                        for item in stu_obj:
                            if item.name == stu_name:
                                item.stu_record = change_record
                                print("\033[1;32m修改后,该学员的成绩为: %d分\033[0m" % item.stu_record)
                    else:
                        print("\033[1;31m请输入1-150之间的一个数字\033[0m")


class Stu_view():
    """
    学员试图
    """

    def __init__(self):
        stu_info = """
        1. 注册
        2. 交学费
        3. 选择班级
        4. 退出
        """
        print(stu_info)

    @staticmethod
    def action():
        menu_dic = {
            '1': Stu_view.register,
            '2': Stu_view.pay_tuition,
            '3': Stu_view.choose_cla,
        }
        while True:
            choice = input('请选择: ').strip()
            if not choice: continue
            if choice.isdecimal() and choice in menu_dic:
                menu_dic[choice]()
            elif choice == '4':
                print("\033[1;32m再见!\033[0m")
                break

    @staticmethod
    def register():
        name = input("请输入姓名: ").strip()
        age = input("请输入年龄: ").strip()
        sex = input("请输入性别: ").strip()
        school_obj = School.get_all_obj(school_path)
        for i, item in enumerate(school_obj, 1):
            print(i, item)
        school_id = input("请输入学校ID: ").strip()
        if school_id.isdecimal():
            school_id = int(school_id)
            if 0 < school_id <= len(school_obj):
                cla_obj = Classes.get_all_obj(classes_path)
                for i, item in enumerate(cla_obj, 1):
                    print(i, item)
                cla_id = input("请输入班级ID: ").strip()
                if cla_id.isdecimal():
                    cla_id = int(cla_id)
                    if 0 < cla_id <= len(cla_obj):
                        new_stu_obj = Student(name, age, sex, school_obj[school_id - 1].school_nid,
                                              cla_obj[cla_id - 1].cla_nid)
                        print("正在保存,请稍等...")
                        new_stu_obj.save(student_path, new_stu_obj.stu_nid)
                        time.sleep(5)
                        if os.path.isfile(os.path.join(school_path, new_stu_obj.stu_nid)):
                            print("\033[1;32m注册成功!\033[0m")
                            # else:
                            #     print("\033[1;31m注册失败!\033[0m")
                    else:
                        print("请输入1-%s之间的整数!" % len(cla_obj))
                else:
                    print("输入不合法,请输入一个正整数!")
            else:
                print("请输入1-%s之间的整数!" % len(school_obj))
        else:
            print("输入不合法,请输入一个正整数!")

    @staticmethod
    def pay_tuition():
        stu_name = []
        stu_obj = Student.get_all_obj(student_path)
        for i, item in enumerate(stu_obj, 1):
            stu_name.append(item.name)
            # print(i,item)
        print(stu_name)
        user_name = input("请输入您的姓名: ").strip()
        if user_name in stu_name:
            for item in stu_obj:
                if user_name == item.name:
                    file_name = item.cla_id
                    # print("file_name",file_name)      # 获取学员对应的班级文件名,即cla_nid,
                    res = pickle.load(open(os.path.join(classes_path, file_name), 'rb'))  # 加载班级数据到内存中
                    # print(res.cou_name)
                    cou_obj = Course.get_all_obj(course_path)  # 获取课程对象
                    for item in cou_obj:
                        if res.cou_name == item.name:
                            print('费用: %d' % item.price)  # 输出课程价格
                            price_num = input("收取费用: ").strip()
                            if price_num.isdecimal():
                                price_num = int(price_num)
                                if price_num == item.price:
                                    print("\033[1;32m缴费成功!\033[0m")
                                elif price_num != item.price:
                                    print("\033[1;31m您应该缴费: %d元人民币\033[0m" % item.price)
        else:
            print("\033[1;31m用户不存在!\033[0m")

    @staticmethod
    def choose_cla():
        cla_obj = Classes.get_all_obj(classes_path)
        for i, item in enumerate(cla_obj, 1):
            print(i, item)
        choice = input("请输入选择的班级: ")
        if choice.isdecimal():
            choice = int(choice)
            if 0 < choice <= len(cla_obj):
                print("\033[1;32m你选择的班级是: %s\033[0m" % (cla_obj[choice - 1]))


class Admin_view():
    """
    管理员试图
    """

    def __init__(self):
        admin_info = """
        1. 创建讲师
        2. 创建班级
        3. 创建课程
        4. 退出
        """
        print(admin_info)

    @staticmethod
    def action():
        menu_dic = {
            '1': Admin_view.create_teacher,
            '2': Admin_view.create_classes,
            '3': Admin_view.create_course,
        }
        while True:
            choice = input('请选择: ').strip()
            if not choice: continue
            if choice.isdecimal() and choice in menu_dic:
                menu_dic[choice]()
            elif choice == '4':
                print("\033[1;32m再见!\033[0m")
                break

    @staticmethod
    def create_teacher():
        while True:
            tea_name = input("请输入讲师姓名: ").strip()
            if not tea_name: continue
            tea_age = input("请输入讲师年龄: ").strip()
            if not tea_age: continue
            if tea_age.isdecimal():
                tea_age = int(tea_age)
            else:
                print("\033[1;31m请输入一个数字!\033[0m")
                continue
            tea_sex = input("请输入讲师性别: ").strip()
            if not tea_age: continue

            school_obj = School.get_all_obj(school_path)
            # school_obj_li = []
            for i, item in enumerate(school_obj, 1):
                print(i, item)
            school_id = input("请输入学校ID: ").strip()
            if not school_id: continue
            if school_id.isdecimal():
                school_id = int(school_id)
                if 0 < school_id <= len(school_obj):
                    school_nid = school_obj[school_id - 1].school_nid
                    # print("学校对应的文件名，即school_nid", school_nid)
                    new_teacher_obj = Teacher(tea_name, tea_age, tea_sex, school_nid)
                    new_teacher_obj.save(teacher_path, new_teacher_obj.tea_nid)
                    print("\033[1;32m讲师创建成功!\033[0m")
                    break
            else:
                print("\033[1;31m请输入一个数字!\033[0m")
                continue

    @staticmethod
    def create_classes():
        while True:
            cla_name = input("请输入班级名称: ").strip()
            if not cla_name: continue
            cla_semster = input("请输入学期: ").strip()
            if not cla_semster: continue
            if cla_semster.isdecimal():
                cla_semster = int(cla_semster)
            else:
                print("\033[1;31m请输入一个数字!\033[0m")
                continue
            course_obj = Course.get_all_obj(course_path)
            for i, item in enumerate(course_obj, 1):
                print(i, item)
            cou_id = input("请输入课程ID: ").strip()
            if not cou_id: continue
            if cou_id.isdecimal():
                cou_id = int(cou_id)
                course_name = course_obj[cou_id - 1].name
                # print("课程名称: ",course_name)
            start_time = input("请输入开课日期,如2017-02-02: ").strip()
            if not start_time: continue
            teacher_obj = Teacher.get_all_obj(teacher_path)
            for i, item in enumerate(teacher_obj, 1):
                print(i, item)
            tea_nid = input("请输入讲师ID: ").strip()
            if tea_nid.isdecimal():
                tea_nid = int(tea_nid)
                if 0 < tea_nid <= len(teacher_obj):
                    teacher_nid = teacher_obj[tea_nid - 1].tea_nid
                    new_cla_obj = Classes(cla_name, cla_semster, course_name, start_time, teacher_nid)
                    new_cla_obj.save(classes_path, new_cla_obj.cla_nid)
                    print("\033[1;32m班级创建成功!\033[0m")
                    break
            else:
                print("\033[1;31m请输入一个数字!\033[0m")
                continue

    @staticmethod
    def create_course():
        while True:
            cou_name = input("请输入课程名称: ").strip()
            if not cou_name: continue
            cou_price = input("请输入课程价格: ").strip()
            if not cou_price: continue
            if cou_price.isdecimal():
                cou_price = int(cou_price)
            else:
                print("\033[1;31m请输入一个数字!\033[0m")
                continue
            cou_cycle = input("请输入课程周期: ").strip()
            if not cou_cycle: continue
            if cou_cycle.isdecimal():
                cou_cycle = int(cou_cycle)
            else:
                print("\033[1;31m请输入一个数字!\033[0m")
                continue

            school_obj = School.get_all_obj(school_path)
            for i, item in enumerate(school_obj, 1):
                print(i, item)
            school_id = input("请输入学校ID: ").strip()
            if school_id.isdecimal():
                school_id = int(school_id)
                if 0 < school_id <= len(school_obj):
                    school_nid = school_obj[school_id - 1].school_nid
                    new_cou_obj = Course(cou_name, cou_price, cou_cycle, school_nid)
                    # print(new_cou_obj.name, new_cou_obj.price, new_cou_obj.cycle, new_cou_obj.school_id)  # 新创建的课程对象信息
                    new_cou_obj.save(course_path, new_cou_obj.cou_nid)
                    print("\033[1;32m课程创建成功!\033[0m")
                    break
            else:
                print("\033[1;31m请输入一个数字!\033[0m")
                continue


def run():
    """
    启动入口函数
    :return:
    """
    info = """
    \033[1;32m\t1. 管理系统\033[0m
    \033[1;35m\t2. 讲师系统\033[0m
    \033[1;36m\t3. 学生系统\033[0m
    \033[1;37m\t4. 退出\033[0m
    """
    print('*' * 50)
    print(info)
    print('*' * 50)
    choice = input('请输入您的选择: ').strip()
    if choice.isdecimal():
        if choice == "1":
            Admin_view()
            Admin_view.action()
        elif choice == "2":
            Tea_view()
            Tea_view.action()
        elif choice == "3":
            Stu_view()
            Stu_view.action()
        elif choice == "4":
            quit()


# if __name__ == '__main__':
#     run()
