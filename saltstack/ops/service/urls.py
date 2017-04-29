from django.conf.urls import url
from service.views import *

urlpatterns = [
    url(r'^state/$', state, name='state'),
    url(r'^state/form/$', stateForm, name='stateForm'),
    url(r'^state/rest/$', StateRest.as_view(), name='stateRest'),
    url(r'^serviceType/$', serviceType, name='serviceType'),
    url(r'^serviceType/form$', serviceTypeForm, name='serviceTypeForm'),
    url(r'^serviceType/rest$', ServiceTypeRest.as_view(), name='serviceTypeRest'),
    url(r'^serviceGroup/$', serviceGroup, name='serviceGroup'),
    url(r'^serviceGroup/form$', serviceGroupForm, name='serviceGroupForm'),
    url(r'^serviceGroup/rest$', ServiceGroupRest.as_view(), name='serviceGroupRest'),
    url(r'^serviceGroup/pillars$', pillarListGet, name='pillarListGet'),
    url(r'^service/$', service, name='service'),
    url(r'^service/form$', serviceForm, name='serviceForm'),
    url(r'^service/rest$', ServiceRest.as_view(), name='serviceRest'),
    url(r'^service/types$', serviceTypeListGet, name='serviceTypeListGet'),
    url(r'^service/states$', stateSameListGet, name='stateSameListGet'),
    url(r'^service/doJob$', doJob, name='doJob'),
    url(r'^service/job$', serviceJob, name='serviceJob'),
    url(r'^service/job/rest$', ServiceJobRest.as_view(), name='serviceJobRest'),
    url(r'^service/job/result', serviceJobResult, name='serviceJobResult'),
]
