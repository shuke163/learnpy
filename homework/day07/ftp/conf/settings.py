#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Zhaofengfeng'

import os

BASE_DIR=os.path.normpath(os.path.join(os.path.abspath(__file__),os.pardir,os.pardir))

DATABASE={
    'engine':'file',
    'home_dir': os.path.join(BASE_DIR,'home'),
    'db_path': os.path.join(BASE_DIR,'db'),
    'user_db_file': os.path.join(BASE_DIR,'db','accounts.json')
}