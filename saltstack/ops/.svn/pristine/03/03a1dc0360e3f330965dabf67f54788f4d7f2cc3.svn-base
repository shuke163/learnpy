from django.conf.urls import url
from job.views import *

urlpatterns = [
    url(r'^cmd/$', cmd, name='cmd'),
    url(r'^cmd/moduleFunList/sync/$', moduleFunListSync, name='moduleFunListSync'),
    url(r'^cmd/moduleFunList/get/$', moduleFunListGet, name='moduleFunListGet'),
    url(r'^cmd/module/$', module, name='module'),
    url(r'^cmd/module/form/$', moduleForm, name='moduleForm'),
    url(r'^cmd/module/rest/$', ModuleRest.as_view(), name='moduleRest'),
    url(r'^cmd/command/$', command, name='command'),
    url(r'^cmd/command/form/$', commandForm, name='commandForm'),
    url(r'^cmd/command/rest/$', CommandRest.as_view(), name='commandRest'),
    url(r'^cmd/command/run/$', commandRun, name='commandRun'),
    url(r'^cmd/command/result/$', commandResult, name='commandResult'),
    url(r'^cmd/command/record/$', commandRecord, name='commandRecord'),
    url(r'^cmd/command/record/rest/$', CommandRecordRest.as_view(), name='commandRecordRest'),
]
