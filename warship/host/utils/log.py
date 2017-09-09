#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/9/4
from warship import settings

import os
import logging

BASE_DIR = settings.BASE_DIR

LOG_LEVEL = logging.INFO
LOG_TYPE = {
    'access': os.path.join(BASE_DIR,'logs','access.log'),
}

logger = logging.getLogger("AppHost")
logger.setLevel(logging.DEBUG)

# create file handler and set level to info
fh = logging.FileHandler(LOG_TYPE['access'],encoding='utf-8')
fh.setLevel(LOG_LEVEL)

# set formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s: %(message)s')

# add formatter to fh
fh.setFormatter(formatter)

# add fh to logger
logger.addHandler(fh)



