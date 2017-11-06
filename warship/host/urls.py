#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/8/13 0013


from django.conf.urls import url
from host.views import views, idc, service, host, user

urlpatterns = [
    url(r'^index/$', views.IndexView.as_view(), name="index"),
    url(r'^idcmanage/$', idc.IdcManageView.as_view(), name="idcmanage"),
    url(r'^editidc/(?P<pk>\d+)', idc.EditIdcView.as_view(), name="editidc"),
    url(r'^delidc/(?P<pk>\d+)', idc.DeltIdcView.as_view(), name="delidc"),
    url(r'^serviceline/$', service.ServiceLineView.as_view(), name="serviceline"),
    url(r'^editsvicline/(?P<pk>\d+)', service.EditSvicLineView.as_view(), name="editsvicline"),
    url(r'^delsvicline/$', service.DelSvicLineView.as_view(), name="delsvicline"),
    # url(r'^project/(?P<serviceid>\d+)', service.project, name="project"),
    url(r'^resources/$', host.ResourcesView.as_view(), name="resources"),
    url(r'^addhost/$', host.AddhostView.as_view(), name="addhost"),
    url(r'^deletehost/$', host.DelhostView.as_view(), name="deletehost"),
    url(r'^edithost/(?P<pk>\d+)', host.EdithostView.as_view(), name='edithost'),
    url(r'^query_ip/$', host.QueryipView.as_view(), name="queryip"),
    url(r'^usermanage/$', user.UserManageView.as_view(), name='usermanage'),
    url(r'^rolemanage/$', user.RoleManageView.as_view(), name='rolemanage'),
    url(r'^asset/$', host.asset, name='asset'),
]
