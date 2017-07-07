#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/6/27 0027

import os
import logging

# BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR=os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    os.pardir,
))


DATABASE={
    'engine':'file',
    'host_path': "%s"%(os.path.join(BASE_DIR,'conf','host.ini'))
}

# ssh 远程访问端口
SSHPORT = 63008

# 执行命令log
# '********COM-LOG********'

LOG_LEVEL = logging.INFO
LOG_TYPES = {
    'result': os.path.join(BASE_DIR,'logs','result.log'),
}

logger = logging.getLogger('COM-LOG')
logger.setLevel(logging.DEBUG)

# create file handler and set level to info
fh = logging.FileHandler(LOG_TYPES['result'],encoding='utf-8')
fh.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s')

# add formatter to fh
fh.setFormatter(formatter)

# add fh to logger
logger.addHandler(fh)
