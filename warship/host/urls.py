#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/8/13 0013


from django.conf.urls import url,include
from host import views



urlpatterns = [
    url('^index/$',views.index),
    url('^addhost/$',views.addhost),
    url('^deletehost/$',views.deletehost),
    url('^modifyhost/$',views.modifyhost),
]