from django.shortcuts import HttpResponse, render, redirect
from host.models import *
import json


def serviceline(request):
    ret = {"status": False, "error": None, "data": None}
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        include_idc_id = request.POST.get("include_idc")
        owner = request.POST.get("owner")
        print("*" * 50)
        print("提交的业务线数据为：", service_name, include_idc_id, owner)
        try:
            # 写入数据
            insert_data = {"name": service_name, "include_idc_id": include_idc_id, "owner": owner}
            Services.objects.create(**insert_data)
            ret["status"] = True
            ret["data"] = "success"
        except Exception as e:
            ret["data"] = "failed"
            ret["error"] = e
        return HttpResponse(json.dumps(ret))
    # 获取数据
    idc_obj = Idc.objects.values('id', 'idc')
    service_obj = Services.objects.all()
    return render(request, 'host/service_line.html', locals())


def project(request, serviceid):
    # name = Services.objects.get(id=serviceid)
    host_li = Hosts.objects.filter(service__id=serviceid).values("id", "service__name", "hostname", "private_ip",
                                                                 "public_ip", "idc__idc", "os", "cpu", "mem", "disk",
                                                                 "status__status", "owner", "update_time")
    print("=" * 100)
    print(host_li)
    return render(request, "host/project.html", {"host_li": host_li})
