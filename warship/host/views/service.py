from django.shortcuts import HttpResponse, render, redirect
from host.models import *
# from host.views.views import auth
from host.views.views import AuthView
from django.views import View
from host import models
from django.forms import Form, fields, widgets
from host.utils.pageination import Page
from host.utils import log
import json


class ServiceForm(Form):
    """
    业务线表单验证
    """

    def __init__(self, *args, **kwargs):
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['idc_id'].choices = models.Idc.objects.values_list("id", "idc")
        self.fields['owner_id'].choices = models.User.objects.values_list("id", "username")
        print("*" * 50)
        print(self.fields['idc_id'].choices)
        print(self.fields['owner_id'].choices)

    name = fields.CharField(
        required=True,
        label=u'业务线名称',
        max_length=32,
        error_messages={"required": "业务线名称不能为空!"},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'业务线名称'})
    )

    idc_id = fields.ChoiceField(
        required=True,
        label=u'所属机房',
        choices=[],
        widget=widgets.Select(attrs={'class': 'form-control'})
    )

    owner_id = fields.MultipleChoiceField(
        required=True,
        choices=[],
        error_messages={'required': "负责人不能为空!"},
        widget=widgets.SelectMultiple(attrs={'class': 'form-control'})
    )


class ServiceLineView(AuthView, View):
    """
    业务线视图函数
    """

    def get(self, request, *args, **kwargs):
        """
        展示业务线信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        form = ServiceForm()
        service_obj = models.Services.objects.all().order_by('-id')
        owner_obj = models.User.objects.values('id', 'username')
        return render(request, "host/service_line.html",
                      {'form': form, 'service_obj': service_obj, 'owner_obj': owner_obj})

    def post(self, request, *args, **kwargs):
        """
        新建业务线
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.session.get('user_info')['username']
        response = {'status': True, 'data': None, 'msg': None}
        print(request.POST)
        print(request.POST.get('owner_id'))
        form = ServiceForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            owner_id_list = form.cleaned_data.pop('owner_id')
            obj = models.Services.objects.create(**form.cleaned_data)
            # 写入第三张表
            obj.owner.add(*owner_id_list)
            # 成功写入log
            log.logger.info(
                "username:{},Add service line info: name:{},idc_id:{}".format(username, form.cleaned_data['name'],
                                                                              form.cleaned_data['idc_id']))
            # for item in owner_id_list:
            #     m2m = models.Service2user(service_id=obj.id, user_id=item)
            #     m2m.save()
        else:
            print(form.errors)
            response['status'] = False
            response['msg'] = form.errors
        return HttpResponse(json.dumps(response))


class EditSvicLineView(AuthView, View):
    """
    修改业务线
    """

    def get(self, request, pk):
        response = {'status': True, 'data': None, 'msg': None}
        try:
            # pk = request.GET.get('sid')
            obj = models.Services.objects.filter(id=pk).first()
            owner_id_list = obj.owner.values_list('id')
            m2m = list(zip(*owner_id_list))[0] if owner_id_list else []
            print("主键id: ", pk, m2m)
            form = ServiceForm(initial={'name': obj.name, 'idc_id': obj.idc_id, 'owner_id': m2m})
            return render(request, 'host/editsvicline.html', {'form': form})
        except Exception as e:
            print(e)
            response['status'] = False
            response['msg'] = "获取信息失败"
        return HttpResponse(json.dumps(response))

    def post(self, request, pk):
        """
        修改业务线
        :param request:
        :param pk:
        :return:
        """
        username = request.session.get('user_info')['username']
        form = ServiceForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            owner_id_li = form.cleaned_data.pop('owner_id')
            # 更新数据
            query = models.Services.objects.filter(id=pk)
            query.update(**form.cleaned_data)
            obj = query.first()
            obj.owner.set(owner_id_li)
            # 成功写入log
            log.logger.info(
                "username:{},update service line info: name:{},idc_id:{}".format(username, form.cleaned_data['name'],
                                                                                 form.cleaned_data['idc_id']))
            return redirect('serviceline')
        else:
            print(form.errors)
            return render(request, 'host/editsvicline.html', {'form': form})


class DelSvicLineView(AuthView, View):
    """
    删除业务线逻辑
    """

    def get(self, request, *args, **kwargs):
        """
        删除业务线数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.session.get('user_info')['username']
        try:
            pk = request.GET.get("id")
            obj = models.Services.objects.filter(id=pk).first()
            models.Services.objects.filter(id=pk).delete()
            log.logger.info("user:{},delete info: name:{},idc_id:{}".format(username, obj.name, obj.idc_id))
        except Exception as e:
            print("Error: ", e)
            log.logger.error("user:%s, 删除业务线错误:%s" % (username, e))
        return redirect('serviceline')

    def post(self, request, *args, **kwargs):
        pass


# @auth
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
