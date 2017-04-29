from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from job.salt import SaltAPI
from job.serializers import *
from sm.rest import ListCreateUpdateDestroyAPIView
from assets.models import HostGroup
import json


@login_required
def cmd(request):
    groups = HostGroup.objects.all().order_by('name')
    return render(request, 'job/cmd.html', {'groups': groups})


@login_required
def moduleFunListGet(request):
    moduleType = request.GET.get("moduleType")
    moduleId = request.GET.get("moduleId")
    data = []
    if moduleType:
        if not moduleId:
            data = ModuleSerializer(Module.objects.filter(type=moduleType), many=True).data
        else:
            data = CommandSerializer(Command.objects.filter(module__type=moduleType, module__id=moduleId),
                                     many=True).data
    return JsonResponse({'errno': 0, 'error': '', 'data': data})


@login_required
def moduleFunListSync(request):
    errno = 0
    try:
        api = SaltAPI()
        moduleTypes = [Module.execution, Module.runner, Module.wheel]
        for moduleType in moduleTypes:
            rsp = api.run(client='runner', fun="doc." + moduleType)
            docs = rsp['return'][0]
            for fun in docs:
                arr = fun.split('.')
                module, created = Module.objects.get_or_create(type=moduleType, name=arr[0])
                command, created = Command.objects.get_or_create(module=module, fun=fun)
                if not command.doc:
                    command.doc = docs[fun]
                    command.save()
    except Exception:
        errno = 1
    return JsonResponse({'errno': errno, 'error': '', 'data': ''})


@login_required
def module(request):
    return render(request, 'job/module.html')


@login_required
def moduleForm(request):
    try:
        obj = JSONRenderer().render(ModuleSerializer(Module.objects.get(id=request.GET.get('id'))).data)
    except Module.DoesNotExist:
        obj = None
    return render(request, 'job/moduleForm.html', {'obj': obj})


class ModuleRest(ListCreateUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer


@login_required
def command(request):
    modules = Module.objects.all()
    return render(request, 'job/command.html', {'modules': modules})


@login_required
def commandForm(request):
    modules = Module.objects.all()
    try:
        obj = JSONRenderer().render(CommandSerializer(Command.objects.get(id=request.GET.get('id'))).data)
    except Command.DoesNotExist:
        obj = None
    return render(request, 'job/commandForm.html', {'obj': obj, 'modules': modules})


class CommandRest(ListCreateUpdateDestroyAPIView):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer
    filter_fields = ('module',)


@login_required
def commandRun(request):
    client = request.GET.get("client")
    command = Command.objects.get(id=request.GET.get("commandId"))
    targetType = request.GET.get("targetType")
    target = request.GET.get("target")
    arguments = request.GET.get("arguments")
    cmd = request.GET.get("cmd")
    arg = []
    kwarg = {}
    if arguments:
        arr = arguments.split('|')
        for param in arr:
            kw = param.split('=')
            if len(kw) > 1:
                kwarg[kw[0]] = kw[1]
            else:
                arg.append(param)
    api = SaltAPI()

    if client == "runner" or client == "runner_async" or client == "wheel":
        rsp = api.run(client, command.fun, arg, kwarg)
    else:
        rsp = api.cmd(client, command.fun, targetType, target, arg, kwarg)

    if client == "local_async" or client == "runner_async":
        data = rsp['return'][0]["jid"]
        record = CommandRecord(cmd=cmd, jid=data, result="")
        record.save()
    else:
        data = rsp['return'][0]
        record = CommandRecord(cmd=cmd, jid="", result=json.dumps(data))
        record.save()
    return JsonResponse({'errno': 0, 'error': '', 'data': data})


@login_required
def commandResult(request):
    id = request.GET.get("id")
    jid = request.GET.get("jid")
    errno = 0
    isNew = False
    data = {}
    try:
        record = None
        if jid:
            record = CommandRecord.objects.get(jid=jid)
        elif id:
            record = CommandRecord.objects.get(id=id)
        if record:
            if record.result and record.result != "{}":
                data = json.loads(record.result)
            else:
                api = SaltAPI()
                rsp = api.jobs(record.jid)
                data = rsp['info'][0]['Result']
                record.result = json.dumps(data)
                record.save()
                isNew = True
    except CommandRecord.DoesNotExist:
        errno = 1
    except Exception:
        errno = 2

    return JsonResponse({'errno': errno, 'error': '', 'data': data, 'isNew': isNew})


@login_required
def commandRecord(request):
    return render(request, 'job/commandRecord.html')


class CommandRecordRest(ListCreateUpdateDestroyAPIView):
    queryset = CommandRecord.objects.all()
    serializer_class = CommandRecordSerializer
