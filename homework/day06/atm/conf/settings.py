#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import logging

# BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR=os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    os.pardir,
))


DATABASE={
    'engine':'file',
    'path': "%s"%(os.path.join(BASE_DIR,'db'))
}

# 购物车信息文件
HISTORY_FILE = os.path.join(BASE_DIR, 'logs', 'shop_history')

# '********ATM-LOG********'

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'transaction': os.path.join(BASE_DIR,'logs','transactions.log'),
    'access': os.path.join(BASE_DIR,'logs','access.log'),
    'pay_log': os.path.join(BASE_DIR,'logs','pay.log')
}

logger = logging.getLogger('ATM-LOG')
logger.setLevel(logging.DEBUG)

# create console handler and set level to warning
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# create file handler and set level to info
fh = logging.FileHandler(LOG_TYPES['access'],encoding='utf-8')
fh.setLevel(logging.INFO)

# create file handler and set level to info
pay = logging.FileHandler(LOG_TYPES['pay_log'],encoding='utf-8')
pay.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s')

# add formatter to ch and fh
ch.setFormatter(formatter)
fh.setFormatter(formatter)
pay.setFormatter(formatter)

# add ch and fh to logger
logger.addHandler(ch)
logger.addHandler(fh)
logger.addHandler(pay)