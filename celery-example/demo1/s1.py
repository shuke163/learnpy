from celery import Celery

app = Celery('tasks',
             broker='redis://192.168.11.91:6379',
             backend='redis://192.168.11.91:6379')

@app.task
def xxxxxx(x, y):
    return x + y