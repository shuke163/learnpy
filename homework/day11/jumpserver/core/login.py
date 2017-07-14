#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/7/10 0010

import pymysql
from prettytable import PrettyTable
from conf.settings import logger, DATABASE


class Auth_show_info:
    def __init__(self, login_user, login_pwd):
        self.login_user = login_user
        self.login_pwd = login_pwd
        self.conn = pymysql.connect(**DATABASE)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        self.tb = PrettyTable(["用户ID", "用户名", "邮箱", "部门"])
        self.host_tb = PrettyTable(["ID", "主机名称", "内网IP", "公网IP"])

    def db_close(self):
        self.cursor.close()
        self.conn.close()

    def show_user_info(self):
        self.cursor.execute(
                "select * from user where username='%s' and password='%s'" % (self.login_user, self.login_pwd))
        row_data = self.cursor.fetchone()
        if row_data:
            self.cursor.execute("SELECT  A.uid,A.username,A.mail,B.title FROM user as A \
            LEFT JOIN department as B on A.department_id=B.pid \
            WHERE A.username='%s'" % self.login_user)
            result = self.cursor.fetchone()
            if result:
                self.tb.align["用户ID"] = "2"
                self.tb.padding_width = 1
                user_info_li = [result['uid'], result['username'], result['mail'], result['title']]
                self.tb.add_row(user_info_li)
                print()
                print("\033[1;32m 当前用户信息\033[0m ".center(50, '*'))
                print(self.tb)
                logger.info("user: %s,success!" % self.login_user)
                return True
        else:
            print("\033[1;31m用户名或密码错误,请检查!\033[0m")
            return False

    def show_host(self):
        self.host_tb.align["ID"] = "1"
        self.host_tb.padding_width = 1
        self.cursor.execute("SELECT a.id,c.hostname,c.private_ip,c.public_ip FROM user_host a \
                            LEFT JOIN `user` b ON a.user_id=b.uid LEFT JOIN `host` c ON a.host_id=c.hid \
                                        WHERE b.username='%s' AND b.password='%s'" % (self.login_user, self.login_pwd))
        res_li = self.cursor.fetchall()
        if not res_li:
            print("\033[1;31m当前用户下主机列表为空!\033[0m")
            return
        for item in res_li:
            temp_li = [item['id'], item['hostname'], item['private_ip'], item['public_ip']]
            self.host_tb.add_row(temp_li)
            temp_li.clear()
        print()
        print("\033[1;32m 当前用户主机列表信息\033[0m ".center(50, '*'))
        print(self.host_tb)

    def get_host_info(self):
        self.cursor.execute("SELECT c.hostname,c.private_ip,c.public_ip,c.ssh_port,c.username,c.password,d.group_name FROM user_host a\
                                 LEFT JOIN `user` b ON a.user_id=b.uid \
                                 LEFT JOIN `host` c ON a.host_id=c.hid \
                                 LEFT JOIN host_group d ON a.group_id=d.gid \
                                 WHERE b.username='%s' AND b.password='%s'" % (self.login_user, self.login_pwd))
        all_host_dic = self.cursor.fetchall()
        # print(all_host_dic)           # 获取当前用户下所有的主机信息
        return all_host_dic

    def __del__(self):
        self.db_close()


def main():
    print("#" * 100)
    print("###", "\033[1;33mWelcome to command system\033[0m".center(103, ' '), "###")
    print("#" * 100)
    while True:
        login_user = input("请输入用户名: ").strip()
        login_pwd = input("请输入密码: ").strip()
        if not login_user or not login_pwd: continue
        obj = Auth_show_info(login_user, login_pwd)
        res = obj.show_user_info()
        if not res: continue
        obj.show_host()
        # print(obj.host_info())


if __name__ == '__main__':
    main()
