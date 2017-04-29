from celery import shared_task

from service.models import *
from job.salt import SaltAPI
import json


@shared_task
def syncJobStatus():
    jobs = ServiceJob.objects.filter(result=None)
    api = SaltAPI()
    for job in jobs:
        rsp = api.jobs(job.jid)
        data = rsp['info'][0]['Result']
        # TODO：任务成功/失败的判断
        if data and data != "{}":
            job.result = json.dumps(data)
            job.service.currentJobId = -1
            job.service.currentJobDesc = ""
            job.service.status = job.state.successStatus
            job.service.save()
            job.save()
