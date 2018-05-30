from celery.result import AsyncResult
from demo1.s1 import app

async = AsyncResult(id="97890bf1-2941-4976-92b8-00bf2fbb3cc2", app=app)
# 取消执行定时任务
# async.revoke()
# 终止任务
# async.revoke(terminate=True)

# if async.status == 'SUCESS':
if async.successful():
    result = async.get()
    print(result)
    # async.forget()
else:
    print('任务未执行或失败')