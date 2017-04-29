from django.db import models


class Module(models.Model):
    execution = 'execution'
    runner = 'runner'
    wheel = 'wheel'
    TYPE = (
        (execution, execution),
        (runner, runner),
        (wheel, wheel),
    )
    id = models.AutoField(primary_key=True)
    type = models.CharField(choices=TYPE, max_length=20, null=False, verbose_name='模块类型')
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name='模块名称')

    class Meta:
        unique_together = ("type", "name",)
        ordering = ('type', 'name',)


class Command(models.Model):
    id = models.AutoField(primary_key=True)
    module = models.ForeignKey(Module, null=False, on_delete=models.PROTECT, verbose_name='模块')
    fun = models.CharField(max_length=100, null=False, verbose_name='Salt命令')
    doc = models.TextField(max_length=1000, null=True, blank=True, verbose_name='帮助文档')

    class Meta:
        unique_together = ('module', 'fun')
        ordering = ('module__name', 'fun',)


class CommandRecord(models.Model):
    id = models.AutoField(primary_key=True)
    cmd = models.CharField(max_length=1000, null=False, blank=False, verbose_name='命令')
    jid = models.CharField(max_length=50, null=True, blank=True, verbose_name='异步任务ID')
    result = models.TextField(null=True, blank=True, verbose_name='执行结果')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        ordering = ("-id",)
