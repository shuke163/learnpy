from django.db import models
import datetime


# Create your models here.

# 部门表
class Department(models.Model):
    name = models.CharField(max_length=16)
    leader = models.CharField(max_length=16)
    create_time = models.DateTimeField(auto_now_add=True)


# 用户信息表
class User(models.Model):
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    sex = models.BooleanField(max_length=1, choices=((0, '男'), (1, '女'),))
    email = models.EmailField(max_length=32)
    phone = models.CharField(max_length=16)
    dep = models.ForeignKey("Department")
    # create_time = models.DateTimeField()
    update_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.username


# idc
# idc  <--> 业务线（多对多）
# idc <--> 主机信息表(一对多)
class Idc(models.Model):
    idc = models.CharField(max_length=16)
    regionId = models.CharField(max_length=16)
    area = models.CharField(max_length=32)
    owner = models.CharField(max_length=16)
    create_time = models.DateTimeField(auto_now_add=True)


# 主机状态表
class Status(models.Model):
    status = models.CharField(max_length=16)
    # offline = models.CharField(max_length=16,verbose_name=u"下线")
    # standby = models.CharField(max_length=16,verbose_name=u"备机")
    # fault = models.CharField(max_length=16,verbose_name=u"故障")


# 业务线
# 业务线  <--> idc(多对多)
# 业务线 <--> 主机信息表(多对多)
class Services(models.Model):
    name = models.CharField(max_length=16)
    owner = models.CharField(max_length=16)
    include_idc = models.ForeignKey("Idc")
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


# 主机信息表
# 主机信息表 <--> 业务线(多对多)
class Hosts(models.Model):
    service = models.ManyToManyField('Services',through="Service2hosts")
    hostname = models.CharField(max_length=32,unique=True)
    private_ip = models.GenericIPAddressField(max_length=32, null=True)
    public_ip = models.GenericIPAddressField(max_length=32, null=True, unique=True)
    idc = models.ForeignKey("Idc")
    os = models.CharField(max_length=16, default="ubuntu 16.04")
    cpu = models.CharField(max_length=10)
    mem = models.CharField(max_length=16)
    disk = models.CharField(max_length=16)
    status = models.ForeignKey("Status")
    owner = models.CharField(max_length=32, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.hostname


# idc与业务线的多对多关系
# class Idc2services(models.Model):
#     idc = models.ForeignKey("Idc")
#     services = models.ForeignKey("Services")


# 业务线与主机信息表的多对多关系
class Service2hosts(models.Model):
    service = models.ForeignKey(to='Services',on_delete=models.CASCADE)
    host = models.ForeignKey(to='Hosts',on_delete=models.CASCADE)

    # 初始化部门表数据
    Department.objects.create(name="销售部",leader="jack")
    Department.objects.create(name="数据运营部",leader="shuke")
    Department.objects.create(name="市场部",leader="jack")
    Department.objects.create(name="广告部",leader="Lucy")
    Department.objects.create(name="行政部",leader="shuke")
    Department.objects.create(name="总裁部",leader="Jone")

    Idc.objects.create(idc="阿里云华北2",regionId="cn-beijing",area="北京",owner="shuke")
    Idc.objects.create(idc="阿里云华东2",regionId="cn-shanghai",area="上海",owner="shuke")
    Idc.objects.create(idc="腾讯云华东地区",regionId="ap-shanghai-1",area="上海",owner="shuke")
    Idc.objects.create(idc="腾讯云华北地区",regionId="ap-beijing-1",area="北京",owner="shuke")
    Idc.objects.create(idc="aws-南美洲",regionId="sa-east-1",area="南美洲(圣保罗)",owner="shuke")

    Services.objects.create(name="官网",owner="beibei",include_idc_id=1)
    Services.objects.create(name="爬虫",owner="keke",include_idc_id=2)
    Services.objects.create(name="电商事业部",owner="shuke",include_idc_id=1)
    Services.objects.create(name="支付",owner="Lucy",include_idc_id="1")

    Status.objects.create(status="online")
    Status.objects.create(status="offline")
    Status.objects.create(status="standby")
    Status.objects.create(status="fault")