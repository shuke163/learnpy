#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/6/27 0027

from multiprocessing import Pool
from command import readconf
import paramiko
import re

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
        print("\033[1;31mExample: batch_run -h h1,h2,h3 -g web,db -cmd  \"df -Th\" \033[0m")
        return
    else:
        inp_l = inp.split()
        host_dic={}
        flag = False
        for item in inp_l:
            if item == "-h":
                flag = True
                continue
            if flag:
                host_dic['host']=item.split(',')
                flag = False
                break
        for item in inp_l:
            if item == "-g":
                flag = True
                continue
            if flag:
                host_dic['hostgroup']=item.split(',')
                flag = False
                break
        for item in inp_l:
            if item == "-cmd":
                comm_index = (inp_l.index(item) + 1)
                temp_li = inp_l[comm_index:]
                flag = True
                continue
            if flag:
                host_dic['cmd']=' '.join(temp_li)
                break
        # print(host_dic)
        return host_dic

def get_host_info(com_dic):
    """
    根据用户输入得到主机信息
    :param com_dic: 返回获取主机信息后的详细列表
    :return:
    """
    h = readconf.Handle_conf(readconf.host_file)
    if com_dic is None:
        return
    if 'host' in com_dic:
        host_key=h.get_all_key('host')
        temp_host_li = []
        for item in com_dic['host']:
            if item in host_key:
                ip = h.get_value_of_key('host',item)
                port = h.conf.get('host','ssh_port')
                user = h.conf.get('host','ssh_user')
                passwd = h.conf.get('host','ssh_passwd')
                temp_dic = {
                    'hostname':item,
                    'ip': ip,
                    'port': port,
                    'user': user,
                    'passwd': passwd,
                }
                temp_host_li.append(temp_dic)
            else:
                print("\033[1;31m主机不存在: %s,请检查!\033[0m" % item)
                continue
        com_dic['host']=temp_host_li
        # print(com_dic)
    if 'hostgroup' in com_dic:
        node_li = h.get_all_node()
        host_group_li = []
        for item in com_dic['hostgroup']:
            if item in node_li:
                port = h.conf.get(item, 'ssh_port')
                user = h.conf.get(item, 'ssh_user')
                passwd = h.conf.get(item, 'ssh_passwd')
            else:
                print("\033[1;31m不存在主机组: %s,请检查!\033[0m" % item)
                continue
            res = h.get_all_info(item)
            # print(res)        # 输入节点下所有的键值对
            if res:
                for host in res:
                    matchObj = re.match(r'ssh',host[0])         # 匹配主机名
                    if matchObj:
                        continue
                    else:
                        hostname = host[0]
                        ip = host[1]
                        temp_dic = {
                            'group':item,
                            'hostname': hostname,
                            'ip': ip,
                            'port': port,
                            'user': user,
                            'passwd': passwd,
                        }
                        host_group_li.append(temp_dic)
                com_dic['hostgroup']=host_group_li
            else:
                print("\033[1;31m主机组: %s为空!\033[0m"%item)
    return com_dic


def get_all_host(exec_com_dic):
    """
    得到所有需要执行的主机列表
    :param exec_com_dic: 展开后的字典信息
    :return: all_host_li
    """
    all_host_li=[]
    if exec_com_dic is None:
        return
    if 'host' in exec_com_dic:
        host_ip_li = exec_com_dic['host']
        for item in host_ip_li:
            all_host_li.append(item)
    if 'hostgroup' in exec_com_dic:
        hostgroup_li = exec_com_dic['hostgroup']
        for item in hostgroup_li:
            all_host_li.append(item)
    # print(all_host_li)
    return all_host_li


def ssh_command(ssh_obj,host_dic,cmd):
    """
    执行ssh命令并输出结果
    :param ssh_obj: ssh对象
    :param host_dic: 主机信息字典
    :return:
    """
    ip = host_dic['ip']
    port = int(host_dic['port'])
    user = host_dic['user']
    passwd = host_dic['passwd']
    cmd = cmd
    # print("执行的命令信息: ",ip,port,user,passwd,cmd)        # 对应的主机信息
    # print("执行的命令信息: ",cmd)
    ssh_obj.connect(ip, port, user, passwd)
    stdin, stdout, stderr = ssh_obj.exec_command(cmd)
    stdout_data = stdout.read().decode()
    if stdout_data:
        print('\033[1;32m%s\t| success | rc=0 >>\033[0m' % ip)
        print(stdout_data)
    else:
        print('\033[1;31m%s\t| failed | rc !=0 >>\033[0m' % ip)
        print(stderr.read().decode())
#
# def exec_command(exec_com_dic):
#     """
#     执行命令函数
#     :param exec_com_dic: 主机信息详细字典列表
#     :return:
#     """
#     cmd = exec_com_dic['cmd'].strip('"')
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     # print(exec_com_dic)                                             # 主机信息详细字典列表
#     if 'host' in exec_com_dic:
#         host_ip_li = exec_com_dic['host']
#         # print('主机列表: ',host_ip_li)
#         for item in host_ip_li:
#             ssh_command(ssh,item,cmd)                                      # 调用ssh_command函数
#     if 'hostgroup' in exec_com_dic:
#         hostgroup_li = exec_com_dic['hostgroup']
#         # print('主机列表: ',hostgroup_li)
#         for item in hostgroup_li:
#             ssh_command(ssh, item,cmd)
#     print('----->')
#     ssh.close()

def com_main(inp):
    """
    主函数
    :param inp:
    :return:
    """
    com_dic = handle_inp(inp)
    exec_com_dic = get_host_info(com_dic)
    all_host_li = get_all_host(exec_com_dic)
    if all_host_li is not None:
        cmd = exec_com_dic['cmd'].strip('"')
    if all_host_li and cmd:
        # print(all_host_li,cmd)
        return all_host_li,cmd



if __name__ == '__main__':
    inp = "batch_run -h h1,h2,h3 -g web,db,test -cmd \"df -Th\""
    res=com_main(inp)
    print(res)

