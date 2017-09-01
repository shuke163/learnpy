from django.shortcuts import HttpResponse, render, redirect
from host.models import *
import json

# Create your views here.
user_info = {}


# 登陆页面
def login(request):
    return render(request, 'host/login.html')


# 认证
def auth(request):
    dt = datetime.datetime.now()
    if request.method == "POST":
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        query_obj = User.objects.filter(username=user).values("username", "password")
        if query_obj:
            username = query_obj[0]['username']
            password = query_obj[0]['password']
            if user == username and pwd == password:
                print("*" * 100)
                print("当前时间： %s,登陆成功用户：%s" % (dt, user))
                user_info['user'] = user
                index = "/host/index/"
                return redirect(index)
    return render(request, 'host/login.html')


# 注册试图
def register(request):
    if request.method == "POST":
        reg_user = request.POST.get('user')
        passwd = request.POST.get('passwd')
        sex = request.POST.get('sex')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        print("*" * 50)
        print("注册数据：", reg_user, passwd, sex, email, phone, department)
        select_user = User.objects.filter(username=reg_user).values()
        print(select_user)
        # 用户已存在
        if select_user:
            ret = {"status": 1, "result": "faild"}
            return HttpResponse(json.dumps(ret))
        else:
            # 注册成功，写入数据
            insert_data = {'username': reg_user, 'password': passwd, "sex": sex, "email": email, "phone": phone,
                           "dep_id": department}
            User.objects.create(**insert_data)
            ret = {"status": 0, "result": "success"}
            return HttpResponse(json.dumps(ret))
    dep_obj = Department.objects.values("id", "name")
    return render(request, "host/register.html", {'name': dep_obj})


# 首页
def index(request):
    total_host = Hosts.objects.all()
    return render(request, 'host/index.html', {'user': 'shuke', "total": total_host})
