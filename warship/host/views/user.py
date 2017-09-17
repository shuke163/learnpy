from django.shortcuts import HttpResponse, render, redirect
from host import models
from host.views.views import AuthView
from django.views import View
from django.forms import Form, fields, widgets
from host.views.views import RegisterForm
from host.utils import getmd5
from host.utils import log
import json


class UserForm(Form):
    """
    用户表单验证
    """
    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        self.fields['dep_id'].choices = models.Department.objects.values_list("id","name")
        self.fields['role_id'].choices = models.UserRole.objects.values_list("id","rolename")

    username = fields.CharField(
        required=True,
        max_length=16,
        error_messages={'required':'用户名不能为空!','invalid':'最大长度16个字符!'},
        widget=widgets.TextInput(attrs={'class': 'form-control', 'placeholder': u'用户名'})
    )
    password = fields.CharField(
        required=True,
        min_length=6,
        max_length=32,
        error_messages={'required': '密码不能为空!', 'invalid': '最小长度6个字符!'},
        widget=widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'密码'})
    )
    sex = fields.ChoiceField(
        choices=((0, '男'), (1, '女'),),
        initial=0,
        widget=widgets.RadioSelect()
    )
    email = fields.EmailField(
        required=True,
        min_length=6,
        max_length=32,
        widget=widgets.EmailInput(attrs={'class': "form-control", 'placeholder': "email"})
    )
    phone = fields.CharField(
        required=True,
        max_length=11,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "phone"})
    )
    dep_id = fields.ChoiceField(
        choices=[],
        widget=widgets.Select(attrs={'class': "form-control", 'placeholder': "dep"})
    )
    role_id = fields.ChoiceField(
        choices=[],
        widget=widgets.Select(attrs={'class': "form-control", 'placeholder': "role"})
    )


class RoleForm(Form):
    """
    角色表单验证
    """
    rolename = fields.CharField(
        required=True,
        max_length=16,
        error_messages={'required':'名称不能为空!'}
    )
    permissions = fields.CharField(
        required=True,
        max_length=16,
        error_messages={'required':'权限不能为空!'}
    )


class UserManageView(AuthView, View):
    """
    用户管理视图
    """

    def get(self, request, *args, **kwargs):
        # dep_obj = models.Department.objects.values("id", "name")
        # role_obj = models.UserRole.objects.values("id", "rolename")
        user_obj = models.User.objects.all().select_related("dep", "role")
        form = UserForm()
        return render(request, "host/usermanage.html", locals())

    def post(self, request, *args, **kwargs):
        pass


class RoleManageView(AuthView, View):
    """
    角色管理视图
    """

    def get(self, request, *args, **kwargs):
        role_obj = models.UserRole.objects.all()
        return render(request, "host/rolemanage.html", {"role_obj": role_obj})

    def post(self, request, *args, **kwargs):
        response = {'status': True, 'data': None, 'msg': None}
        form = RoleForm(data=request.POST)
        if form.is_valid():
            models.UserRole.objects.create(**form.cleaned_data)
            log.logger.info(
                "username:{},Add role info: rolenmae:{},permissions:{}".format(request.session['user_info']['username'],
                                                                               form.cleaned_data['rolename'],
                                                                               form.cleaned_data['permissions']))
        else:
            print("Error: ", form.errors)
            response['status'] = False
            response['msg'] = form.errors
        return HttpResponse(json.dumps(response))



# @auth
def usermanage(request):
    """
    用户管理视图函数
    :param request:
    :return:
    """
    user = request.session.get("user")
    if request.method == "GET":
        user_obj = User.objects.all().select_related("dep", "role").order_by("id")
        dep_obj = Department.objects.all().values("id", "name")
        role_obj = UserRole.objects.all().values("id", "rolename")
        return render(request, "host/usermanage.html", locals())
    else:
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        sex = request.POST.get('sex')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dep_id = request.POST.get('dep_id')
        role_id = request.POST.get('role_id', 3)
        print("*" * 50)
        print("注册数据：", username, passwd, sex, email, phone, dep_id, role_id)
        select_user = User.objects.filter(username=username).values()
        # 用户已存在
        if select_user:
            log.logger.error("register info: username:{},Already exists".format(username))
            ret = {"status": 1, "result": "faild"}
            return HttpResponse(json.dumps(ret))
        else:
            # 注册成功，写入数据
            passwd = getmd5.md5(passwd)
            insert_data = {'username': username, 'password': passwd, "sex": sex, "email": email, "phone": phone,
                           "dep_id": dep_id, 'role_id': role_id}
            User.objects.create(**insert_data)
            log.logger.info(
                "register info: username:{0},email:{1},phone:{2},department:{3}".format(username, email, phone,
                                                                                        dep_id, role_id))
            ret = {"status": 0, "result": "success"}
            return HttpResponse(json.dumps(ret))


# @auth
def rolemanage(request):
    """
    角色管理视图函数
    :param request:
    :return:
    """
    ret = {"status": False, "data": None, 'error': None}
    user = request.session.get("user")
    if request.method == "GET":
        user_obj = User.objects.values("id", "username")
        role_obj = UserRole.objects.all().order_by("id")
        return render(request, "host/rolemanage.html", locals())
    else:
        rolename = request.POST.get("rolename")
        permissions = request.POST.get("permissions")
        user_id = request.POST.get("user_id")
        try:
            insert_data = {"rolename": rolename, "permissions": permissions, "user_id": user_id}
            UserRole.objects.create(**insert_data)
            ret["status"] = True
            ret["data"] = "success"
            # 记录log
            log.logger.info(
                "username:{},New create role info,rolename:{},permissions:{},owner_id:{}".format(user, rolename,
                                                                                                 permissions, user_id))
        except Exception as e:
            print("Error: ", e)

    return HttpResponse(json.dumps(ret))
