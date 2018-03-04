#!/usr/bin/env python
# -*-coding:utf-8-*-
# @Time    : 2018-03-03 22:23
# @Author  : huifer
# @File    : IpSpider.py
# @Software: PyCharm
import requests
from lxml import etree
from fake_useragent import UserAgent

from util.LogHandler import LogHandler
from db.SqliteClient import SqliteClient

import time


class IpSpider(object):

    def __init__(self, urltype):
        """

        :param urltype: 0-国内高匿代理IP;1-国内透明代理IP;2-国内HTTPS代理IP;3-国外高匿代理IP
        """
        url_list = {
            0: 'http://www.pcdaili.com/index.php?m=daili&a=free&type=1',
            1: 'http://www.pcdaili.com/index.php?m=daili&a=free&type=2',
            2: 'http://www.pcdaili.com/index.php?m=daili&a=free&type=3',
            3: 'http://www.pcdaili.com/index.php?m=daili&a=free&type=4',
        }
        if urltype in [0, 1, 2, 3]:
            self.url = url_list.get(urltype)
        self.ua = UserAgent()
        self.sqlite = SqliteClient()
        self.sqlite.create_table_sqlite()
        self.log = LogHandler("db")

    def run_spider(self, page):
        """
        进行爬虫抓取
        :param page:几页
        :return:tuple
        """
        iplist = []
        for x in range(1, page + 1):
            headers = {
                'Host': 'www.pcdaili.com',
                "user-agent": self.ua.chrome
            }
            sp_url = self.url + "&page=%d" % x
            try:
                r = requests.get(sp_url, headers=headers)
            except Exception as e:
                self.log.error(e)
            finally:
                html = etree.HTML(r.text)
                res = html.xpath('/html/body/div/div/div[2]/table/tbody/tr/td/text()')
                iptuple = self.group_list(res, 7)
                iplist.append(iptuple)
                time.sleep(1)
                self.log.info("spider html ok")
        return iplist

    def group_list(self, grouped, length):
        """
        分组
        :param grouped:列表
        :param length:分组长度
        :return: [(),()]
        """
        d = [tuple(grouped[i:i + length]) for i in range(0, len(grouped), length)]

        return d[:13]

    def ip_insert_sql(self, ip_list):
        """
        ip代理插入数据库
        :param ip_list: ip列表
        :return:
        """
        for y in range(len(ip_list)):
            # print(ip_list[y])
            for x in ip_list[y]:
                ip_addr = x[0]
                ip_port = x[1]
                type = x[3]
                ip_proxy = type + "://" + ip_addr + ":" + ip_port
                is_ok_ip = self.validate_ip(type=type, ip_proxy=ip_proxy)
                if is_ok_ip:
                    insert_res = self.sqlite.insert_table_sqlite(ip_addr=ip_addr,
                                                                     ip_port=ip_port,
                                                                     type=type,
                                                                     ip_proxy=ip_proxy)

        return True

    def validate_ip(self, type, ip_proxy):
        """
        测试ip是否能够代理访问https://weibo.com/
        :param type:ip类型
        :param ip_proxy:IP地址
        :return:true false
        """
        test_url = "https://weibo.com/"
        proxies = {
            type: ip_proxy
        }

        try:
            requests.get(test_url, proxies=proxies)
        except Exception as e:
            self.log.error(e)
            return False
        else:
            self.log.info(ip_proxy + " is ok !test url is " + test_url)
            return True


if __name__ == '__main__':
    ipspider = IpSpider(2)
    ip_list = ipspider.run_spider(page=3)

    # print(ip_list)
    ipspider.ip_insert_sql(ip_list)
    # ipspider.validate_ip(type='HTTPS',ip_proxy='HTTPS://109.120.199.27:8081')
