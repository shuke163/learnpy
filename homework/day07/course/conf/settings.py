#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import logging

BASE_DIR=os.path.normpath(os.path.join(os.path.abspath(__file__),os.pardir,os.pardir))

DATABASE={
    'engine':'file',
    'path': os.path.join(BASE_DIR,'db'),
    'school_path': os.path.join(BASE_DIR,'db','school'),
    'teacher_path': os.path.join(BASE_DIR,'db','teacher'),
    'course_path': os.path.join(BASE_DIR,'db','course'),
    'classes_path': os.path.join(BASE_DIR,'db','classes'),
    'student_path': os.path.join(BASE_DIR,'db','student')
}


# '********Course-LOG********'

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'access': os.path.join(BASE_DIR,'logs','access.log'),
}

logger = logging.getLogger('Course-LOG')
logger.setLevel(logging.DEBUG)

# create file handler and set level to info
fh = logging.FileHandler(LOG_TYPES['access'],encoding='utf-8')
fh.setLevel(LOG_LEVEL)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s')

# add formatter to ch and fh
fh.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(fh)