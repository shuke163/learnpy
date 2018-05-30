from celery.result import AsyncResult
from demo1.s1 import app

async = AsyncResult(id="da06dda8-2134-4a64-b40d-0e21b1cb867f", app=app)

if async.successful():
    result = async.get()
    print(result)
else:
    print('任务未执行或失败')