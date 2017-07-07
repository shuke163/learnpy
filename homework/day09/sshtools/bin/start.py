#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/6/28 0028

import os
import sys

BASE_DIR=os.path.normpath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    os.pardir,
))
sys.path.append(BASE_DIR)

from command.execcom import ssh_command,com_main,batch_run_help
from command.scpfile import file_main,action_file,batch_scp_help
from multiprocessing import Pool
import paramiko


if __name__ == '__main__':
    print("#" * 100)
    print("###","\033[1;33mWelcome to command system\033[0m".center(103,' '),"###")
    print("#" * 100)
    while True:
        pool = Pool()
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        exec_li = []
        inp = input("\033[1;32m\n[shuke@myhost ~]# \033[0m").strip()
        # inp = "batch_run -h h1,h2,h3 -g web,db,test -cmd \"df -Th\""     # 输入
        # inp = r"batch_scp -h h1,h2,h3 -g web,db -action get -local E:\YQLFC\study\homework\ftp\README.md -remote /tmp"
        if not inp:continue
        if inp.startswith("batch_run"):                     # 执行命令
            res = com_main(inp)
            if res is not None:
                all_host_li = res[0]
                cmd = res[1]
                for item in all_host_li:
                    res_action = pool.apply_async(ssh_command,args=(ssh, item, cmd))
                    exec_li.append(res_action)
                # print("执行的主机列表: %s" % all_host_li)
                # print("执行的命令: %s" % cmd)
            else:
                batch_run_help()
                continue
        elif inp.startswith("batch_scp"):                   # 上传下载文件
            res = file_main(inp)
            if not res:
                batch_scp_help()
                continue
            else:
                action = res[0]
                all_host_li = res[1]
                localpath = res[2]
                remotepath = res[3]
                for item in all_host_li:
                    res_action = pool.apply_async(action_file,args=(action,item,localpath,remotepath))
                    exec_li.append(res_action)
#		threads = [gevent.spawn(action_file, action, item, localpath, remotepath) for item in all_host_li]  # 单线程并发的方式
        elif inp.lower() == 'q':
            break
        else:
            print("eg: batch_run -h h1,h2,h3 -g web,db -cmd \"df -Th\"")
            print("eg: batch_scp -h h1,h2,h3 -g web,db -action put -local /data/study/pid.py -remote /tmp")
            print("eg: batch_scp -h h1,h2,h3 -g web,db -action get -local /data/study/pid.py -remote /tmp")
            print("eg: (q|Q)")
            continue
        # print("============= 我是分割线 =================")
        pool.close()    # 关闭进程池，防止进一步操作。如果所有操作持续挂起，它们将在工作进程终止前完成
        pool.join()     # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool进程池,join函数等待所有子进程结束
        print("Sub-process(es) done.")
#	gevent.joinall(threads)
        for i in exec_li:
            result = res_action.get()
            if not result:
                continue
