#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/8/13 0013


from django.conf.urls import url

from host.views import views, idc
from host.views import service, host ,user

urlpatterns = [
    url(r'^index/$', views.index, name="index"),
    url(r'^idcmanage/$', idc.idcmanage, name="idcmanage"),
    url(r'^serviceline/$', service.serviceline, name="serviceline"),
    url(r'^project/(?P<serviceid>\d+)', service.project, name="project"),
    url(r'^resources/$', host.resources, name="resources"),
    url(r'^query_ip/$', host.query_ip, name="query_ip"),
    url(r'^addhost/$', host.addhost, name="addhost"),
    url(r'^deletehost/$', host.deletehost, name="deletehost"),
    url(r'^modifyhost/$', host.modifyhost, name='modifyhost'),
    url(r'^usermanage/$', user.usermanage, name='usermanage'),
    url(r'^rolemanage/$', user.rolemanage, name='rolemanage'),
]