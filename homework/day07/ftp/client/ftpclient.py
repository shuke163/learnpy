#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Zhaofengfeng'

from conf.settings import BASE_DIR
import sys
import time
import socket
import struct
import json
import os
import hashlib


user_info = {'username':None,'status':False}

class MYTCPClient:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    allow_reuse_address = False
    max_packet_size = 8192
    coding='utf-8'
    request_queue_size = 5
    download_path = os.path.join(BASE_DIR,'client','Download')

    def __init__(self, server_address, connect=True):
        self.server_address=server_address
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)
        if connect:
            try:
                self.client_connect()
            except:
                self.client_close()
                raise

    def client_connect(self):
        self.socket.connect(self.server_address)

    def client_close(self):
        self.socket.close()

    def run(self):
        while True:
            if not user_info['status']:
                self.login()
            else:
                inp = input("退出(exit) >>: ").strip()
                if not inp: continue
                if inp.lower() == 'exit':
                    print("\033[1;32m再见!\033[0m")
                    exit()
                l = inp.split()
                cmd = l[0]
                if hasattr(self, cmd):
                    func = getattr(self, cmd)
                    func(l)

    def login(self):
        while True:
            username=input("请输入用户名: ").strip()
            passwd=input("请输入密码: ").strip()
            if not username or not passwd:continue
            head_dic = {'cmd': 'login','username': username, 'passwd': passwd}
            # print(head_dic)
            head_json = json.dumps(head_dic)
            head_json_bytes = bytes(head_json, encoding=self.coding)
            head_struct = struct.pack('i', len(head_json_bytes))
            self.socket.send(head_struct)
            self.socket.send(head_json_bytes)
            back_msg = self.socket.recv(1024)
            back_msg = back_msg.decode('utf-8')
            if back_msg == "True":
                user_info['username'] = username
                user_info['status'] = True
                print("\033[1;32m欢迎: %s,登陆成功!\033[0m"%username)
            else:
                print(back_msg)
            break

    def file_md5(self,filename):
        h = hashlib.md5(b'welcometobeijing3L')
        with open(filename,'r',encoding='utf-8') as f:
            for lines in f:
                h.update(lines.encode('utf-8'))
                res = h.hexdigest()
                # print('file md5 is: %s'% res)
                return res

    def put(self, args):
        cmd = args[0]
        filename = args[1]
        if not os.path.isfile(filename):
            print('file:%s is not exists' % filename)
            return
        else:
            filesize = os.path.getsize(filename)
        file_md5 = self.file_md5(filename)
        head_dic = {'cmd': cmd, 'filename': os.path.basename(filename), 'filemd5': file_md5, 'filesize': filesize}
        print(head_dic)
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding=self.coding)

        head_struct = struct.pack('i', len(head_json_bytes))
        self.socket.send(head_struct)
        self.socket.send(head_json_bytes)
        send_size = 0
        with open(filename, 'rb') as f:
            for line in f:
                self.socket.send(line)
                send_size += len(line)
            for i in range(100):
                 k = i + 1
                 str = '>'*(i//2)+' '*((100-k)//2)
                 sys.stdout.write('\r'+str+'[%s%%]'%(i+1))
                 sys.stdout.flush()
                 time.sleep(0.1)
            else:
                print('\nupload successful')

    def get(self,args):
        cmd = args[0]
        filename = args[1]
        head_dic = {'cmd': cmd, 'filename': os.path.basename(filename)}
        # print(head_dic)
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding=self.coding)

        head_struct = struct.pack('i', len(head_json_bytes))
        self.socket.send(head_struct)
        self.socket.send(head_json_bytes)

        # 先收报头的长度
        head_struct = self.socket.recv(4)
        head_len = struct.unpack('i', head_struct)[0]

        # 再收报头的bytes
        head_bytes = self.socket.recv(head_len)
        head_json = head_bytes.decode('utf-8')
        head_dic = json.loads(head_json)
        print(head_dic)
        if not head_dic['status']:
            print("\033[1;31m文件不存在...\033[0m")
            return
        else:
            # 最后根据报头里的详细信息取真实的数据
            total_size = head_dic['filesize']
            file_md5 = head_dic['filemd5']
            recv_size = 0
            data = b''
            if not os.path.isdir(self.download_path):
                os.mkdir(self.download_path)
            with open(os.path.join(self.download_path,filename),'wb') as f:
                while recv_size < total_size:
                    recv_data = self.socket.recv(self.max_packet_size)
                    data += recv_data
                    f.write(data)
                    recv_size += len(recv_data)
                    # print(recv_size)
                    # print(data.decode('gbk'))
                    print('recv_size:%s filesize:%s' % (recv_size, total_size))
                for i in range(100):
                    k = i + 1
                    str = '>'*(i//2)+' '*((100-k)//2)
                    sys.stdout.write('\r'+str+'[%s%%]'%(i+1))
                    sys.stdout.flush()
                    time.sleep(0.1)

            res = self.file_md5(os.path.join(self.download_path,filename))
            if file_md5 == res:
                print("\033[1;32m\n文件传输完成，且md5值校验一致!\033[0m")
            else:
                print("\033[1;31m\n文件损坏，md5值校验不一致!\033[0m")

    def dir(self,args):
        cmd = args[0]
        head_dic = {'cmd': cmd}
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding=self.coding)

        head_struct = struct.pack('i', len(head_json_bytes))
        self.socket.send(head_struct)
        self.socket.send(head_json_bytes)

        # 先收报头的长度
        head_struct = self.socket.recv(4)
        head_len = struct.unpack('i', head_struct)[0]

        # 再收报头的bytes
        head_bytes = self.socket.recv(head_len)
        head_json = head_bytes.decode('utf-8')
        head_dic = json.loads(head_json)

        total_size = head_dic['total_size']
        recv_size=0
        data=b''
        while recv_size < total_size:
            recv_data=self.socket.recv(self.max_packet_size)
            data+=recv_data
            recv_size+=len(recv_data)
        print(data.decode('gbk'))

def main():
    """
    入口函数
    """
    print(" 欢迎使用FTP小程序 ".center(50,"*"))
    client = MYTCPClient(('127.0.0.1', 8080))
    client.run()

if __name__ == '__main__':
    main()
