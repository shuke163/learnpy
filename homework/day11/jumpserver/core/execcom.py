#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/6/27 0027

import paramiko
from conf.settings import logger
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


def batch_run_help():
    """
    batch_run 命令的帮助信息
    :return:
    """
    help_info = """\033[0;33m
    Usage: batch_run [OPTION]...
    Remote execution command

    -h      h1,h2,h3    hostname
    -g      web,db,kvm  hostgoup
    -cmd    command     eg: 'df -Th';'free -m';\033[0m
    """
    print(help_info)


def handle_inp(inp):
    """
    :return: 返回一个包含主机和命令信息的字典
    """
    if (("-h" or "-g") not in inp) or ("-cmd" not in inp):
        print("\033[1;31mExample: batch_run -h web09,web07 -g web -cmd \"df -Th\" \033[0m")
        return
    else:
        inp_l = inp.split()
        host_dic = {}
        flag = False
        for item in inp_l:
            if item == "-h":
                flag = True
                continue
            if flag:
                host_dic['host'] = item.split(',')
                flag = False
                break
        for item in inp_l:
            if item == "-g":
                flag = True
                continue
            if flag:
                host_dic['hostgroup'] = item.split(',')
                flag = False
                break
        for item in inp_l:
            if item == "-cmd":
                comm_index = (inp_l.index(item) + 1)
                temp_li = inp_l[comm_index:]
                flag = True
                continue
            if flag:
                host_dic['cmd'] = ' '.join(temp_li)
                break
        # print(host_dic)
        return host_dic


def get_all_host(host_li, all_host_dic):
    """
    得到所有需要执行的主机列表
    :param host_li: 用户输入切分后的列表
    :param all_user_host: 数据库中用户有权限操作的主机列表
    :return: 可以操作的主机列表
    """
    all_host_li = []
    exec_host_li = []
    if 'host' in host_li.keys():
        inp_host = host_li['host']
        for item in all_host_dic:
            all_host_li.append(item['hostname'])
        for hostname in inp_host:
            if hostname not in all_host_li:
                print("\033[1;31m主机不存在: %s,请检查!\033[0m" % hostname)
                index = inp_host.index(hostname)
                inp_host.remove(hostname)
                inp_host.insert(index, None)
        if inp_host:
            for hostname in inp_host:
                for item in all_host_dic:
                    if hostname == item['hostname']:
                        exec_host_li.append(item)
    if 'hostgroup' in host_li.keys():
        inp_group = host_li['hostgroup']
        for item in all_host_dic:
            all_host_li.append(item['group_name'])
        for hostgroup in inp_group:
            if hostgroup not in all_host_li:
                print("\033[1;31m主机组不存在: %s,请检查!\033[0m" % hostgroup)
                index = inp_group.index(hostgroup)
                inp_group.remove(hostgroup)
                inp_group.insert(index, None)
        if inp_group:
            for hostgroup in inp_group:
                for item in all_host_dic:
                    if hostgroup == item['group_name']:
                        exec_host_li.append(item)
    return exec_host_li


def ssh_command(host_dic, cmd):
    """
    执行ssh命令并输出结果
    :param ssh_obj: ssh对象
    :param host_dic: 主机信息字典
    :return:
    """
    ip = host_dic['public_ip']
    ssh_port = int(host_dic['ssh_port'])
    ssh_user = host_dic['username']
    passwd = host_dic['password']
    cmd = cmd
    ssh_obj = paramiko.SSHClient()
    ssh_obj.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # print("执行的命令信息: ", ip, ssh_port, ssh_user, passwd, cmd)  # 对应的主机信息
    logger.info("ip:%s ssh_port:%d, ssh_user:%s, cmd:%s" % (ip, ssh_port, ssh_user, cmd))
    ssh_obj.connect(ip, ssh_port, ssh_user, passwd, timeout=300)
    stdin, stdout, stderr = ssh_obj.exec_command(cmd)
    stdout_data = stdout.read().decode()
    if stdout_data:
        print('\033[1;32m%s\t| success | rc=0 >>\033[0m' % ip)
        return stdout_data
    else:
        print('\033[1;31m%s\t| failed | rc !=0 >>\033[0m' % ip)
        stderr_data = stderr.read().decode()
        return stderr_data


def task(exec_host_li, cmd):
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(ssh_command, host_dic, cmd) for host_dic in exec_host_li]
        for future in as_completed(futures):
            print(future.result())


def main(all_host_dic):
    while True:
        inp = input("\033[1;32m\n[shuke@myhost ~]# \033[0m").strip()
        if not inp: continue
        if inp.startswith("batch_run"):             # 执行命令
            inp_dic = handle_inp(inp)
            if inp_dic is not None:
                cmd = inp_dic['cmd'].strip('"')
                exec_host_li = get_all_host(inp_dic, all_host_dic)
                if not exec_host_li: continue
                # print(exec_host_li)               # 待执行的主机信息
                task(exec_host_li, cmd)             # 线程池函数task
            else:
                batch_run_help()
                continue
        elif inp.lower() == 'q':
            try:
                print("\033[1;32m再见!\033[0m")
                exit()
            except AttributeError as e:
                pass
        else:
            print("eg: batch_run -h web09,web07 -g web,db -cmd \"df -Th\"")
            print("eg: (q|Q)")
            continue


if __name__ == '__main__':
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    cmd = "df"
    host_li = [{'private_ip': '192.168.1.6', 'password': 'Shuke163@163.com', 'ssh_port': '63008', 'hostname': 'web09',
                'username': 'shuke', 'public_ip': '119.29.237.119'},
               {'private_ip': '192.168.1.6', 'password': 'Shuke163@163.com', 'ssh_port': '63008', 'hostname': 'web09',
                'username': 'shuke', 'public_ip': '119.29.237.119'},
               {'private_ip': '192.168.1.6', 'password': 'Shuke163@163.com', 'ssh_port': '63008', 'hostname': 'web09',
                'username': 'shuke', 'public_ip': '119.29.237.119'}]
    for item in host_li:
        ssh_command(ssh, item, cmd)
