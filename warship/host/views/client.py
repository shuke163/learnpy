#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/10/14
import requests
import socket
import os
import platform
from multiprocessing import cpu_count


class HostAgent:
    """
    Collect host information agent
    """
    post_dic = {}

    def __init__(self, server_url):
        self.url = server_url

    def get_host_info(self):
        """
        host info
        :return:
        """
        hostname = socket.gethostname()
        eth0 = os.popen(
            "ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6|awk '{print $2}'|tr -d 'addr:'")
        eth1 = "110.100.100.101"
        plat = platform.uname()[0]
        if plat == "Darwin":
            plat = "Linux"
        cpu = cpu_count()
        disk = os.popen("df -h | grep /data | awk '{print $2}'")
        self.post_dic['service_id'] = 2
        self.post_dic['hostname'] = hostname
        self.post_dic['private_ip'] = eth0.read().strip()
        self.post_dic['public_ip'] = eth1
        self.post_dic['os'] = plat
        self.post_dic['cpu'] = cpu
        self.post_dic['mem'] = "8G"
        self.post_dic['disk'] = "500G" if not disk.read().strip() else disk.read().strip()
        self.post_dic['idc_id'] = 2
        self.post_dic['status_id'] = 3
        self.post_dic['owner_id'] = 1
        # print(self.post_dic)
        return self.post_dic

    def send_data(self):
        post_dic = self.get_host_info()
        response = requests.post(self.url, json=post_dic)
        print(response.status_code)


if __name__ == '__main__':
    obj = HostAgent('http://127.0.0.1:9000/host/asset/')
    obj.send_data()