import datetime
from flask import Flask, render_template, request, redirect
from celery.result import AsyncResult

from celery_tasks.celery import cel
from celery_tasks.tasks import deploy

app = Flask(__name__)

HISTORY = []


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', history=HISTORY)


@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'GET':
        return render_template('publish.html')
    else:
        version = request.form.get('version')
        hosts = request.form.getlist('hosts')
        print(version, hosts)

        ctime = datetime.datetime.now()
        utc_ctime = datetime.datetime.utcfromtimestamp(ctime.timestamp())
        ctime_10 = utc_ctime + datetime.timedelta(seconds=10)

        result = deploy.apply_async(args=[version, hosts, ], eta=ctime_10)
        # result.id 将随机字符串放入数据库
        HISTORY.append({'version': version, 'hosts': hosts, 'task_id': result.id})
        print("========", HISTORY)
        return redirect('/index')


@app.route('/check_result')
def check_result():
    task_id = request.args.get('task_id')
    async = AsyncResult(id=task_id, app=cel)
    if async.successful():
        result = async.get()
        print(result)
        # async.forget()  # 将结果删除
        return "执行成功"
    elif async.failed():
        return '执行失败'
    elif async.status == 'PENDING':
        return '任务等待中被执行'
    elif async.status == 'RETRY':
        return '任务异常后正在重试'
    elif async.status == 'STARTED':
        return '任务已经开始被执行'
    else:
        return '未知状态'


@app.route('/cancel')
def cancel():
    task_id = request.args.get('task_id')
    async = AsyncResult(id=task_id, app=cel)
    async.revoke(terminate=True)
    return "取消成功"


if __name__ == '__main__':
    app.run()
