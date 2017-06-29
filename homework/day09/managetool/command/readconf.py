#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/6/27 0027

from conf.settings import DATABASE
import configparser

host_file=DATABASE['host_path']

class Handle_conf:
    """
    处理配置文件，获取主机信息
    """
    def __init__(self,confname):
        self.confname=confname
        self.conf = configparser.ConfigParser()
        self.conf.read(self.confname,encoding='utf-8')

    def get_all_node(self):
        node = self.conf.sections()
        return node

    def get_all_key(self,node):
        if self.conf.has_section(node):
            key = self.conf.options(node)
            return key
        else:
            print('%s not found'%node)

    def get_all_info(self,node):
        if self.conf.has_section(node):
            info_l = self.conf.items(node)
            return info_l
        else:
            print('%s not found' % node)

    def get_value_of_key(self,node,key):
        if self.conf.has_option(node,key):
            value = self.conf.get(node,key)
            return value
        else:
            print('%s not found' % key)

#
# h=Handle_conf(host_file)
# res = h.get_all_info('db')
# res1 = h.get_all_key('host')
# print(res)
# print(res1)


