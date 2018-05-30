from .celery import cel


@cel.task
def deploy(version,hosts):
    # subpocess.check_output('....',cwd="xxxx")
    # salt "web*" cmd.run "ifconfig"
    # stackstack的state
    #   - 同步文件
    #   - 执行脚本
    # salt '*' state.sls s7code  pillar='{"appname": "luffy"}'
    # subpocess.check_output(salt '*' state.sls s7code  pillar='{"appname": "luffy"}')
    print('执行代码发布的任务')
    return 200

