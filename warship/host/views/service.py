from django.shortcuts import HttpResponse, render, redirect
from host.models import *
from host.views.views import auth
from host.utils.pageination import Page
from host.utils import log
import json


@auth
def serviceline(request):
    """
    业务线视图函数
    :param request:
    :return:
    """
    user = request.session.get("user")
    ret = {"status": False, "error": None, "data": None}
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        idc_id = request.POST.get("idc")
        owner = request.POST.get("owner")
        print("*" * 50)
        print("提交的业务线数据为：", service_name, idc_id, owner)
        try:
            # 写入数据
            insert_data = {"name": service_name, "idc_id": idc_id, "owner_id": owner}
            Services.objects.create(**insert_data)
            ret["status"] = True
            ret["data"] = "success"
            log.logger.info(
                "username: {},create service line name:{},status:{}".format(user, service_name, ret["status"]))
        except Exception as e:
            ret["data"] = "failed"
            ret["error"] = e
        return HttpResponse(json.dumps(ret))
    # 获取数据
    idc_obj = Idc.objects.values('id', 'idc')
    owner_obj = User.objects.all().values('id', 'username')
    service_obj = Services.objects.all()
    return render(request, 'host/service_line.html', locals())


@auth
def project(request, serviceid):
    """
    业务线对应的主机展示
    :param request: 请求信息
    :param serviceid: 业务线id
    :return:
    """
    user = request.session.get('user')
    # 当前页
    current_page = request.GET.get("page", 1)
    print("当前页：", current_page)

    all_count = Hosts.objects.filter(service__id=serviceid).count()
    base_url = request.path_info
    page_obj = Page(current_page, all_count, base_url)
    host_li = Hosts.objects.filter(service__id=serviceid).values("id", "service__name", "hostname", "private_ip",
                                                                 "public_ip", "idc__idc", "os", "cpu", "mem", "disk",
                                                                 "status__status", "owner__username", "update_time")[
              page_obj.start:page_obj.end]
    # 渲染的HTML
    page_str = page_obj.page_html()
    print("=" * 100)
    return render(request, "host/project.html", locals())
