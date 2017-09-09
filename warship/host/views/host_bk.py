from django.shortcuts import HttpResponse, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from host.utils import log
from host.views.views import auth
from django.db.models import Q
from host.models import *
import json


@auth
def resources(request, query_arg=None):
    """
    资源池视图展示功能
    :param request:
    :param query_arg:
    :return:
    """
    service_li = Services.objects.values("id", "name")
    idc_li = Idc.objects.values("id", "idc")
    status_li = Status.objects.values("id", "status")
    owner_li = User.objects.values("id", "username")
    # values_arg = '''"id", "service__name", "hostname", "private_ip", "public_ip", "idc__idc", "os","cpu", "mem", \
    # "disk","status__status", "owner__username","update_time"'''
    # if not query_arg:
    #     host_obj = Hosts.objects.values(values_arg).order_by('id')
    # else:
    #     host_obj = Hosts.objects.filter(Q(private_ip=query_arg) | Q(public_ip=query_arg)).values(values_arg)

    try:
        # 根据内网IP或公网IP查询条件进行过滤
        if query_arg:
            host_obj = Hosts.objects.filter(Q(private_ip=query_arg) | Q(public_ip=query_arg)).values("id",
                                                                                                     "service__name",
                                                                                                     "hostname",
                                                                                                     "private_ip",
                                                                                                     "public_ip",
                                                                                                     "idc__idc", "os",
                                                                                                     "cpu", "mem",
                                                                                                     "disk",
                                                                                                     "status__status",
                                                                                                     "owner__username",
                                                                                                     "update_time")
        else:
            # 根据用户id进行过滤
            owner_id = request.GET.get("owner_id")
            if owner_id:
                host_obj = Hosts.objects.filter(owner_id=owner_id).values("id", "service__name", "hostname",
                                                                          "private_ip",
                                                                          "public_ip", "idc__idc", "os", "cpu", "mem",
                                                                          "disk", "status__status", "owner__username",
                                                                          "update_time")
            else:
                raise KeyError("owner_id is %s" % owner_id)
    # 所有的主机资源
    except Exception as e:
        print("*" * 50)
        print("Error: ", e)
        host_obj = Hosts.objects.values("id", "service__name", "hostname", "private_ip", "public_ip", "idc__idc", "os",
                                        "cpu", "mem", "disk", "status__status", "owner__username",
                                        "update_time").order_by('id')

    paginator = Paginator(host_obj, 5)  # 每页5条数据
    page = request.GET.get("page", 1)









    try:
        contacts = paginator.page(page)
        print(contacts)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    return render(request, "host/resources.html",
                  {"user": "shuke", "service_li": service_li, "idc_li": idc_li, "status_li": status_li,
                   "host_li": host_obj, "contacts": contacts, "owner_li": owner_li})


@auth
def query_ip(request):
    """
    主机查询功能
    :param request:
    :return:
    """
    # user = request.session.get("user")
    if request.method == "POST":
        query_ip = request.POST.get("query_ip")
        print("=" * 100)
        print(query_ip)
        if query_ip:
            try:
                # 查询
                return resources(request, query_arg=query_ip)
                log.logger.info("username: {},query args: {}".format(request.session.get("user"), query_ip))
            except Exception as e:
                print("Error: %s" % e)
        else:
            return HttpResponse("请输入查询条件!")


@auth
def addhost(request):
    """
    添加主机功能
    :param request:
    :return:
    """
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
        owner_id = request.POST.get('owner')
        # 获得用户输入
        print("==" * 50)
        print(service_id, hostname, private_ip, public_ip, idc_id, os, cpu, mem, disk, status_id, owner_id)
        try:
            host_info = {"hostname": hostname, "private_ip": private_ip, "public_ip": public_ip, \
                         "idc_id": idc_id, "os": os, "cpu": cpu, "mem": mem, "disk": disk, "status_id": status_id,
                         "owner_id": owner_id}
            Hosts.objects.create(**host_info)
            # 多对多表写入,此处使用自定义第三张表的方式
            get_host_id = Hosts.objects.filter(hostname=hostname).values('id')[0]
            # print(str(get_host_id["id"]),str(service_id))
            Service2hosts_obj = Service2hosts(host_id=get_host_id['id'], service_id=service_id)
            Service2hosts_obj.save()
            log.logger.info("Add host info".center(50, "*"))
            log.logger.info(
                "username:{},hostname:{},private_ip:{},public_ip:{},service_id:{},idc_id:{},os:{},cpu:{},mem:{},disk:{}, \
                status_id:{},owner_id:{}".format(request.session.get("user"), hostname, private_ip, public_ip, \
                                                 service_id, idc_id, os, cpu, mem, disk, status_id, owner_id))
        except Exception as e:
            print("Error: %s" % e)
            log.logger.error("username:{},add host faild!".format(request.session.get("user")))
            error_info = "Error: new host failed"
            return render(request, 'host/resources.html', {"error_info": error_info})

    # 获取数据返回给前端进行展示
    return redirect('resources')


@auth
def deletehost(request):
    """
    删除主机功能功能
    :param request:
    :return:
    """
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


@auth
def modifyhost(request):
    """
    更新主机信息功能
    :param request:
    :return:
    """
    ret = {"status": True, "result": "success", 'error': None, 'data': None}
    if request.method == "GET":
        hid = request.GET.get("id")
        try:
            host_info = Hosts.objects.get(id=int(hid))
            ret['data'] = host_info
            print(host_info)
        except Exception as e:
            print("\033[1;32mError: \033[0m", e)
            ret["status"] = False
            ret["error"] = "获取数据失败!"

        return HttpResponse(json.dumps(ret))
    else:
        # request.method == "POST":
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
