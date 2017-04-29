from django.db import models
from assets.models import Host

ACTION_STATUS = {
    0: '空状态',
    1: '安装失败',
    2: '暂停中',
    3: '启动成功',
    4: '启动失败',
}


class Jinja(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, null=False, blank=False, verbose_name='名称')
    path = models.CharField(max_length=500, null=False, blank=False, verbose_name='文件路径')
    content = models.TextField(null=True, blank=True, verbose_name='文件内容')

    class Meta:
        ordering = ('name',)


class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name='名称')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name="说明")
    fun = models.CharField(max_length=500, null=False, blank=False, verbose_name='State命令')
    path = models.CharField(max_length=500, null=False, blank=False, verbose_name='文件路径')
    content = models.TextField(null=True, blank=True, verbose_name='文件内容')
    successStatus = models.IntegerField(null=False, default=0, verbose_name='成功状态')
    failureStatus = models.IntegerField(null=False, default=0, verbose_name='失败状态')
    jinjas = models.ManyToManyField(Jinja)
    pillars = models.TextField(null=False, blank=False, default="{}", verbose_name='pillar变量的json')

    class Meta:
        ordering = ('name',)


class ServiceType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name='名称')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name="说明")
    states = models.ManyToManyField(State, verbose_name='功能集')

    class Meta:
        ordering = ('name',)


class ServiceGroup(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name='名称')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name="说明")
    serviceTypes = models.ManyToManyField(ServiceType, verbose_name='服务类型集')
    # pillars = {'serviceType1':{'key1':value1, 'key2':value2, ...}, 'serviceType2':{..}}
    pillars = models.TextField(null=False, blank=False, default="{}", verbose_name='pillar数据')
    hasNewPillars = models.BooleanField(null=False, default=False, verbose_name='是否有新增pillar变量')

    class Meta:
        ordering = ('name',)


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False, blank=False, verbose_name='名称')
    remark = models.CharField(max_length=100, null=True, blank=True, verbose_name="说明")
    host = models.ForeignKey(Host, null=False, on_delete=models.PROTECT, verbose_name='主机')
    group = models.ForeignKey(ServiceGroup, null=False, on_delete=models.PROTECT, verbose_name='服务组')
    type = models.ForeignKey(ServiceType, null=False, on_delete=models.PROTECT, verbose_name='服务类型')
    status = models.IntegerField(null=False, default=0, verbose_name='当前状态')
    currentJobId = models.IntegerField(null=False, default=-1, verbose_name='当前任务id')
    currentJobDesc = models.CharField(max_length=100, null=True, blank=True, verbose_name='当前任务说明')
    # TODO：服务私有的pillar = {'key1':value1, 'key2':value2, ...}
    pillars = models.TextField(null=True, blank=True, verbose_name='pillar变量的json')

    class Meta:
        ordering = ('group__name', 'type__name', 'name',)


class ServiceJob(models.Model):
    id = models.AutoField(primary_key=True)
    jid = models.CharField(max_length=50, null=True, blank=True, verbose_name='任务ID')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name='服务')
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name='功能')
    result = models.TextField(null=True, blank=True, verbose_name='执行结果')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ("-id",)
