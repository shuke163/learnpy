from django.shortcuts import HttpResponse, render, redirect
from host.models import *
import json

# Create your views here.
user_info = {}


# 登陆页面
def login(request):
    return render(request, 'login.html')


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
    return render(request, 'login.html')


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
    return render(request, "register.html", {'name': dep_obj})


# 首页
def index(request):
    # 获取用户输入写入数据库
    host_li = Hosts.objects.values()
    service_line = Services.objects.values("id", "name")
    idc_li = Idc.objects.values("id", "idc")
    status_li = Status.objects.values("id", "status")
    # print("登陆用户：", user_info['user'])
    print("业务线：", service_line)
    print("主机列表：", host_li)
    print("IDC列表：", idc_li)

    host_obj = Hosts.objects.all().select_related('idc', 'status')[:20]
    if host_obj:
        # for item in host_obj:
        #     item.idc = item.idc.idc
        #     item.status = item.status.status
        return render(request, 'index.html', {'user': 'shuke', "service_li": service_line, \
                                              "idc_li": idc_li, "status_li": status_li, 'host_li': host_obj})
    else:
        return render(request,'index.html',{'user': 'shuke',"idc_li": idc_li, "service_li": service_line,"status_li": status_li})


# 添加主机
def addhost(request):
    if request.method == "POST":
        print("==" * 50)
        service_id = request.POST.get('service')
        hostname = request.POST.get('hostname')
        private_ip = request.POST.get('private_ip')
        public_ip = request.POST.get('public_ip')
        idc_id = request.POST.get('idc')
        os = request.POST.get('os')
        cpu = request.POST.get('cpu')
        mem = request.POST.get('mem')
        disk = request.POST.get('disk')
        status_id = request.POST.get('status')
        owner = request.POST.get('owner')
        # 获得用户输入
        print(service_id, hostname, private_ip, public_ip, idc_id, os, cpu, mem, disk, status_id, owner)
        host_info = {"hostname": hostname, "private_ip": private_ip, "public_ip": public_ip, \
                     "idc_id": idc_id, "os": os, "cpu": cpu,"mem": mem, "disk": disk, "status_id": status_id, "owner": owner}
        Hosts.objects.create(**host_info)
        # 多对多表写入,此处使用自定义第三张表的方式
        get_host_id = Hosts.objects.filter(hostname=hostname).values('id')[0]
        Service2hosts_obj = Service2hosts.objects.create(host_id=str(get_host_id['id']), service_id=str(service_id))
        Service2hosts_obj.save()
        # 获取数据返回给前端进行展示
        host_obj = Hosts.objects.all().select_related('idc', 'status')[:20]
        if host_obj:
            return render(request, 'index.html', {'user': 'shuke', 'host_li': host_obj})
    return render(request, 'index.html')


def deletehost(request):
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
    return render(request, 'index.html', {'user': 'shuke', 'host_li': host_info})


def modifyhost(request):
    if request.method == "POST":
        ret = {"status": True, "result": "success", 'error': None}
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
                                                   idc_id=idc_id, os=os, mem=mem, disk=disk, status_id=status_id, owner=owner)
            else:
                ret["status"] = False
                ret["error"] = "主机ID不能为空"
        except Exception as e:
            print("\033[1;32mError: \033[0m", e)
            ret["status"] = False
            ret["error"] = "请求错误"
        return HttpResponse(json.dumps(ret))
