#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : MySqlitClient.py
# @Author: huifer
# @Date  : 2018-3-2
import datetime

from util.DBConfig import DBConfig
from util.LogHandler import LogHandler
import pymysql.cursors


class MysqlCline(object):
    def __init__(self, dbtype):
        """
        创建数据库
        :param dbtype: 数据库类型
        """
        self.log = LogHandler("db")

        dbconfig = DBConfig().get_db_config(dbtype)

        # self.connection = pymysql.connect(
        #     **dbconfig,
        # )
        if dbtype == "mysql":
            # print("ok")
            self.connection = pymysql.connect(
                **dbconfig,
            )

    def create_table_mysql(self):
        """
        创建表
        :return: false true
        """
        sql = """CREATE TABLE IF NOT EXISTS ipdaili (
          ip_addr varchar(30) DEFAULT NULL,
          ip_port varchar(11) DEFAULT NULL,
          type varchar(10) DEFAULT NULL,
          Downloadtime varchar(30) DEFAULT NULL
            )"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            self.log.info("create success")
            return True
        except Exception as e:
            self.log.error(e)
            return False
        finally:
            self.log.info("create success")
            return True
        pass

    def insert_table_mysql(self, ip_addr, ip_port, type):
        """
        插入数据
        :param ip_addr: ip地址
        :param ip_port: 端口
        :param type:    类型
        :return:false true
        """
        # 插入数据  # TODO 不能用with
        try:
            cursor = self.connection.cursor()
            downloadtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql = "INSERT INTO ipdaili VALUES ('" + ip_addr + "','" + ip_port + "','" + type + "','" + downloadtime + "');"

            cursor.execute(sql)
            self.connection.commit()
            self.connection.commit()
            self.log.info("inserter sql success")
            return True
        except Exception as e:
            self.log.error(e)
            return False
        finally:
            self.log.info("insert success")

    def search_table_mysql(self, sql="select * from ipdaili"):
        """
        查询数据库
        :param sql:查询语句
        :return:结果值 false
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
        except Exception as e:
            self.log.error(e)
            return False
        finally:

            self.log.info("search success")
            return res

    def __del__(self):
        """
        关闭数据库链接
        :return:
        """
        self.connection.close()


if __name__ == '__main__':
    # MysqlCline("mysql").sql_search("select * from weather")
    mysqlcline = MysqlCline(
        dbtype="mysql"
    )
    # mysqlcline.create_table_mysql()
    # mysqlcline.search_table_mysql("select * from weather")
    # mysqlcline.create_table_mysql()
    # mysqlcline.insert_table_mysql(ip_addr="192.168.1.3",ip_port='3304',type="http")
