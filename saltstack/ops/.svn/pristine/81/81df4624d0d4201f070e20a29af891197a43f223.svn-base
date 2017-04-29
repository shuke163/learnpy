from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer

from assets.serializers import *
from job.tasks import hostSyncTask
from sm.rest import ListCreateUpdateDestroyAPIView


@login_required
def hostGroup(request):
    return render(request, 'assets/hostGroup.html')


@login_required
def hostGroupForm(request):
    try:
        obj = JSONRenderer().render(HostGroupSerializer(HostGroup.objects.get(id=request.GET.get('id'))).data)
    except HostGroup.DoesNotExist:
        obj = None
    return render(request, 'assets/hostGroupForm.html', {'obj': obj})


class HostGroupRest(ListCreateUpdateDestroyAPIView):
    queryset = HostGroup.objects.all()
    serializer_class = HostGroupSerializer


@login_required
def host(request):
    groups = HostGroup.objects.all()
    return render(request, 'assets/host.html', {'groups': groups})


@login_required
def hostForm(request):
    groups = HostGroup.objects.all()
    try:
        obj = JSONRenderer().render(HostSerializer(Host.objects.get(id=request.GET.get('id'))).data)
    except Host.DoesNotExist:
        obj = None
    return render(request, 'assets/hostForm.html', {'obj': obj, 'groups': groups})


class HostRest(ListCreateUpdateDestroyAPIView):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    filter_fields = ('hostGroup',)


@login_required
def hostSync(request):
    # TODO
    # task = hostSyncTask.delay()
    # errno = task.get()
    errno = hostSyncTask()
    return JsonResponse({'errno': errno, 'error': '', 'data': ''})
