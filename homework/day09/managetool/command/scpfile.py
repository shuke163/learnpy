#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/6/28 0028

from command import readconf
import paramiko
import re
import os

def batch_scp_help():
    """
    batch_scp 命令的帮助信息
    :return:
    """
    help_info = """\033[0;33m
    Usage: batch_scp [OPTION]...
    Upload or Download files

    -h          h1,h2,h3            hostname
    -g          web,db,kvm          hostgoup
    -action     put|get             upload or download files
    -local      local abspath       The absolute path of the local file     eg: /data/study/pid.py
    -remote     remote abspath      The absolute path of the remote dir     eg: /tmp\033[0m
    """
    print(help_info)

def handle_inp(inp):
    """
    获取用户输入
    :return: 空格分割后的列表
    """
    if (("-h" or "-g") not in inp) or ("-action" not in inp) or ("-local" not in inp) or ("-remote" not in inp):
        # print("\033[1;31mcommand error\033[0m")
        print("\033[1;31mExample: batch_scp -h h1 -g web,db -action put -local test.py -remote /tmp \033[0m")
        return
    else:
        inp_list = inp.split()
        host_dic = {}
        # print("输入的列表: ", inp_list)
        flag = False
        for item in inp_list:
            if "-h" == item:
                flag = True
                continue
            if flag:
                host_dic['host'] = item.split(',')
                flag = False
                break
        for item in inp_list:
            if "-g" == item:
                flag = True
                continue
            if flag:
                host_dic['hostgroup'] = item.split(',')
                flag = False
                break
        for item in inp_list:
            if "-action" == item:
                flag = True
                continue
            if flag:
                host_dic['action'] = item
                flag = False
                break
        for item in inp_list:
            if "-local" == item:
                flag = True
                continue
            if flag:
                host_dic['localpath'] = item
                flag = False
                break
        for item in inp_list:
            if "-remote" == item:
                flag = True
                continue
            if flag:
                host_dic['remotepath'] = item
                break
        return host_dic


def handle_host_info(host_info_dic):
    """
    处理用户输入
    :param host_info_dic: 用户输入得到的列表信息
    :return: 获取对应的主机信息，返回详细的字典信息
    """
    if host_info_dic is None:
        return False
    h = readconf.Handle_conf(readconf.host_file)
    if 'host' in host_info_dic:
        temp_host_li = []
        for item in host_info_dic['host']:
            ip = h.get_value_of_key('host', item)
            port = h.conf.get('host', 'ssh_port')
            user = h.conf.get('host', 'ssh_user')
            passwd = h.conf.get('host', 'ssh_passwd')
            temp_dic = {
                'hostname': item,
                'ip': ip,
                'port': port,
                'user': user,
                'passwd': passwd,
            }
            temp_host_li.append(temp_dic)
            host_info_dic['host'] = temp_host_li

    if 'hostgroup' in host_info_dic:
        node_li = h.get_all_node()
        host_group_li = []
        for item in host_info_dic['hostgroup']:
            if item in node_li:
                port = h.conf.get(item, 'ssh_port')
                user = h.conf.get(item, 'ssh_user')
                passwd = h.conf.get(item, 'ssh_passwd')
            else:
                print("\033[1;31m不存在主机组: %s,请检查!\033[0m" % item)
                continue
            res = h.get_all_info(item)
            # print(res)                                    # 获取节点下所有的键值对
            if res:
                for host in res:
                    matchObj = re.match(r'ssh', host[0])    # 匹配主机名
                    if matchObj:
                        continue
                    else:
                        hostname = host[0]
                        ip = host[1]
                        temp_dic = {
                            'group': item,
                            'hostname': hostname,
                            'ip': ip,
                            'port': port,
                            'user': user,
                            'passwd': passwd,
                        }
                        host_group_li.append(temp_dic)
                        host_info_dic['hostgroup'] = host_group_li
            else:
                print("\033[1;31m主机组: %s为空!\033[0m" % item)
    # print("得到主机详细信息: ", host_info_dic)
    return host_info_dic

def get_all_host(host_info_dic):
    all_host_li = []
    if "host" in host_info_dic:
        host_li = host_info_dic['host']
        for host_item in host_li:
            all_host_li.append(host_item)
    if 'hostgroup' in host_info_dic:
        hostgroup_li = host_info_dic['hostgroup']
        for group_item in hostgroup_li:
            all_host_li.append(group_item)
    return all_host_li


def action_file(action, host_dic, localpath, remotepath):
    """
    上传下载文件
    :param action: 动作
    :param host_dic: 单台主机的字典信息
    :param localpath: 本地文件路径
    :param remotepath: 远程文件路径
    :return:
    """
    flag = False
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_ip = host_dic['ip']
    ssh_port = int(host_dic['port'])
    ssh_user = host_dic['user']
    ssh_passwd = host_dic['passwd']
    # print("ssh: ", ssh_ip, ssh_port, ssh_user, ssh_passwd)        # 对应的主机信息
    ssh.connect(ssh_ip, ssh_port, ssh_user, ssh_passwd)
    stdin, stdout, stderr = ssh.exec_command("ls %s" % remotepath)
    stderr_data = stderr.read().decode()
    if action == "get" and stderr_data:
        print("\033[1;31mERROR: \033[0m", stderr_data)
        return flag
    p = paramiko.Transport((ssh_ip, ssh_port))
    p.connect(username=ssh_user, password=ssh_passwd)
    sftp = paramiko.SFTPClient.from_transport(p)
    if action == "put":
        sftp.put(localpath, remotepath)  # put文件
    elif action == "get":
        local_dir=os.path.dirname(localpath)
        if not os.path.isdir(local_dir):
            os.makedirs(local_dir)
        sftp.get(remotepath, localpath)  # get文件
    p.close()
    print('\033[1;32m%s\t| success | rc=0 >>\033[0m' % ssh_ip)
    print('changed: %s' % "True")
    print('action: %s' % action)
    print('localpath: %s' % localpath)
    print('remotepath: %s\n' % remotepath)
    flag = True
    return flag

# def exec_command(host_info_dic):
#     flag = False
#     action = host_info_dic['action']
#     localpath = host_info_dic['localpath']
#     filename = os.path.basename(localpath)
#     remotepath = host_info_dic['remotepath'].rstrip('/') + '/' + filename
#     if (action != "put") and (action != "get"):
#         print("\033[1;31m当前的执行动作为: %s, 请使用(put|get)模式!" % action)
#         return flag
#     if (not os.path.isabs(localpath)) or (not os.path.isabs(remotepath)):
#         print("\033[1;31m请使用绝对路径,谢谢!\033[0m")
#         print("localpath: %s" % localpath)
#         print("remotepath: %s" % remotepath)
#         return flag
#     print("local: ", localpath, "remote: ", remotepath)  # 文件路径信息
#     if "host" in host_info_dic:
#         host_li = host_info_dic['host']
#         for item in host_li:
#             res = action_file(action, item, localpath, remotepath)
#             if not res:
#                 break
#
#     if "hostgroup" in host_info_dic:
#         hostgroup_li = host_info_dic['hostgroup']
#         for item in hostgroup_li:
#             res = action_file(action, item, localpath, remotepath)
#             if not res:
#                 break

def file_main(inp):
    """
    入口主函数
    :param inp:
    :return:
    """
    flag = False
    inp_dic = handle_inp(inp)                                                   # 处理输入
    host_info_dic = handle_host_info(inp_dic)                                   # 得到主机信息
    if host_info_dic:
        action = host_info_dic['action']                                            # 动作
        localpath = host_info_dic['localpath']                                      # 本地路径
        filename = os.path.basename(localpath)
        remotepath = host_info_dic['remotepath'].rstrip('/') + '/' + filename       # 远程路径
        all_host_li = get_all_host(host_info_dic)                                   # 所有的主机列表
        if (action != "put") and (action != "get"):
            print("\033[1;31m当前的执行动作为: %s, 请使用(put|get)模式!" % action)
            return flag
        if (not os.path.isabs(localpath)) or (not os.path.isabs(remotepath)):
            print("\033[1;31m请使用绝对路径,谢谢!\033[0m")
            print("localpath: %s" % localpath)
            print("remotepath: %s" % remotepath)
            return flag
        if action and all_host_li and localpath and remotepath:
            return action,all_host_li,localpath,remotepath                           # 返回值，提供给action_file函数使用
        else:
            print("\033[1;31m未知错误!\033[0m")
            return flag
    else:
        return flag

if __name__ == '__main__':
    inp = r"batch_scp -h h1,h2,h3 -g web,db -action get -local E:\YQLFC\study\homework\ftp\README.md -remote /tmp"
    res = file_main(inp)
    print(res)
