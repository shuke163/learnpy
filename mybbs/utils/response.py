#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/10/4


class BaseResponse(object):
    def __init__(self):
        self.status = False
        self.data = None
        self.msg = None

    def get_dict(self):
        return self.__dict__