#!/usr/bin/env python
# -*- coding:utf-8 -*-
from celery import Celery
from celery.schedules import crontab


cel = Celery('cel_tasks',
             broker='redis://127.0.0.1:6379',
             backend='redis://127.0.0.1:6379',
             include=['celery_tasks.tasks'])

# # 时区
# celery.conf.timezone = 'Asia/Shanghai'
# # 是否使用UTC
# celery.conf.enable_utc = False
