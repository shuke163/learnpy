from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction
from rest_framework.renderers import JSONRenderer

from sm.rest import ListCreateUpdateDestroyAPIView
from service.serializers import *
from service.tools import *
from job.salt import SaltAPI
import json


@login_required
def state(request):
    return render(request, 'service/state.html')


@login_required
def stateForm(request):
    saltRoot = settings.SALT_ROOT
    projectRoot = settings.PROJECT_ROOT
    jinjaRoot = settings.JINJA_ROOT
    try:
        obj = JSONRenderer().render(StateSerializer(State.objects.get(id=request.GET.get("id"))).data)
    except State.DoesNotExist:
        obj = None
    return render(request, 'service/stateForm.html',
                  {'saltRoot': saltRoot, 'projectRoot': projectRoot, 'jinjaRoot': jinjaRoot, 'obj': obj,
                   'ACTION_STATUS': ACTION_STATUS})


class StateRest(ListCreateUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    # create
    def post(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                data = json.loads(request.data.get('data'))
                Tools.stateCheck(data)
                data.pop('id')
                items = data.pop('jinjas')
                state = State.objects.create(**data)
                for item in items:
                    item.pop('id')
                    jinja = Jinja.objects.create(**item)
                    state.jinjas.add(jinja)
                state.pillars = json.dumps(Tools.getPillars(state), sort_keys=True)
                state.save()
                # 保存文件
                api = SaltAPI()
                api.writeFile(state.path, state.content)
                for jinja in state.jinjas.all():
                    api.writeFile(jinja.path, jinja.content)
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})

    # update
    def put(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                data = json.loads(request.data.get('data'))
                Tools.stateCheck(data)
                state = State.objects.get(id=data.get('id'))
                deletePaths = []
                if state.path != data.get('path'):
                    deletePaths.append(state.path)
                state.name = data.get('name')
                state.remark = data.get('remark')
                state.fun = data.get('fun')
                state.path = data.get('path')
                state.content = data.get('content')
                state.successStatus = data.get('successStatus')
                state.failureStatus = data.get('failureStatus')
                currentJinjaIds = []
                for item in data.get('jinjas'):
                    if item.get('id') == "":
                        # 新增
                        item.pop('id')
                        jinja = Jinja.objects.create(**item)
                        state.jinjas.add(jinja)
                        currentJinjaIds.append(jinja.id)
                    else:
                        # 修改
                        jinja = Jinja.objects.get(id=item.get('id'))
                        if jinja.path != item.get('path'):
                            deletePaths.append(jinja.path)
                        jinja.name = item.get('name')
                        jinja.path = item.get('path')
                        jinja.content = item.get('content')
                        jinja.save()
                        currentJinjaIds.append(jinja.id)
                for jinja in state.jinjas.all():
                    if jinja.id not in currentJinjaIds:
                        # 已删除
                        deletePaths.append(jinja.path)
                        jinja.delete()
                pillars = Tools.getPillars(state)
                if Tools.isPillarsAdd(json.loads(state.pillars), pillars):
                    for serviceType in state.servicetype_set.all():
                        for serviceGroup in serviceType.servicegroup_set.all():
                            serviceGroup.hasNewPillars = True
                            serviceGroup.save()
                state.pillars = json.dumps(pillars, sort_keys=True)
                state.save()
                # 保存文件
                api = SaltAPI()
                api.writeFile(state.path, state.content)
                for jinja in state.jinjas.all():
                    api.writeFile(jinja.path, jinja.content)
                # 删除文件
                for path in deletePaths:
                    api.deleteFile(path)
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})

    # delete
    def delete(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                id = int(request.data['id'])
                state = State.objects.get(id=id)
                deletePaths = []
                for jinja in state.jinjas.all():
                    deletePaths.append(jinja.path)
                    jinja.delete()
                deletePaths.append(state.path)
                state.delete()
                # 删除文件
                api = SaltAPI()
                for path in deletePaths:
                    api.deleteFile(path)
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})


@login_required
def serviceType(request):
    states = State.objects.all()
    return render(request, 'service/serviceType.html', {'states': states})


@login_required
def serviceTypeForm(request):
    states = State.objects.all()
    try:
        obj = JSONRenderer().render(ServiceTypeSerializer(ServiceType.objects.get(id=request.GET.get("id"))).data)
    except ServiceType.DoesNotExist:
        obj = None
    return render(request, 'service/serviceTypeForm.html', {'states': states, 'obj': obj})


class ServiceTypeRest(ListCreateUpdateDestroyAPIView):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer

    # create
    def post(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                data = json.loads(request.data.get('data'))
                Tools.serviceTypeCheck(data)
                data.pop('id')
                items = data.pop("states")
                serviceType = ServiceType.objects.create(**data)
                for item in items:
                    state = State.objects.get(id=item)
                    serviceType.states.add(state)
                serviceType.save()
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})

    # update
    def put(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                data = json.loads(request.data.get('data'))
                Tools.serviceTypeCheck(data)
                items = data.pop("states")
                serviceType = ServiceType.objects.get(id=data.get('id'))
                # 不能修改name
                serviceType.remark = data.get('remark')
                serviceType.states.clear()
                for item in items:
                    state = State.objects.get(id=item)
                    serviceType.states.add(state)
                serviceType.save()
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})

    # delete
    def delete(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                id = int(request.data['id'])
                serviceType = ServiceType.objects.get(id=id)
                serviceType.delete()
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})


@login_required
def serviceGroup(request):
    serviceTypes = ServiceType.objects.all()
    return render(request, 'service/serviceGroup.html', {'serviceTypes': serviceTypes})


@login_required
def serviceGroupForm(request):
    serviceTypes = ServiceType.objects.all()
    try:
        obj = JSONRenderer().render(ServiceGroupSerializer(ServiceGroup.objects.get(id=request.GET.get("id"))).data)
    except ServiceGroup.DoesNotExist:
        obj = None
    return render(request, 'service/serviceGroupForm.html', {'serviceTypes': serviceTypes, 'obj': obj})


class ServiceGroupRest(ListCreateUpdateDestroyAPIView):
    queryset = ServiceGroup.objects.all()
    serializer_class = ServiceGroupSerializer

    # create
    def post(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                data = json.loads(request.data.get('data'))
                Tools.serviceGroupCheck(data)
                data.pop('id')
                items = data.pop("serviceTypes")
                data['hasNewPillars'] = False
                serviceGroup = ServiceGroup.objects.create(**data)
                for item in items:
                    serviceType = ServiceType.objects.get(id=item)
                    serviceGroup.serviceTypes.add(serviceType)
                serviceGroup.pillars = json.dumps(data.get('pillars'), sort_keys=True)
                serviceGroup.save()
                # 保存文件
                api = SaltAPI()
                path = settings.PROJECT_ROOT + serviceGroup.name + ".sls"
                content = Tools.generatePillarContent(serviceGroup)
                api.writePillar(path, content)
                # 更新init.sls
                Tools.addPillarsPathConfig(api, path)
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})

    # update
    def put(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                data = json.loads(request.data.get('data'))
                Tools.serviceGroupCheck(data)
                items = data.pop("serviceTypes")
                serviceGroup = ServiceGroup.objects.get(id=data.get('id'))
                # 不能修改name
                serviceGroup.remark = data.get('remark')
                serviceGroup.serviceTypes.clear()
                for item in items:
                    serviceType = ServiceType.objects.get(id=item)
                    serviceGroup.serviceTypes.add(serviceType)
                serviceGroup.pillars = json.dumps(data.get('pillars'), sort_keys=True)
                serviceGroup.hasNewPillars = False
                serviceGroup.save()
                # 保存文件
                api = SaltAPI()
                path = settings.PROJECT_ROOT + serviceGroup.name + ".sls"
                content = Tools.generatePillarContent(serviceGroup)
                api.writePillar(path, content)
                # 更新init.sls
                Tools.addPillarsPathConfig(api, path)
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})

    # delete
    def delete(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                id = int(request.data['id'])
                serviceGroup = ServiceGroup.objects.get(id=id)
                path = settings.PROJECT_ROOT + serviceGroup.name + ".sls"
                serviceGroup.delete()
                api = SaltAPI()
                # 更新init.sls
                Tools.delPillarsPathConfig(api, path)
                # 删除文件
                api.deletePillar(path)
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})


@login_required
def pillarListGet(request):
    errno = 0
    error = ""
    pillars = {}
    try:
        ids = json.loads(request.GET.get('serviceTypes'))
        for id in ids:
            serviceType = ServiceType.objects.get(id=id)
            items = {}
            for state in serviceType.states.all():
                items.update(json.loads(state.pillars))
            pillars[serviceType.name] = items
    except Exception as e:
        errno = 1
        error = str(e)
    return JsonResponse({'errno': errno, 'error': error, 'pillars': json.dumps(pillars, sort_keys=True)})


@login_required
def service(request):
    hosts = Host.objects.all()
    groups = ServiceGroup.objects.all()
    types = ServiceType.objects.all()
    return render(request, 'service/service.html',
                  {'hosts': hosts, 'groups': groups, 'types': types, 'ACTION_STATUS': ACTION_STATUS})


@login_required
def serviceForm(request):
    groups = ServiceGroup.objects.all()
    hosts = Host.objects.all()
    try:
        obj = JSONRenderer().render(ServiceSerializer(Service.objects.get(id=request.GET.get("id"))).data)
    except Service.DoesNotExist:
        obj = None
    return render(request, 'service/serviceForm.html', {'groups': groups, 'hosts': hosts, 'obj': obj})


class ServiceRest(ListCreateUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_fields = ('group', 'type',)

    # delete
    def delete(self, request, *args, **kwargs):
        errno = 0
        error = ""
        try:
            with transaction.atomic():
                id = int(request.data['id'])
                service = Service.objects.get(id=id)
                if service.currentJobId != -1:
                    errno = 1
                    error = "该服务有任务正在运行，不行删除!"
                else:
                    service.delete()
        except Exception as e:
            errno = 1
            error = str(e)
        return JsonResponse({'errno': errno, 'error': error})


@login_required
def serviceTypeListGet(request):
    groupId = request.GET.get("groupId")
    data = []
    if groupId:
        group = ServiceGroup.objects.get(id=groupId)
        data = ServiceTypeSerializer(group.serviceTypes.all(), many=True).data
    return JsonResponse({'errno': 0, 'error': '', 'data': data})


@login_required
def stateSameListGet(request):
    errno = 0
    error = ""
    data = []
    try:
        ids = json.loads(request.GET.get("ids"))
        count = dict()
        states = dict()
        for id in ids:
            service = Service.objects.get(id=id)
            if service.currentJobId != -1:
                raise RuntimeError("服务(" + service.name + ")正在执行任务，不能执行新任务！")
            for state in service.type.states.all():
                if state.id in count:
                    count[state.id] += 1
                else:
                    count[state.id] = 1
                states[state.id] = state
        sameList = []
        for id, time in count.items():
            if time == len(ids):
                sameList.append(states[id])
        data = StateSerializer(sameList, many=True).data
    except Exception as e:
        errno = 1
        error = str(e)
    return JsonResponse({'errno': errno, 'error': error, 'data': data})


@login_required
def doJob(request):
    errno = 0
    error = ""
    try:
        stateId = request.GET.get("stateId")
        state = State.objects.get(id=stateId)
        serviceIds = json.loads(request.GET.get("serviceIds"))
        api = SaltAPI()
        for serviceId in serviceIds:
            service = Service.objects.get(id=serviceId)
            try:
                pillar = {'service_group': service.group.name, 'service_type': service.type.name}
                rsp = api.cmd(client='local_async', fun="state.sls", targetType='list', target=service.host.saltId,
                              arg=[state.fun], kwarg={'pillar': pillar})
                jid = rsp['return'][0]["jid"]
                job = ServiceJob.objects.create(jid=jid, service=service, state=state)
                service.currentJobId = job.id
                service.currentJobDesc = job.state.name
            except Exception:
                service.currentJobId = -1
                service.currentJobDesc = ""
                service.status = state.failureStatus
            service.save()
    except Exception as e:
        errno = 1
        error = str(e)
    return JsonResponse({'errno': errno, 'error': error})


@login_required
def serviceJob(request):
    return render(request, 'service/serviceJob.html')


class ServiceJobRest(ListCreateUpdateDestroyAPIView):
    queryset = ServiceJob.objects.all()
    serializer_class = ServiceJobSerializer


@login_required
def serviceJobResult(request):
    errno = 0
    error = ""
    data = {}
    try:
        job = ServiceJob.objects.get(id=request.GET.get("id"))
        if job.result:
            data = json.loads(job.result)
    except Exception as e:
        errno = 1
        error = str(e)
    return JsonResponse({'errno': errno, 'error': error, 'data': data})
