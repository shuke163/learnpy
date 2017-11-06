from django.shortcuts import HttpResponse, render, redirect
from django.views import View
from host import models
from host.utils import getmd5
from host.utils import log
from django.forms import Form
from django.forms import fields
from django.forms import widgets
import json


class RegisterForm(Form):
    """
    注册表单验证
    """

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # self.fileds为下列所有字段的深拷贝
        self.fields['dep_id'].choices = models.Department.objects.values_list('id', 'name')

    username = fields.CharField(
        required=True,
        min_length=3,
        max_length=16,
        widget=widgets.TextInput(attrs={'class': "form-control", 'placeholder': "username"})
    )
    password = fields.CharField(
        required=True,
        min_length=6,
        max_length=16,
        widget=widgets.PasswordInput(attrs={'class': "form-control", 'placeholder': "password"})
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
        widget = widgets.TextInput(attrs={'class': "form-control", 'placeholder': "phone"})
    )
    dep_id = fields.ChoiceField(
        choices=[],
        widget=widgets.Select(attrs={'class': "form-control", 'placeholder': "phone"})
    )


class RegisterView(View):
    """
    注册视图
    """

    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, "register.html", {'form': form})

    def post(self, request, *args, **kwargs):
        response = {'status': True, 'data': None, 'msg': None}
        print("*" * 50)
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            print("post提交数据", form.cleaned_data)
            form.cleaned_data["password"] = getmd5.md5(form.cleaned_data["password"])
            obj = models.User.objects.create(**form.cleaned_data)
            log.logger.info(
                "Register info: user:{},sex:{},email:{},phone:{},dep_id:{}".format(form.cleaned_data["username"],
                                                                                   form.cleaned_data["sex"],
                                                                                   form.cleaned_data["email"],
                                                                                   form.cleaned_data["phone"],
                                                                                   form.cleaned_data["dep_id"]))
        else:
            print("错误信息", form.errors)
            response['status'] = False
            # json.dumps之后转化为字典格式
            response['msg'] = form.errors

        return HttpResponse(json.dumps(response))


class AuthView(object):
    """
    session验证
    """

    def dispath(self, request, *args, **kwargs):
        if request.session.get('user_info'):
            response = super(AuthView, self).dispatch(request, *args, **kwargs)
            # 返回 View类中映射的get/post方法
            return response
        else:
            return redirect('login')


class LoginView(View):
    """
    登陆
    """

    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        pwd = getmd5.md5(pwd)
        obj = models.User.objects.filter(username=user, password=pwd).first()
        if obj:
            request.session['user_info'] = {'id': obj.id, 'username': obj.username, 'is_login': True}
            log.logger.info("username: %s,login success" % user)
            return redirect('index')
        return render(request, 'login.html', {'msg': '用户名或密码错误!'})


class IndexView(AuthView, View):
    """
    首页
    """

    def get(self, request, *args, **kwargs):
        host_count = models.Hosts.objects.all().count()
        return render(request, "host/index.html", {"total": host_count})


class LogoutView(AuthView, View):
    """
    注销
    """

    def get(self, request, *args, **kwargs):
        user = request.session.get("user_info")['username']
        request.session.clear()
        log.logger.info("{} logged out success".format(user))
        return render(request, "login.html")

# # 登陆页面
# def login(request):
#     """
#     登陆认证函数
#     :param request:
#     :return:
#     """
#     if request.method == "GET":
#         return render(request, 'login.html')
#     else:
#         user = request.POST.get('user')
#         pwd = request.POST.get('pwd')
#         pwd = getmd5.md5(pwd)
#         query_obj = User.objects.filter(username=user, password=pwd).first()
#         if query_obj:
#             request.session['user'] = user
#             request.session['is_login'] = True
#             logger.info("username: %s,login success" % user)
#             return redirect("index")
#         else:
#             return render(request, 'login.html', {'msg': '用户名或密码错误!'})
#
#
# # 认证
# # def auth(request):
# #     dt = datetime.datetime.now()
# #     if request.method == "POST":
# #         user = request.POST.get('user')
# #         pwd = request.POST.get('pwd')
# #         query_obj = User.objects.filter(username=user).values("username", "password")
# #         if query_obj:
# #             username = query_obj[0]['username']
# #             password = query_obj[0]['password']
# #             if user == username and pwd == password:
# #                 print("*" * 100)
# #                 print("当前时间： %s,登陆成功用户：%s" % (dt, user))
# #                 index = "/host/index/"
# #                 return redirect(index)
# #     return render(request, 'host/login.html')
#
#
# # 注册试图
# def register(request):
#     """
#     注册函数
#     :param request:
#     :return:
#     """
#     if request.method == "POST":
#         reg_user = request.POST.get('user')
#         passwd = request.POST.get('passwd')
#         sex = request.POST.get('sex')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         dep = request.POST.get('department')
#         role_id = request.POST.get('role_id', 3)
#
#         print("*" * 50)
#         print("注册数据：", reg_user, passwd, sex, email, phone, dep)
#         select_user = User.objects.filter(username=reg_user).values()
#         print(select_user)
#         # 用户已存在
#         if select_user:
#             ret = {"status": 1, "result": "faild"}
#             return HttpResponse(json.dumps(ret))
#         else:
#             # 注册成功，写入数据
#             passwd = getmd5.md5(passwd)
#             insert_data = {'username': reg_user, 'password': passwd, "sex": sex, "email": email, "phone": phone,
#                            "dep_id": dep, 'role_id': role_id}
#             User.objects.create(**insert_data)
#             logger.info(
#                 "register info: username:{0},email:{1},phone:{2},department:{3}".format(reg_user, email, phone,
#                                                                                         dep))
#             ret = {"status": 0, "result": "success"}
#             return HttpResponse(json.dumps(ret))
#     dep_obj = Department.objects.values("id", "name")
#     return render(request, "register.html", {'name': dep_obj})
#
#
# # 首页
# @auth
# def index(request):
#     """
#     首页
#     :param request:
#     :return: 首页
#     """
#     username = request.session.get("user")
#     total_host = Hosts.objects.all().count()
#     return render(request, 'host/index.html', {'user': username, "total": total_host})
#

# @auth
# def logout(request):
#     """
#     注销
#     :param request:
#     :return:
#     """
#     if request.method == "GET":
#         user = request.session.get("user")
#         request.session.clear()
#         logger.info("{} logged out success".format(user))
#         return render(request, "login.html")