from django.shortcuts import HttpResponse, render, redirect
from host.views.views import AuthView
from django.views import View
from host import models
from django.forms import Form, fields, widgets
from host.utils.pageination import Page
from django.db.models import Q
from host.utils import log
import json


class HostForm(Form):
    """
    host表单验证
    """

    def __init__(self, *args, **kwargs):
        super(HostForm, self).__init__(*args, **kwargs)
        self.fields['service_id'].choices = models.Services.objects.values_list('id', 'name')
        self.fields['idc_id'].choices = models.Idc.objects.values_list('id', 'idc')
        self.fields['status_id'].choices = models.Status.objects.values_list('id', 'status')
        self.fields['owner_id'].choices = models.User.objects.values_list('id', 'username')

    hostname = fields.CharField(
        required=True,
        label=u'主机名',
        max_length=32,
        error_messages={'required': '主机名不能为空!'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'主机名'})
    )
    private_ip = fields.GenericIPAddressField(
        required=True,
        label=u'内网IP',
        max_length=32,
        # null=True,
        error_messages={'required': 'IP不合法!'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'内网IP'})
    )
    public_ip = fields.GenericIPAddressField(
        required=True,
        label=u'公网IP',
        max_length=32,
        # null=True,
        error_messages={'required': 'IP不合法!'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'公网IP'})
    )
    os = fields.CharField(
        required=True,
        label=u'OS',
        max_length=16,
        # default="ubuntu 16.04",
        error_messages={'required': 'os类型错误!'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'os'})
    )
    cpu = fields.CharField(
        required=True,
        label=u'cpu',
        max_length=10,
        error_messages={'required': '格式错误!'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'cpu'})
    )
    mem = fields.CharField(
        required=True,
        label=u'mem',
        max_length=16,
        error_messages={'required': '格式错误!'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'mem'})
    )
    disk = fields.CharField(
        required=True,
        label=u'disk',
        max_length=16,
        error_messages={'required': '格式错误!'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'disk'})
    )
    service_id = fields.ChoiceField(
        required=True,
        label=u'业务线',
        choices=[],
        error_messages={'required': '业务线类型错误!'},
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    idc_id = fields.ChoiceField(
        required=True,
        label=u'IDC',
        choices=[],
        error_messages={'required': 'IDC类型错误!'},
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    status_id = fields.ChoiceField(
        required=True,
        label=u'主机状态',
        choices=[],
        error_messages={'required': '主机状态类型错误!'},
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    owner_id = fields.ChoiceField(
        required=True,
        label=u'负责人',
        choices=[],
        error_messages={'required': '负责人未知错误!'},
        widget=widgets.Select(attrs={'class': 'form-control'})
    )


class ResourcesView(AuthView, View):
    """
    主机资源池
    """

    def get(self, request, *args, **kwargs):
        print(*args)
        service_li = models.Services.objects.values("id", "name")
        idc_li = models.Idc.objects.values("id", "idc")
        status_li = models.Status.objects.values("id", "status")
        owner_li = models.User.objects.values("id", "username")

        # 分页
        current_page = int(request.GET.get('page', 1))
        print("当前页: ", current_page)
        all_count = models.Hosts.objects.all().count()
        page_obj = Page(current_page, all_count, request.path_info)
        host_obj = models.Hosts.objects.values("id", "service__name", "hostname", "private_ip", "public_ip", "idc__idc",
                                               "os", "cpu", "mem", "disk", "status__status", "owner__username",
                                               "update_time").order_by('-id')[page_obj.start:page_obj.end]
        # 渲染的HTML
        page_str = page_obj.page_html()
        return render(request, 'host/resources.html', locals())

    def post(self, request, *args, **kwargs):
        pass


class AddhostView(AuthView, View):
    """
     添加主机
    """

    def get(self, request, *args, **kwargs):
        form = HostForm()
        return render(request, 'host/addhost.html', {'form': form})

    def post(self, request, *args, **kwargs):
        """
        添加主机
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.session.get('user_info')['username']
        response = {'status': True, 'data': None, 'msg': None}
        # 数据验证
        form = HostForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            models.Hosts.objects.create(**form.cleaned_data)
            log.logger.info(
                'username:{},Add host info:hostname:{},private_ip:{},public_ip:{},os:{},cpu:{},mem:{},disk:{},service_id:{},idc_id:{},status_id:{},owner_id:{}'.format(
                    username, form.cleaned_data['hostname'], form.cleaned_data['private_ip'],
                    form.cleaned_data['public_ip'], form.cleaned_data['os'], form.cleaned_data['cpu'],
                    form.cleaned_data['mem'], form.cleaned_data['disk'], form.cleaned_data['service_id'],
                    form.cleaned_data['idc_id'], form.cleaned_data['status_id'], form.cleaned_data['owner_id']))
            return redirect('resources')
        else:
            print(form.errors)
            return render(request, 'host/addhost.html', {'form': form})


class EdithostView(AuthView, View):
    """
    修改主机信息
    """

    def get(self, request, pk):
        try:
            obj = models.Hosts.objects.get(id=pk)
            form = HostForm(initial={'hostname': obj.hostname, 'private_ip': obj.private_ip, 'public_ip': obj.public_ip,
                                     'os': obj.os, 'cpu': obj.cpu, 'mem': obj.mem, 'disk': obj.disk,
                                     'service_id': obj.service_id, 'idc_id': obj.idc_id, 'status_id': obj.status_id,
                                     'owner_id': obj.owner_id})
            return render(request, 'host/edithost.html', {'form': form})
        except Exception as e:
            print('Error: ', e)

    def post(self, request, pk):
        """
        修改后更新主机信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        form = HostForm(data=request.POST)
        if form.is_valid():
            # 更新主机信息
            update_obj = models.Hosts.objects.filter(id=pk)
            update_obj.update(**form.cleaned_data)
            log.logger.info(
                'username:{},Update host info success:id:{}'.format(request.session['user_info']['username'], pk))
            return redirect('resources')
        else:
            print(form.errors)
            return render(request, 'host/edithost.html', {'form': form})


class DelhostView(AuthView, View):
    """
    删除主机
    """

    def get(self, request, *args, **kwargs):
        pk = request.GET.get('hid')
        models.Hosts.objects.get(id=pk).delete()
        log.logger.info(
            'username:{},delete host success:host id:{}'.format(request.session['user_info']['username'], pk))
        return redirect('resources')


class QueryipView(AuthView, View):
    """
    主机查询
    """

    def get(self, request, *args, **kwargs):
        try:
            query_ip = models.Hosts.objects.get('query_ip')
            query = ResourcesView.get(query_ip)
            pass
        except Exception as e:
            print("Error: ", e)

    def post(self, request, *args, **kwargs):
        try:
            ip = request.POST.get('query_ip')
            print("查询的条件为: ", ip)
            query = ResourcesView()
            print("*" * 50)
            ret = query.get(request, ip)
            return HttpResponse('ok')
        except Exception as e:
            pass


# @auth
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

    # 当前页
    current_page = int(request.GET.get("page", 1))
    print("当前页：", current_page)

    try:
        # 根据内网IP或公网IP查询条件进行过滤
        if query_arg:
            all_count = Hosts.objects.filter(Q(private_ip=query_arg) | Q(public_ip=query_arg)).count()
            page_obj = Page(current_page, all_count, request.path_info)
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
                                                                                                     "update_time")[
                       page_obj.start:page_obj.end]

        else:
            # 根据用户id进行过滤
            owner_id = request.GET.get("owner_id")
            if owner_id:
                all_count = Hosts.objects.filter(owner_id=owner_id).count()
                page_obj = Page(current_page, all_count, request.path_info)
                host_obj = Hosts.objects.filter(owner_id=owner_id).values("id", "service__name", "hostname",
                                                                          "private_ip",
                                                                          "public_ip", "idc__idc", "os", "cpu", "mem",
                                                                          "disk", "status__status", "owner__username",
                                                                          "update_time")[page_obj.start:page_obj.end]
            else:
                raise KeyError("owner_id is %s" % owner_id)
    # 所有的主机资源
    except Exception as e:
        print("*" * 50)
        print("Error: ", e)
        all_count = Hosts.objects.all().count()
        page_obj = Page(current_page, all_count, request.path_info)
        host_obj = Hosts.objects.values("id", "service__name", "hostname", "private_ip", "public_ip", "idc__idc", "os",
                                        "cpu", "mem", "disk", "status__status", "owner__username",
                                        "update_time").order_by('id')[page_obj.start:page_obj.end]
    # 渲染的html
    page_str = page_obj.page_html()

    return render(request, "host/resources.html",
                  {"user": "shuke", "service_li": service_li, "idc_li": idc_li, "status_li": status_li,
                   "host_li": host_obj, "owner_li": owner_li, "page_str": page_str})


# @auth
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
                log.logger.info("username: {},query args: {}".format(request.session.get("user"), query_ip))
                # 查询
                return resources(request, query_arg=query_ip)
            except Exception as e:
                print("Error: %s" % e)
        else:
            return HttpResponse("请输入查询条件!")


# @auth
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
            # return redirect('resources')


# @auth
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


# @auth
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
