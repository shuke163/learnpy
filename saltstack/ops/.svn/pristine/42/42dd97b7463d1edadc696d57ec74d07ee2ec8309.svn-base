from __future__ import absolute_import, unicode_literals
from celery import shared_task
from job.salt import SaltAPI
from assets.models import HostGroup, Host
from django.utils.timezone import now


@shared_task
def hostSyncTask():
    try:
        try:
            group = HostGroup.objects.get(name='备用组')
        except HostGroup.DoesNotExist:
            group = HostGroup(name='备用组')
            group.save()

        api = SaltAPI()
        rsp = api.minions()
        datas = rsp['return'][0]
        onlines = set()
        updateTime = now()
        for saltId, data in datas.items():
            serialNumber = data['serialnumber']
            try:
                host = Host.objects.get(serialNumber=serialNumber)
            except Host.DoesNotExist:
                # 新建的机器全部放在备用组
                host = Host(serialNumber=serialNumber, hostGroup=group)
            ips = data['ip_interfaces']
            if 'eth0' in ips and len(ips['eth0']) > 0:
                host.ip = ips['eth0'][0]
            if 'eth1' in ips and len(ips['eth1']) > 0:
                host.ipEth1 = ips['eth1'][0]
            host.kernel = data['kernel']
            host.os = data['os']
            host.osArch = data['osarch']
            host.osRelease = data['osrelease']
            host.saltId = saltId
            host.saltStatus = Host.ONLINE
            host.updateTime = updateTime
            host.save()
            onlines.add(serialNumber)
        for host in Host.objects.all():
            if host.serialNumber not in onlines:
                host.saltStatus = Host.OFFLINE
                host.save()
        return 0
    except Exception:
        return 1
