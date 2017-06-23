#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Zhaofengfeng'

from server import account
from conf.settings import BASE_DIR,DATABASE
import socket
import struct
import json
import os
import hashlib
import subprocess


class MYTCPServer:
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    allow_reuse_address = False
    max_packet_size = 8192
    coding = 'utf-8'
    request_queue_size = 5
    server_dir = 'file_upload'
    user_info_dic = {'username':None,'quota_space':None,'status':False}

    def __init__(self, server_address, bind_and_activate=True):
        """Constructor.  May be extended, do not override."""
        self.server_address = server_address
        self.socket = socket.socket(self.address_family,
                                    self.socket_type)
        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise

    def server_bind(self):
        """Called by constructor to bind the socket.
        """
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def server_activate(self):
        """Called by constructor to activate the server.
        """
        self.socket.listen(self.request_queue_size)

    def server_close(self):
        """Called to clean-up the server.
        """
        self.socket.close()

    def get_request(self):
        """Get the request and client address from the socket.
        """
        return self.socket.accept()

    def close_request(self, request):
        """Called to clean up an individual request."""
        request.close()

    def run(self):
        while True:
            self.conn, self.client_addr = self.get_request()
            print('from client ', self.client_addr)
            while True:
                try:
                    head_struct = self.conn.recv(4)
                    if not head_struct: break
                    head_len = struct.unpack('i', head_struct)[0]
                    head_json = self.conn.recv(head_len).decode(self.coding)
                    head_dic = json.loads(head_json)
                    # head_dic={'cmd':'put','filename':'a.txt','filesize':123123}
                    cmd = head_dic['cmd']
                    if hasattr(self, cmd):
                        func = getattr(self, cmd)
                        func(head_dic)
                except Exception:
                    break

    def login(self,args):
        """
        登陆
        """
        user_name = args['username']
        tag = account.query_user(user_name)
        if tag:
            user_info_li = account.id_and_user()
            for item in user_info_li:
                if item['username'] == user_name and item['password'] == args['passwd']:
                    print("\033[1;32m登陆成功: %s\033[0m" % user_name)
                    self.user_info_dic = {'username':user_name,'quota_space':item['quota_space'],'status':True}
                    # print("dic",self.user_info_dic)
                    back_msg=bytes("True",encoding='utf-8')
                    self.conn.send(back_msg)
                    if not os.path.isdir(os.path.join(DATABASE['home_dir'],user_name)):
                        os.makedirs(os.path.join(DATABASE['home_dir'],user_name))
                    break
            else:
                print("\033[1;31m用户名或密码错误!\033[0m")
                self.conn.send(bytes("用户名或密码错误!",encoding='utf-8'))
        else:
            print("\033[1;31m用户不存在!\033[0m")
            self.conn.send(bytes("用户不存在!",encoding='utf-8'))

    def file_md5(self,filename):
        """
        文件md5
        """
        h = hashlib.md5(b'welcometobeijing3L')
        with open(filename,'r',encoding='utf-8') as f:
            for lines in f:
                h.update(lines.encode('utf-8'))
                res = h.hexdigest()
                # print('file md5 is: %s'% res)
                return res

    def put(self, args):
        """
        上传文件
        """
        file_path = os.path.normpath(os.path.join(DATABASE['home_dir'],self.user_info_dic['username'],args['filename']))
        filesize = args['filesize']
        file_md5 = args['filemd5']
        recv_size = 0
        print('----->', file_path)
        # if not os.path.isdir(os.path.join(DATABASE['home_dir'],self.user_info_dic['username'])):
        #     os.mkdir(os.path.join(DATABASE['home_dir'],self.user_info_dic['username']))
        with open(file_path, 'wb') as f:
            while recv_size < filesize:
                recv_data = self.conn.recv(self.max_packet_size)
                f.write(recv_data)
                recv_size += len(recv_data)
                print('recvsize:%s filesize:%s' % (recv_size, filesize))
        res = self.file_md5(file_path)
        if file_md5 == res:
            print("\033[1;32m文件传输完成，且md5值校验一致!\033[0m")
        else:
            print("\033[1;31m文件损坏，md5值校验不一致!\033[0m")

    def get(self,args):
        """
        下载文件
        """
        filename = os.path.normpath(os.path.join(DATABASE['home_dir'],self.user_info_dic['username'],args['filename']))
        if not os.path.isfile(filename):
            print('file:%s is not exists' % filename)
            head_dic = {'filename': args['filename'],'status':False}
            # return
        else:
            filesize = os.path.getsize(filename)
            file_md5 = self.file_md5(filename)
            head_dic = {'filename': args['filename'], 'filemd5': file_md5, 'filesize': filesize,'status':True}
            print(head_dic)
        head_json = json.dumps(head_dic)
        head_json_bytes = bytes(head_json, encoding=self.coding)
        head_struct = struct.pack('i', len(head_json_bytes))
        self.conn.send(head_struct)
        self.conn.send(head_json_bytes)
        if head_dic['status']:
            print("开始传输文件...",filename)
            with open(filename, 'rb') as f:
                for line in f:
                    self.conn.send(line)
                else:
                    print('\033[1;32msend successful!\033[0m')

    def dir(self,args):
        """
        显示用户家目录列表
        """
        cmd = args['cmd']
        home_path = os.path.normpath(os.path.join(DATABASE['home_dir'],self.user_info_dic['username']))
        res=subprocess.Popen(cmd,cwd=home_path,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        err=res.stderr.read()
        if err:
            cmd_res=err
        else:
            cmd_res=res.stdout.read()
        head_dic={'total_size':len(cmd_res)}
        head_json=json.dumps(head_dic)
        head_bytes=head_json.encode('utf-8')
        self.conn.send(struct.pack('i',len(head_bytes)))
        self.conn.send(head_bytes)
        self.conn.send(cmd_res)

def main():
    """
    入口函数
    """
    tcpserver1 = MYTCPServer(('127.0.0.1', 8080))
    tcpserver1.run()

if __name__ == '__main__':
    main()