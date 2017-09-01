#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/8/13 0013


from django.conf.urls import url
from host import views,idc,service,host

urlpatterns = [
    url(r'^idcmanage/$', idc.idcmanage, name="idcmanage"),
    url(r'^serviceline/$', service.serviceline, name="serviceline"),
    url(r'^project/(?P<serviceid>\d+)', service.project, name="project"),
    url(r'^index/$', views.index, name="index"),
    url(r'^resources/$', host.resources, name="resources"),
    url(r'^addhost/$', host.addhost, name="addhost"),
    url(r'^deletehost/$', host.deletehost, name="deletehost"),
    url(r'^modifyhost/$', host.modifyhost, name='modifyhost'),

]
