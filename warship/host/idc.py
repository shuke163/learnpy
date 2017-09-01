from django.shortcuts import HttpResponse, render, redirect
from host.models import *
import json


def idcmanage(request):
    ret = {"status": False, "error": None, "data": None}
    if request.method == "POST":
        idc = request.POST.get("idc")
        regionId = request.POST.get("regionId")
        area = request.POST.get("area")
        owner = request.POST.get("owner")
        print("*" * 50)
        print("提交的IDC数据为：", idc, regionId, area, owner)
        try:
            # 写入数据
            insert_data = {"idc": idc, "regionId": regionId, "area": area, "owner": owner}
            Idc.objects.create(**insert_data)
            ret["status"] = True
            ret["data"] = "success"
        except Exception as e:
            ret["data"] = "failed"
            ret["error"] = e
        return HttpResponse(json.dumps(ret))
    # 获取数据
    idc_obj = Idc.objects.all()
    return render(request, 'host/cloud_idc.html', locals())
