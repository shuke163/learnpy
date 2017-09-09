from django.db import models


# Create your models here.
class Department(models.Model):
    """
    部门表
    """
    name = models.CharField(max_length=16)
    leader = models.CharField(max_length=16)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(models.Model):
    """
    用户信息表
    """
    username = models.CharField(max_length=16)
    password = models.CharField(max_length=32)
    sex = models.BooleanField(max_length=1, choices=((0, '男'), (1, '女'),))
    email = models.EmailField(max_length=32)
    phone = models.CharField(max_length=16)
    dep = models.ForeignKey("Department")
    role = models.ForeignKey("UserRole", default=3)
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class UserRole(models.Model):
    """
    角色信息表
    """
    rolename = models.CharField(max_length=16)
    permissions = models.CharField(max_length=16)
    # user = models.ForeignKey("User")
    update_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rolename


# idc  <--> 业务线（多对多）
# idc <--> 主机信息表(一对多)
class Idc(models.Model):
    """
    云主机idc表
    """
    idc = models.CharField(max_length=16)
    regionId = models.CharField(max_length=16)
    area = models.CharField(max_length=32)
    owner = models.ForeignKey("User")
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.idc


# 主机状态表
class Status(models.Model):
    """
    主机状态表
    """
    status = models.CharField(max_length=16)


# 业务线  <--> idc(多对多)
# 业务线 <--> 主机信息表(多对多)
class Services(models.Model):
    """
    业务线表
    """
    name = models.CharField(max_length=16)
    owner = models.ForeignKey("User")
    idc = models.ForeignKey("Idc")
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


# 主机信息表 <--> 业务线(多对多)
class Hosts(models.Model):
    """
    主机信息表
    """
    hostname = models.CharField(max_length=32, unique=True)
    private_ip = models.GenericIPAddressField(max_length=32, null=True)
    public_ip = models.GenericIPAddressField(max_length=32, null=True, unique=True)
    service = models.ManyToManyField('Services', through="Service2hosts")
    os = models.CharField(max_length=16, default="ubuntu 16.04")
    cpu = models.CharField(max_length=10)
    mem = models.CharField(max_length=16)
    disk = models.CharField(max_length=16)
    idc = models.ForeignKey("Idc")
    status = models.ForeignKey("Status")
    owner = models.ForeignKey("User")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.hostname

    def __str__(self):
        return self.hostname


# idc与业务线的多对多关系
# class Idc2services(models.Model):
#     idc = models.ForeignKey("Idc")
#     services = models.ForeignKey("Services")


class Service2hosts(models.Model):
    """
    业务线与主机信息表的多对多关系表
    """
    service = models.ForeignKey(to='Services', on_delete=models.CASCADE)
    host = models.ForeignKey(to='Hosts', on_delete=models.CASCADE)

    # Idc.objects.create(idc="阿里云华北2",regionId="cn-beijing",area="北京",owner="shuke")
    # Idc.objects.create(idc="阿里云华东2",regionId="cn-shanghai",area="上海",owner="shuke")
    # Idc.objects.create(idc="腾讯云华东地区",regionId="ap-shanghai-1",area="上海",owner="shuke")
    # Idc.objects.create(idc="腾讯云华北地区",regionId="ap-beijing-1",area="北京",owner="shuke")
    # Idc.objects.create(idc="aws-南美洲",regionId="sa-east-1",area="南美洲(圣保罗)",owner="shuke")
    #
    # # Services.objects.create(name="官网",owner=1,idc_id=1)
    # # Services.objects.create(name="爬虫",owner=2,idc_id=2)
    # # Services.objects.create(name="电商事业部",owner=3,idc_id=1)
    # # Services.objects.create(name="支付",owner=1,idc_id=1)
    #
    # Status.objects.create(status="online")
    # Status.objects.create(status="offline")
    # Status.objects.create(status="standby")
    # Status.objects.create(status="fault")

    # Department.objects.create(name="销售部", leader="jack")
    # Department.objects.create(name="数据运营部", leader="shuke")
    # Department.objects.create(name="市场部", leader="jack")
    # Department.objects.create(name="广告部", leader="Lucy")
    # Department.objects.create(name="行政部", leader="shuke")
    # Department.objects.create(name="总裁部", leader="Jone")
