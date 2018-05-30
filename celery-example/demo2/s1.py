from celery_tasks.tasks import hello

result = hello.delay(4, 4)
print(result.id)