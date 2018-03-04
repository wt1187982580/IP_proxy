#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : TestDBConfig.py
# @Author: huifer
# @Date  : 2018-3-2
from util.DBConfig import DBConfig


def test_db_config():
    set_config = DBConfig()
    set_config.add_db_config(
        dbtype='mysql',
        host='192.168.1.87',
        port='3306',
        user='root',
        pwd='ROOT',
        database='wt',
        charset="utf-8",
    )
    print(set_config.get_db_config("mongodb"))
    print(set_config.update_config(
        section='mongodb',
        option='user',
        value='ROOT',
    ))
    print(set_config.add_config("a", "b", "c"))


if __name__ == '__main__':
    test_db_config()
