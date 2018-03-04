#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : DBConfig.py
# @Author: huifer
# @Date  : 2018-3-2
from configparser import ConfigParser
import os

from util.LogHandler import LogHandler

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(os.path.dirname(os.path.abspath(CURRENT_PATH)), 'config')



class DBConfig(object):

    def __init__(self, ):
        self.config = ConfigParser()
        self.name = "config.ini"
        self.sql_path = os.path.join(ROOT_PATH, self.name)
        self.log = LogHandler("db")

    def add_db_config(self, dbtype, host, port, user, password, database, charset):
        """
        增加或修改数据库配置,配置文件位置config/config.ini
        :param dbtype: 数据库类型
        :param host: 主机
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名称
        :param charset: 字符集
        :return: True 增加或修改成功
        """
        self.config.read(self.sql_path, encoding="utf-8")

        if dbtype in self.config:
            # TODO 设置数据库配置
            self.config.set(dbtype, "host", host)
            self.config.set(dbtype, "port", port)
            self.config.set(dbtype, "user", user)
            self.config.set(dbtype, "password", password)
            self.config.set(dbtype, "database", database)
            self.config.set(dbtype, "charset", charset)

            with open(self.sql_path, "w", encoding="utf8") as f:
                self.config.write(f)
                self.log.info(
                    "Amend the success ， Modifying the data %s" % [dbtype, host, port, user, password, database, charset])
                return True
        else:
            # TODO 修改数据库配置
            self.config.add_section(dbtype)
            self.config.set(dbtype, "host", host)
            self.config.set(dbtype, "port", port)
            self.config.set(dbtype, "user", user)
            self.config.set(dbtype, "password", password)
            self.config.set(dbtype, "database", database)
            self.config.set(dbtype, "charset", charset)

            with open(self.sql_path, "w+", encoding="utf8") as f:
                self.config.write(f)
                self.log.info(
                    "Amend the success ， Modifying the data %s" % [dbtype, host, port, user, password, database, charset])
                return True

    def get_db_config(self, dbtyep):
        """
        返回数据库相关配置
        :param dbtyep: 数据库类型
        :return: dict(数据库配置) None不存在
        """
        # TODO 获取配置
        self.config.read(self.sql_path, encoding="utf-8")
        if dbtyep in self.config:
            options = self.config.items(dbtyep)
            option = {x: y for x, y in options}
            for k,v in option.items():
                if k == "port":
                    option[k]=int(v)
            self.log.info("success %s" % option)
            return option
        else:
            self.log.error("Parameter error %s" % dbtyep)
            return None

    def update_config(self, section, option, value):
        """
        根据传入参数修改相关配置
        :param section: 块
        :param option:  修改key
        :param value:   修改值
        :return: True 修改成功 False 参数错误
        """
        # TODO 新增其他配置
        self.config.read(self.sql_path, encoding="utf-8")
        if section in self.config.sections():
            if option in self.config.options(section):
                self.config.set(section, option, value)
                # return '需要修改'
                self.log.info("Need to be modified")
            else:
                self.log.error("Parameter error %s" % option)
                return None
        else:
            self.log.error("Parameter error %s" % section)

            return None

        with open(self.sql_path, "w", encoding="utf8") as f:
            self.config.write(f)
            self.log.info("Amend the success")
            return True

    def add_config(self, section, option, value):
        """
        独立创建其他配置文件
        :param section: 块
        :param option:  修改key
        :param value:   修改值
        :return: True 修改成功
        """
        self.config.read(self.sql_path, encoding="utf-8")
        if section not in self.config.sections():
            self.config.add_section(section)
            self.config.set(section, option, value)
            with open(self.sql_path, "w+", encoding="utf8") as f:
                self.config.write(f)
                self.log.info("Amend the success")
        elif section in self.config.sections():
            self.config.set(section,option,value)
            with open(self.sql_path, "w+", encoding="utf8") as f:
                self.config.write(f)
                self.log.info("Amend the success")


if __name__ == '__main__':
    set_config = DBConfig()
    # set_config.add_db_config(
    #     dbtype='mysql',
    #     host='localhost',
    #     port='3306',
    #     user='root',
    #     password='root',
    #     database='tianqi',
    #     charset="utf8",
    # )
    # print(set_config.get_db_config("mysql"))
    # print(set_config.update_config(
    #     section='mysql',
    #     option='1',
    #     value='ROOT',
    # ))
    # print(set_config.add_config("a", "b", "c"))
    set_config.add_config('sqlit','path','db')
    set_config.add_config('sqlit',"dbname",'test')