#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os

BASE_DIR=os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    os.pardir
))
sys.path.append(BASE_DIR)

from core.admin import run
from core.main import *


if __name__ == '__main__':
    run()
