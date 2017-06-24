#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

BASE_DIR=os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    os.pardir,
))
sys.path.append(BASE_DIR)

from server.ftpserver import main

if __name__ == '__main__':
    main()