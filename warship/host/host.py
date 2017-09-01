from django.shortcuts import HttpResponse, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from host.models import *
import json


def resources(request):
    # host_li = Hosts.objects.all()
    service_li = Services.objects.values("id", "name")
    idc_li = Idc.objects.values("id", "idc")
    status_li = Status.objects.values("id", "status")
    host_obj = Hosts.objects.values("id", "service__name", "hostname", "private_ip", "public_ip", "idc__idc", "os",
                                    "cpu", "mem", "disk", "status__status", "owner", "update_time").order_by('id')
    print("业务线：", service_li)
    # print("主机列表：", host_li)
    # print("IDC列表：", idc_li)

    # host_obj = Hosts.objects.all().select_related('idc', 'status')[:20]
    # print(host_obj)
    paginator = Paginator(host_obj, 5)  # 每页10条数据
    page = request.GET.get("page")
    print("页码：",page)
    try:
        contacts = paginator.page(page)
        print(contacts)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "host/resources.html",
                  {"user": "shuke", "service_li": service_li, "idc_li": idc_li, "status_li": status_li,
                   "host_li": host_obj,"contacts": contacts})


# 添加主机
def addhost(request):
    if request.method == "POST":
        service_id = request.POST.get('service')
        hostname = request.POST.get('hostname')
        private_ip = request.POST.get('private_ip')
        public_ip = request.POST.get('public_ip', "null")
        idc_id = request.POST.get('idc')
        os = request.POST.get('os')
        cpu = request.POST.get('cpu')
        mem = request.POST.get('mem')
        disk = request.POST.get('disk')
        status_id = request.POST.get('status')
        owner = request.POST.get('owner')
        # 获得用户输入
        print("==" * 50)
        print(service_id, hostname, private_ip, public_ip, idc_id, os, cpu, mem, disk, status_id, owner)
        host_info = {"hostname": hostname, "private_ip": private_ip, "public_ip": public_ip, \
                     "idc_id": idc_id, "os": os, "cpu": cpu, "mem": mem, "disk": disk, "status_id": status_id,
                     "owner": owner}
        Hosts.objects.create(**host_info)
        # 多对多表写入,此处使用自定义第三张表的方式
        get_host_id = Hosts.objects.filter(hostname=hostname).values('id')[0]
        Service2hosts_obj = Service2hosts(host_id=str(get_host_id['id']), service_id=str(service_id))
        Service2hosts_obj.save()

        # 获取数据返回给前端进行展示
        # host_obj = Hosts.objects.all().select_related('idc', 'status')[:20]
        # if host_obj:
        #     return render(request, 'host/resources.html', {'user': 'shuke', 'host_li': host_obj})
    return render(request, 'host/resources.html')


def deletehost(request):
    print('*' * 50)
    if request.method == "POST":
        nid = request.POST.get('id')  # 获取删除的行ID
        print("删除的当前行ID为: ", nid)
        del_row = Hosts.objects.filter(id=nid)
        del_row.delete()
        status = 0
        result = "success"
        return HttpResponse(json.dumps({
            "status": status,
            "result": result
        }))
    host_info = list(Hosts.objects.values())
    return render(request, 'host/index.html', {'user': 'shuke', 'host_li': host_info})


def modifyhost(request):
    if request.method == "POST":
        ret = {"status": True, "result": "success", 'error': None}
        print("修改的内容为： \n")
        hid = request.POST.get('hid')
        service_id = request.POST.get('service_id')
        hostname = request.POST.get('hostname')
        private_ip = request.POST.get('private_ip')
        public_ip = request.POST.get('public_ip')
        idc_id = request.POST.get('idc_id')
        os = request.POST.get('os')
        mem = request.POST.get('mem')
        disk = request.POST.get('disk')
        status_id = request.POST.get('status_id')
        owner = request.POST.get('owner')
        try:
            if hid:
                # 获得用户输入
                print(hid, service_id, hostname, private_ip, public_ip, idc_id, os, mem, disk, status_id, owner)
                # 修改数据
                Hosts.objects.filter(id=hid).update(hostname=hostname, private_ip=private_ip, public_ip=public_ip, \
                                                    idc_id=idc_id, os=os, mem=mem, disk=disk, status_id=status_id,
                                                    owner=owner)
            else:
                ret["status"] = False
                ret["error"] = "主机ID不能为空"
        except Exception as e:
            print("\033[1;32mError: \033[0m", e)
            ret["status"] = False
            ret["error"] = "请求错误"
        return HttpResponse(json.dumps(ret))
