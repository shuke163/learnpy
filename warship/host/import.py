#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/9/15

from host.models import *

li = []
for i in range(2,102):
    li.append(models.Hosts(hostname='nginx' + str(i) + 'com.cn',private_ip='192.168.1.' + str(i),public_ip='112.112.112.'+str(i),os="ubuntu 16.4",cpu='4 core',mem='8G',disk=str(i) + 'G',service_id='1',idc_id='2',status_id='3',owner_id='3'))
models.Hosts.objects.bulk_create(li)

