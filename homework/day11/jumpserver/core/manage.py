#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "shuke"
# Date: 2017/7/14 0014

import pymysql
from conf.settings import DATABASE,logger
from core.login import Auth_show_info


class AdminView:
    def __init__(self):
        self.conn = pymysql.connect(**DATABASE)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def db_close(self):
        self.cursor.close()
        self.conn.close()

    def update(self, sql):
        """
        update sql
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print("\033[1;32mUpdate success!\033[0m")
        except Exception as e:
            self.conn.rollback()
            print("\033[1;31mUpdate faild!\033[0m")
        finally:
            self.db_close()

    def dalete(self, sql):
        """
        delete sql
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print("\033[1;32mDelete success!\033[0m")
        except Exception as e:
            self.conn.rollback()
            print("\033[1;31mDelete faild!\033[0m")
        finally:
            self.db_close()

    def insert(self, sql):
        """
        insert sql
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            print("\033[1;32mInsert success!\033[0m")
        except Exception as e:
            self.conn.rollback()
            print("\033[1;31mInsert faild!\033[0m")
        finally:
            self.db_close()

    def select(self,sql):
        """
        select sql
        """
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            data = self.cursor.fetchall()
            for item in data:
                print(item)
            print("\033[1;32mSelect success!\033[0m")
        except Exception as e:
            print("\033[1;31mSelect faild!\033[0m")
        finally:
            self.db_close()


def main(login_user,login_pwd):
    admin_obj = Auth_show_info(login_user,login_pwd)
    res = admin_obj.show_user_info()
    if res:
        while True:
            sql = input("\033[1;32mmysql> \033[0m").strip()
            if sql == "quit" or sql == "exit":
                quit()
            inp_li = sql.split(' ')
            operation = inp_li[0]
            obj = AdminView()               # 实例化
            if hasattr(obj,operation):
                action_obj = getattr(obj,operation)
                action_obj(sql)
                logger.info("user: %s sql: %s" % (login_user,sql))
    else:
        print("\033[1;31m用户名或密码错误,请检查!\033[0m")







if __name__ == '__main__':
    main('admin',123456)
    # admin_obj = Auth_show_info('admin','123456')
    # res = admin_obj.show_user_info()
    # res = hasattr(admin_obj,'update')
    # print(res)