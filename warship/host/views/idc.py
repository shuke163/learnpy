from django.shortcuts import HttpResponse, render, redirect
from host import models
from host.views.views import AuthView
from django.views import View
from django.forms import Form, fields, widgets
from host.utils.customjson import JsonCustomEncoder
from host.utils import log
import json


class IdcManageForm(Form):
    """
    Idc表单验证
    """

    def __init__(self, *args, **kwargs):
        super(IdcManageForm, self).__init__(*args, **kwargs)
        # self.fields中包括拷贝的所有字段信息(深拷贝)
        self.fields['owner_id'].choices = models.User.objects.values_list("id", "username")
        print("*" * 50)
        # print(self.fields['owner_id'].choices)

    idc = fields.CharField(
        required=True,
        label=u'机房名称',
        max_length=32,
        error_messages={"required": "idc不能为空!"},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'机房名称'})
    )
    regionId = fields.CharField(
        required=True,
        label=u'英文简称',
        max_length=16,
        error_messages={"required": "idc简称不能为空!"},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'机房简称(英文)'})
    )
    area = fields.CharField(
        required=True,
        label=u'地区',
        max_length=32,
        error_messages={"required": "地区不能为空!"},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'机房所在地区'})
    )
    owner_id = fields.ChoiceField(
        required=True,
        label=u'负责人',
        choices=[],
        # widget=widgets.Select()
        widget=widgets.Select(attrs={'class': 'form-control'})
    )


class IdcManageView(AuthView, View):
    """
    idc数据展示
    """

    def get(self, request, *args, **kwargs):
        """
        展示IDC数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        form = IdcManageForm()
        idc_obj = models.Idc.objects.all()
        owner_obj = models.User.objects.all().values("id", "username")
        return render(request, "host/idcmanage.html", locals())

    def post(self, request, *args, **kwargs):
        """
        新建idc信息
        :param request: 请求参数
        :param args:
        :param kwargs:
        :return:
        """
        username = request.session.get('user_info')['username']
        response = {'status': True, 'data': None, 'msg': None}
        # 数据验证
        form = IdcManageForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            models.Idc.objects.create(**form.cleaned_data)
            log.logger.info("New idc info: username:{},idc:{},regionId:{},area:{},owner_id:{}".format(username,
                                                                                                      form.cleaned_data[
                                                                                                          'idc'],
                                                                                                      form.cleaned_data[
                                                                                                          'regionId'],
                                                                                                      form.cleaned_data[
                                                                                                          'area'],
                                                                                                      form.cleaned_data[
                                                                                                          'owner_id']))
        else:
            response['status'] = False
            response['msg'] = form.errors
            print(form.errors)
        return HttpResponse(json.dumps(response))


class EditIdcView(AuthView, View):
    """
    编辑idc信息
    """

    def get(self, request, pk):
        response = {'status': True, 'data': None, 'msg': None}
        print("主键", pk)
        try:
            obj = models.Idc.objects.filter(id=pk).values('id', 'idc', 'regionId', 'area', 'owner_id')
            response['data'] = list(obj)
            print(response['data'])
        except Exception as e:
            print(e)
            response['status'] = False
            response['msg'] = "获取信息失败"
        return HttpResponse(json.dumps(response))

    def post(self, request, pk):
        """
        保存修改后的idc数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        username = request.session.get('user_info')['username']
        print(username)
        response = {'status': True, 'data': None, 'msg': None}
        # 数据验证
        form = IdcManageForm(data=request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            idc_obj = models.Idc.objects.filter(id=pk)
            idc_obj.update(**form.cleaned_data)
            log.logger.info("Update idc info: username:{},idc:{},regionId:{},area:{},owner_id:{}".format(username,
                                                                                                         form.cleaned_data[
                                                                                                             'idc'],
                                                                                                         form.cleaned_data[
                                                                                                             'regionId'],
                                                                                                         form.cleaned_data[
                                                                                                             'area'],
                                                                                                         form.cleaned_data[
                                                                                                             'owner_id']))
        else:
            response['status'] = False
            response['msg'] = form.errors
            print(response['msg'])
        return HttpResponse(json.dumps(response))


class DeltIdcView(AuthView, View):
    """
    删除主机
    """

    def get(self, request, pk):
        """
        删除IDC信息
        :param request:
        :param pk:
        :return:
        """
        username = request.session.get('user_info')['username']
        print("删除", pk)
        try:
            models.Idc.objects.filter(id=pk).delete()
            log.logger.info("username:{},delete row id:{}".format(username, pk))
        except Exception as e:
            print("Error: ", e)
            log.logger.error("user:%s,删除主机错误: %s" % (username, e))
        return redirect("idcmanage")

# form = IdcManageForm(
#     initial={'idc': obj.idc, 'regionId': obj.regionId, 'area': obj.area, 'owner_id': obj.owner_id})
# print(form.idc, form.regionId, form.area)
# except Exception as e:
#     print(e)
#     response['status'] = False
#     response['msg'] = form.errors
#     print(form.errors)
# return HttpResponse(json.dumps(response))  # @auth  # def idcmanage(request):

# """
#     创建dic功能函数
#     :param request:
#     :return:
#     """
#     ret = {"status": False, "error": None, "data": None}
#     if request.method == "POST":
#         idc = request.POST.get("idc")
#         regionId = request.POST.get("regionId")
#         area = request.POST.get("area")
#         owner_id = request.POST.get("owner_id")
#         print("*" * 50)
#         print("提交的IDC数据为：", idc, regionId, area, owner_id)
#         try:
#             # 写入数据
#             insert_data = {"idc": idc, "regionId": regionId, "area": area, "owner_id": owner_id}
#             Idc.objects.create(**insert_data)
#             ret["status"] = True
#             ret["data"] = "success"
#             # 记录log
#             log.logger.info("New idc info".center(50, "*"))
#             log.logger.info(
#                 "username:{},idc:{},regionId:{},area:{},owner_id:{}".format(request.session.get("user"), idc, regionId,
#                                                                             area, owner_id))
#         except Exception as e:
#             print("Error: ", e)
#             ret["data"] = "failed"
#             ret["error"] = "Create idc faild"
#         return HttpResponse(json.dumps(ret))
#     # 获取数据
#     user = request.session.get("user")
#     idc_obj = Idc.objects.all()
#     owner_obj = User.objects.all().values("id", "username")
#     return render(request, 'host/cloud_idc.html', locals())
