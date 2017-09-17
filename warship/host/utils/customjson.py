#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/9/11

import json
from datetime import date
from datetime import datetime


class JsonCustomEncoder(json.JSONEncoder):
    """
    处理datetime格式数据
    """

    def default(self, field):
        if isinstance(field, datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)
