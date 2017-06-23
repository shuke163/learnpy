#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import pickle
import uuid
from conf.settings import DATABASE

school_path = DATABASE['school_path']
teacher_path = DATABASE['teacher_path']
course_path = DATABASE['course_path']
classes_path = DATABASE['classes_path']
student_path = DATABASE['student_path']


class BaseModule:
    """
    基准类
    """

    def save(self, save_path,nid):
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        pickle.dump(self, open(os.path.join(save_path,nid), 'wb'))

    @classmethod
    def get_all_obj(cls, type_path):
        type_info = []
        all_file_li = os.listdir(type_path)
        for file_name in all_file_li:
            res = pickle.load(open(os.path.join(type_path, file_name), 'rb'))
            type_info.append(res)
        return type_info

    def create_uuid(self):
        return str(uuid.uuid1())


class School(BaseModule):
    """
    学校类
    """

    def __init__(self, name, city, addr):
        self.school_nid = self.create_uuid()
        self.name = name
        self.city = city
        self.addr = addr

    def __str__(self):
        return self.name


class Teacher(BaseModule):
    """
    讲师类
    """

    def __init__(self, name, age, sex, schood_id):
        self.tea_nid = self.create_uuid()
        self.name = name
        self.age = age
        self.sex = sex
        self.school_id = schood_id

    def __str__(self):
        return self.name


class Course(BaseModule):
    '''
    课程类
    '''

    def __init__(self, name, price, cycle, school_id):
        self.cou_nid = self.create_uuid()
        self.name = name
        self.price = price
        self.cycle = cycle
        self.school_id = school_id

    def __str__(self):
        return self.name


class Classes(BaseModule):
    '''
    班级类
    '''

    def __init__(self, name, semster, cou_name, start_time, tea_id):
        self.cla_nid = self.create_uuid()
        self.name = name
        self.semster = semster
        self.cou_name = cou_name
        self.start_time = start_time
        self.tea_id = tea_id

    def __str__(self):
        return self.name


class Student(BaseModule):
    '''
    学员类
    '''

    def __init__(self, name, age, sex, school_id, cla_id):
        self.stu_nid = self.create_uuid()
        self.name = name
        self.age = age
        self.sex = sex
        self.school_id = school_id
        self.cla_id = cla_id

        # def __str__(self):
        #     return self.name


s1 = School('老男孩', '北京', '昌平区沙河')
# print(s1)
# s1.save(school_path,s1.school_nid)
s2 = School('Oldboy', '上海', '五棵松体育馆')
# s2.save(school_path,s2.school_nid)
# print(s2)

t1 = Teacher('shuke', 18, 'male', s1.school_nid)
t2 = Teacher('jack', 19, 'women', s2.school_nid)
# t1.save(teacher_path,t1.tea_nid)
# t2.save(teacher_path,t2.tea_nid)

cou1 = Course('Linux', 3000, 3, s1.school_nid)
cou2 = Course('Python', 4000, 4, s1.school_nid)
cou3 = Course('Go', 5000, 5, s2.school_nid)
# cou1.save(course_path,cou1.cou_nid)
# cou2.save(course_path,cou2.cou_nid)
# cou3.save(course_path,cou3.cou_nid)

cla3 = Classes('s1-16', '16', 'Python', '2017-01-00', t1.tea_nid)
cla1 = Classes('s1-17', '17', 'Python', '2017-01-01', t1.tea_nid)
cla2 = Classes('s1-18', '18', 'Linux', '2017-01-02', t1.tea_nid)
# print(cla1.cla_nid)
# cla1.save(classes_path,cla1.cla_nid)
# cla2.save(classes_path,cla2.cla_nid)
# cla3.save(classes_path,cla3.cla_nid)

stu1 = Student('dave', 20, 'male', s1.school_nid, cla1.cla_nid)
stu2 = Student('jack', 20, 'male', s1.school_nid, cla2.cla_nid)
# print(stu1.cla_id)
# stu1.save(student_path,stu1.stu_nid)
# stu2.save(student_path,stu2.stu_nid)