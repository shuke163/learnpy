from django.shortcuts import HttpResponse, render, redirect
from host.models import *
from host.utils import getmd5
from host.utils.log import logger
import json


def auth(func):
    """
    试图功能函数装饰器
    :param func: 被装饰的函数
    :return: 用户携带session则允许访问函数，返回函数对象并执行
    """

    def wrap(requerst, *args, **kwargs):
        session = requerst.session.get('user')
        if not session:
            return redirect("/login/")
        return func(requerst, *args, **kwargs)

    return wrap


# 登陆页面
def login(request):
    """
    登陆认证函数
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        pwd = getmd5.md5(pwd)
        query_obj = User.objects.filter(username=user, password=pwd).first()
        if query_obj:
            request.session['user'] = user
            request.session['is_login'] = True
            logger.info("username: %s,login success" % user)
            return redirect("index")
        else:
            return render(request, 'login.html', {'msg': '用户名或密码错误!'})


# 认证
# def auth(request):
#     dt = datetime.datetime.now()
#     if request.method == "POST":
#         user = request.POST.get('user')
#         pwd = request.POST.get('pwd')
#         query_obj = User.objects.filter(username=user).values("username", "password")
#         if query_obj:
#             username = query_obj[0]['username']
#             password = query_obj[0]['password']
#             if user == username and pwd == password:
#                 print("*" * 100)
#                 print("当前时间： %s,登陆成功用户：%s" % (dt, user))
#                 index = "/host/index/"
#                 return redirect(index)
#     return render(request, 'host/login.html')


# 注册试图
def register(request):
    """
    注册函数
    :param request:
    :return:
    """
    if request.method == "POST":
        reg_user = request.POST.get('user')
        passwd = request.POST.get('passwd')
        sex = request.POST.get('sex')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dep = request.POST.get('department')
        role_id = request.POST.get('role_id', 3)

        print("*" * 50)
        print("注册数据：", reg_user, passwd, sex, email, phone, dep)
        select_user = User.objects.filter(username=reg_user).values()
        print(select_user)
        # 用户已存在
        if select_user:
            ret = {"status": 1, "result": "faild"}
            return HttpResponse(json.dumps(ret))
        else:
            # 注册成功，写入数据
            passwd = getmd5.md5(passwd)
            insert_data = {'username': reg_user, 'password': passwd, "sex": sex, "email": email, "phone": phone,
                           "dep_id": dep, 'role_id': role_id}
            User.objects.create(**insert_data)
            logger.info(
                "register info: username:{0},email:{1},phone:{2},department:{3}".format(reg_user, email, phone,
                                                                                        dep))
            ret = {"status": 0, "result": "success"}
            return HttpResponse(json.dumps(ret))
    dep_obj = Department.objects.values("id", "name")
    return render(request, "register.html", {'name': dep_obj})


# 首页
@auth
def index(request):
    """
    首页
    :param request:
    :return: 首页
    """
    username = request.session.get("user")
    total_host = Hosts.objects.all().count()
    return render(request, 'host/index.html', {'user': username, "total": total_host})


@auth
def logout(request):
    """
    注销
    :param request:
    :return:
    """
    if request.method == "GET":
        user = request.session.get("user")
        request.session.clear()
        logger.info("{} logged out success".format(user))
        return render(request, "login.html")
