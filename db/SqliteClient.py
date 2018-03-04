#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Time    : 2018-03-02 20:19
# @Author  : huifer
# @File    : SqliteClient.py
# @Software: PyCharm
import os

from util.LogHandler import LogHandler
from util.DBConfig import DBConfig
import sqlite3

import datetime

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class SqliteClient(object):
    def __init__(self, dbtype='sqlit'):
        """

        :param dbtype: 选择数据库类型
        """
        self.log = LogHandler("db")
        DBCONFIG = DBConfig().get_db_config(dbtype)
        ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(CURRENT_PATH)), DBCONFIG.get('path'))
        DB_NAME = DBCONFIG.get("dbname")
        DB_PATH = os.path.join(ROOT_PATH,DB_NAME)
        print(DB_PATH)
        self.conn = sqlite3.connect(DB_PATH)

        self.c = self.conn.cursor()

    def create_table_sqlite(self):
        """
        创建数据表
        :return: false true
        """
        try:
            sql = "create table if not exists ipdaili(ip_addr TEXT, ip_port TEXT, type TEXT,ip_proxy TEXT, Downloadtime TEXT)"
            # self.c.execute('''CREATE TABLE ipdaili
                 # (ip_addr TEXT, ip_port TEXT, type TEXT,ip_proxy TEXT, Downloadtime TEXT )''')
            self.c.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.log.error(e)
            return False
        else:
            self.log.info("create success")
            return True

    def insert_table_sqlite(self, ip_addr, ip_port, type,ip_proxy):
        """
        插入数据
        :param ip_addr: ip地址
        :param ip_port: 端口
        :param type:    类型
        :return:false true
        """
        downloadtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            self.c.execute("INSERT INTO ipdaili (ip_addr,ip_port,type,ip_proxy,Downloadtime) VALUES (?,?,?,?,?)",
                           (ip_addr, ip_port, type,ip_proxy, downloadtime))
            self.conn.commit()
        except Exception as e:
            self.log.error(e)
            return False
        else:
            self.log.info("insert success")
            return True

    def search_table_sqlite(self, sql="select * from ipdaili"):
        """
        查询数据数
        :param sql:执行sql语句
        :return:结果值 false
        """
        try:
            res = self.c.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.log.error(e)
            return False
        else:
            self.log.info("search success")
            return res.fetchall()

    def __del__(self):
        """
        关闭链接
        :return:
        """
        # class_name = self.__class__.__name__
        self.conn.close()
        # print(class_name, "销毁")


if __name__ == '__main__':
    sqlcle = SqliteClient()
    # sqlcle.create_table_sqlite()
    # print(sqlcle.insert_table_sqlite(1,1,2))
    # print(sqlcle.search_table_sqlite("select * from ipdaili"))
    # print(sqlcle.search_table_sqlite())