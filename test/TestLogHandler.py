#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : TestLogHandler.py
# @Author: huifer
# @Date  : 2018-3-2
from util.LogHandler import LogHandler


def test_log_handler():
    log = LogHandler("Tlog")
    log.info("test log")
    log.resetName("test1")
    log.info('this is a log from test1')

    log.resetName('test2')
    log.info('this is a log from test2')


if __name__ == '__main__':
    test_log_handler()
