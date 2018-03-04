#!/usr/bin/env python
#-*-coding:utf-8-*-
# @Time    : 2018-03-04 19:15
# @Author  : huifer
# @File    : TestIPpSpider.py
# @Software: PyCharm
from spider.IpSpider import IpSpider

def test_ip_spider():
    ipspider = IpSpider(3)
    ip_list = ipspider.run_spider(page=3)
    ipspider.ip_insert_sql(ip_list)


if __name__ == '__main__':
    test_ip_spider()