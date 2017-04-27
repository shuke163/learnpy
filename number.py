#!/usr/bin/python
# -*- coding:utf-8 -*-

v1 = [11, 22, 33, 44, 55, 66, 77, 88, 99, 90]
min_num = []                             # 创建小于66的列表
max_num = []                             # 创建大于66的列表
dict_list = {}                           # 创建空字典用于存放数据
for item in v1:
    if item < 66:                        # 判断是否小于66
        min_num.append(item)             # 加入列表
    else:
        max_num.append(item)             # 其他情况添加至大于66的列表中

dict_list['k1'] = min_num                # 添加小于66的列表至字典
dict_list['k2'] = max_num                # 添加大于66的列表至字典
print(dict_list)