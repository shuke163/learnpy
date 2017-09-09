from django.shortcuts import HttpResponse, render, redirect
from host.views.views import auth
from host.utils import log
from host.models import User, UserRole, Department
from host.utils import getmd5
import json


@auth
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


@auth
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
